from __future__ import annotations

import argparse
import copy
import json
import os
from pathlib import Path
import sys
import time
import uuid

from .campaign import calibrate_cases, create_campaign, load_results, run_campaign, smoke_cases, verify_campaign
from .common import read_json, utc_now, write_json
from .config import load_config
from .planning import build_plan, library_inventory
from .reporting import make_report

DEFAULT_CONFIG = Path(__file__).resolve().parents[1] / "config.local.json"


def emit(value):
    print(json.dumps(value, indent=2, sort_keys=True))


def check_runtime(config):
    from .cases import CASES
    from .runtime import preflight
    runtime = dict(config["runtime"])
    runtime["required_tools"] = sorted({tool for case_id in config["cases"] for tool in CASES[case_id].tools})
    return preflight(runtime)


def execute_new(config, allow_holdout=False):
    from .cases import CASES
    if not allow_holdout and any(CASES[k].split == "holdout" for k in config["cases"]):
        raise ValueError("Protected cases require --allow-holdout; keep them out of optimization feedback")
    if not os.environ.get(config["runtime"].get("api_key_env", "ZAI_API_KEY")):
        raise ValueError("Set the configured API key environment variable before worker trials")
    check = check_runtime(config)
    if not check.get("ok"):
        raise ValueError("Worker preflight failed: " + json.dumps(check.get("errors", check)))
    run = create_campaign(config, check)
    # No model calls until the independent graders accept their reference and reject empty outputs.
    calibration = calibrate_cases(config["cases"], run / "calibration")
    if not all(r["passed"] for r in calibration):
        raise ValueError(f"Fixture calibration failed; inspect {run}")
    print(f"Campaign: {run}", flush=True)
    result = run_campaign(run)
    make_report(run)
    return result


def development_evidence(run, skill):
    from .cases import CASES
    manifest = read_json(Path(run) / "manifest.json")
    if any(CASES[k].split != "development" for k in manifest["config"]["cases"]):
        raise ValueError("Optimization cannot consume a campaign containing holdout cases")
    records = []
    for row in load_results(run):
        if row.get("skill") != skill or row.get("split") != "development":
            continue
        # Deliberately do not include oracle files, full logs, environment or credentials.
        item = {k: row.get(k) for k in ("case_id", "split", "condition", "status", "passed",
                        "grading", "usage", "tool_calls", "skill_reads", "elapsed_seconds")}
        item["task_request"] = CASES[row["case_id"]].prompt()
        item["final_text"] = str(row.get("final_text", ""))[:2000]
        event_path = Path(run) / "trials" / row["trial_id"] / "logs" / "events.jsonl"
        excerpts = []
        if event_path.is_file() and not event_path.is_symlink() and event_path.stat().st_size <= 8 * 1024 * 1024:
            for line in event_path.read_text(encoding="utf-8", errors="replace").split("\n"):
                try:
                    event = json.loads(line)
                except ValueError:
                    continue
                if isinstance(event, dict) and event.get("type") in {"tool_execution_start", "tool_execution_end"}:
                    excerpts.append(json.dumps(event, ensure_ascii=False)[:1600])
            item["tool_trace_excerpts"] = excerpts[-8:]
        records.append(item)
    if not records:
        raise ValueError(f"No development observations for {skill}")
    return records


def optimize(config, skill, campaign, iterations):
    from .cases import CASES
    from .optimizer import propose_candidate
    if not 1 <= iterations <= 10:
        raise ValueError("iterations must be between 1 and 10")
    source = Path(config["library_root"]) / "skills" / skill
    if not source.is_dir() or source.parent != Path(config["library_root"]) / "skills":
        raise ValueError("Unknown skill package")
    cases = [k for k in config["cases"] if CASES[k].skill == skill and CASES[k].split == "development"]
    if not cases or any(CASES[k].split == "holdout" for k in config["cases"]):
        raise ValueError("Optimizer config must select development cases including the chosen skill")
    evidence = development_evidence(campaign, skill)
    output = Path(config["runs_root"]) / ("optimization-" + uuid.uuid4().hex[:12])
    output.mkdir(parents=True, mode=0o700)
    journal = {"created_at": utc_now(), "skill": skill, "iterations_limit": iterations,
               "status": "running", "candidates": [], "canonical_skills_modified": False,
               "worker_trials": 0, "known_total_tokens": 0, "token_accounting_complete": True}
    write_json(output / "optimization.json", journal)
    started = time.monotonic()
    for index in range(iterations):
        if time.monotonic() - started >= config["budgets"]["max_campaign_seconds"]:
            journal["status"] = "optimization_time_budget"
            break
        planned_trials = len(cases) * config["repetitions"] * 2
        remaining_trials = config["budgets"]["max_trials"] - journal["worker_trials"]
        if planned_trials > remaining_trials:
            journal["status"] = "optimization_trial_budget"
            break
        token_limit = config["budgets"].get("max_total_tokens")
        if token_limit is not None and (not journal["token_accounting_complete"] or journal["known_total_tokens"] >= token_limit):
            journal["status"] = "optimization_token_budget_or_unknown_usage"
            break
        candidate_root = output / "candidates" / f"{index+1:03d}"
        item = {"iteration": index+1, "candidate_root": str(candidate_root)}
        generation_counted = False
        try:
            proposal_config = copy.deepcopy(config)
            proposal_config["optimizer"]["timeout_seconds"] = min(
                proposal_config["optimizer"].get("timeout_seconds", 180),
                max(1, config["budgets"]["max_campaign_seconds"] - (time.monotonic()-started)))
            proposal = propose_candidate(source, candidate_root / skill, evidence, proposal_config)
            item["proposal"] = proposal
            tokens = proposal.get("generation", {}).get("usage", {}).get("total_tokens")
            journal["known_total_tokens"] += tokens or 0
            journal["token_accounting_complete"] &= tokens is not None
            generation_counted = True
            write_json(output / f"proposal-{index+1:03d}.json", proposal)
            if token_limit is not None and (tokens is None or journal["known_total_tokens"] >= token_limit):
                raise ValueError("Proposal exhausted token budget or its usage is unavailable; candidate retained without evaluation")
            cfg = copy.deepcopy(config)
            cfg["cases"] = cases
            cfg["conditions"] = ["current", "candidate"]
            cfg["candidate_root"] = str(candidate_root)
            cfg["runs_root"] = str(output / "campaigns")
            cfg["budgets"]["max_trials"] = remaining_trials
            if token_limit is not None:
                cfg["budgets"]["max_total_tokens"] = token_limit - journal["known_total_tokens"]
            cfg["budgets"]["max_campaign_seconds"] = max(1, config["budgets"]["max_campaign_seconds"] - (time.monotonic()-started))
            run = execute_new(cfg)
            item["evaluation"] = run
            worker_results = load_results(run["run_dir"])
            journal["worker_trials"] += len(worker_results)
            for row in worker_results:
                if row["status"] == "fixture_error":
                    continue
                tokens = row.get("usage", {}).get("total_tokens")
                journal["known_total_tokens"] += tokens or 0
                journal["token_accounting_complete"] &= tokens is not None
            item["comparison"] = make_report(run["run_dir"])["comparisons"]
            item["status"] = "evaluated_candidate_requires_confirmation"
            evidence = development_evidence(run["run_dir"], skill) + evidence
        except Exception as exc:
            item.update(status="proposal_or_evaluation_error", error=f"{type(exc).__name__}: {exc}")
            if hasattr(exc, "generation"):
                item["generation"] = exc.generation
                if not generation_counted and exc.generation.get("request_count"):
                    tokens = exc.generation.get("usage", {}).get("total_tokens")
                    journal["known_total_tokens"] += tokens or 0
                    journal["token_accounting_complete"] &= tokens is not None
        journal["candidates"].append(item)
        write_json(output / "optimization.json", journal)
        print(f"Candidate {index+1}: {item['status']}", flush=True)
    if journal["status"] == "running":
        journal["status"] = "complete"
    journal["elapsed_seconds"] = time.monotonic()-started
    write_json(output / "optimization.json", journal)
    return {"output": str(output), **journal}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Linux CLI skill experiments; controller needs Python 3.10+, workers need Docker/Pi.")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="List implemented cases and coverage limits")
    for name in ("plan", "doctor", "run", "optimize", "smoke"):
        sub = commands.add_parser(name)
        sub.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
        if name == "smoke":
            sub.add_argument("--output", type=Path, required=True)
        if name == "run":
            sub.add_argument("--resume", type=Path)
            sub.add_argument("--allow-holdout", action="store_true")
        if name == "optimize":
            sub.add_argument("--skill", required=True)
            sub.add_argument("--campaign", type=Path, required=True)
            sub.add_argument("--iterations", type=int, default=1)
    sub = commands.add_parser("calibrate", help="Check graders using Python reference artifacts; no model or CLI evaluation")
    sub.add_argument("--output", type=Path, required=True)
    sub.add_argument("--cases", nargs="+")
    sub = commands.add_parser("report")
    sub.add_argument("run_dir", type=Path)
    args = parser.parse_args(argv)
    try:
        from .cases import CASES
        if args.command == "list":
            emit([{"id": c.id, "skill": c.skill, "family": c.family, "split": c.split,
                   "tools": c.tools, "description": c.description} for c in CASES.values()])
        elif args.command == "calibrate":
            ids = args.cases or list(CASES)
            if any(k not in CASES for k in ids):
                raise ValueError("Unknown case ID")
            rows = calibrate_cases(ids, args.output)
            emit(rows)
            return 0 if all(r["passed"] for r in rows) else 1
        elif args.command == "report":
            emit(make_report(args.run_dir))
        elif args.command == "run" and args.resume:
            manifest = verify_campaign(args.resume)
            if not os.environ.get(manifest["config"]["runtime"].get("api_key_env", "ZAI_API_KEY")):
                raise ValueError("Set the configured API key environment variable before resuming worker trials")
            if any(CASES[k].split == "holdout" for k in manifest["config"]["cases"]) and not args.allow_holdout:
                raise ValueError("Resume of protected evaluation requires --allow-holdout")
            check = check_runtime(manifest["config"])
            if not check.get("ok"):
                raise ValueError("Runtime preflight failed before resume")
            emit(run_campaign(args.resume))
            make_report(args.resume)
        else:
            cfg = load_config(args.config)
            if args.command == "plan":
                inventory = library_inventory(cfg["library_root"])
                plan = build_plan(cfg, inventory)
                emit({"library_skills": len(inventory), "planned_trials": len(plan),
                      "within_trial_budget": len(plan) <= cfg["budgets"]["max_trials"], "plan": plan})
            elif args.command == "doctor":
                check = check_runtime(cfg)
                emit(check)
                return 0 if check.get("ok") else 1
            elif args.command == "run":
                emit(execute_new(cfg, args.allow_holdout))
            elif args.command == "smoke":
                rows = smoke_cases(cfg, args.output)
                emit(rows)
                return 0 if len(rows) == len(cfg["cases"]) and all(r["passed"] for r in rows) else 1
            elif args.command == "optimize":
                emit(optimize(cfg, args.skill, args.campaign, args.iterations))
        return 0
    except (ValueError, OSError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
