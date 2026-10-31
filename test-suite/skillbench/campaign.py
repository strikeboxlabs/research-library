"""Serial, resumable campaigns with frozen inputs and controller-owned grading."""
from __future__ import annotations

import contextlib
import copy
import json
import os
from pathlib import Path
import socket
import time
import uuid

from .common import copy_package, digest, engine_hash, package_manifest, read_json, utc_now, write_json
from .planning import build_plan, library_inventory


@contextlib.contextmanager
def campaign_lock(directory):
    path = Path(directory) / "controller.lock"
    if path.exists():
        owner = read_json(path)
        if owner.get("host") != socket.gethostname():
            raise ValueError("Campaign lock belongs to another host; inspect it before resuming")
        if os.name != "posix":
            raise ValueError("An existing controller lock must be inspected manually on non-POSIX hosts")
        try:
            os.kill(int(owner["pid"]), 0)
        except ProcessLookupError:
            path.unlink()
        except (OSError, KeyError, ValueError) as exc:
            raise ValueError("Cannot verify stale campaign lock") from exc
        else:
            raise ValueError("Campaign controller is already running")
    with path.open("x", encoding="utf-8") as stream:
        json.dump({"pid": os.getpid(), "host": socket.gethostname()}, stream)
    try:
        yield
    finally:
        path.unlink(missing_ok=True)


def calibrate_cases(case_ids, output):
    from .cases import CASES
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    results = []
    for name in case_ids:
        case = CASES[name]
        work = output / name
        work.mkdir()
        oracle = case.prepare(work, 9321)
        negative = case.grade(work, oracle)
        case.solve(work, oracle)
        positive = case.grade(work, oracle)
        results.append({"case_id": name, "empty_solution_rejected": not negative["passed"],
                        "reference_solution_accepted": positive["passed"],
                        "passed": not negative["passed"] and positive["passed"]})
    write_json(output / "calibration.json", {"kind": "python_grader_calibration", "results": results,
               "note": "Reference artifact construction only; no CLI procedure or model was evaluated."})
    return results


def create_campaign(config, preflight):
    cfg = copy.deepcopy(config)
    root = Path(cfg["runs_root"])
    root.mkdir(parents=True, exist_ok=True)
    run = root / (time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()) + "-" + uuid.uuid4().hex[:8])
    run.mkdir(mode=0o700)
    inventory = library_inventory(cfg["library_root"])
    plan = build_plan(cfg, inventory)
    if len(plan) > cfg["budgets"]["max_trials"]:
        raise ValueError("Planned trials exceed max_trials; reduce cases/repetitions or raise the explicit limit")
    snapshot_hashes = {}
    selected = sorted({name for trial in plan for name in trial["selected_skills"]})
    targets = {trial["skill"] for trial in plan}
    for name in selected:
        source = Path(cfg["library_root"]) / "skills" / name
        dest = run / "snapshots" / "current" / name
        snapshot_hashes[f"current/{name}"] = copy_package(source, dest)
        if "candidate" in cfg["conditions"]:
            source = Path(cfg["candidate_root"]) / name if name in targets else source
            snapshot_hashes[f"candidate/{name}"] = copy_package(source, run / "snapshots" / "candidate" / name)
    if preflight.get("image_id"):
        cfg["runtime"]["image"] = preflight["image_id"]
    manifest = {"schema_version": 1, "created_at": utc_now(), "engine_hash": engine_hash(),
                "config": cfg, "config_hash": digest(cfg), "inventory": inventory,
                "preflight": preflight, "snapshots": snapshot_hashes, "plan": plan}
    manifest["experiment_hash"] = digest({k: manifest[k] for k in ("config", "plan", "engine_hash", "snapshots")})
    write_json(run / "manifest.json", manifest)
    return run


def load_results(run):
    return [read_json(p) for p in sorted((Path(run) / "trials").glob("*/result.json"))]


def verify_campaign(run):
    run = Path(run).resolve()
    manifest = read_json(run / "manifest.json")
    if digest({k: manifest[k] for k in ("config", "plan", "engine_hash", "snapshots")}) != manifest["experiment_hash"]:
        raise ValueError("Experiment manifest changed")
    if manifest["engine_hash"] != engine_hash():
        raise ValueError("Controller/case code changed; start a new campaign instead of mixing implementations")
    if digest(manifest["config"]) != manifest["config_hash"]:
        raise ValueError("Campaign config was modified")
    for name, expected in manifest["snapshots"].items():
        if package_manifest(run / "snapshots" / name) != expected:
            raise ValueError(f"Frozen skill changed: {name}")
    return manifest


def run_campaign(run, runner=None, progress=print):
    from .cases import CASES
    from .runtime import run_worker
    runner = runner or run_worker
    run = Path(run).resolve()
    manifest = verify_campaign(run)
    cfg = manifest["config"]
    started = time.monotonic()
    with campaign_lock(run):
        state_path = run / "state.json"
        previous = read_json(state_path) if state_path.exists() else {}
        consumed_seconds = float(previous.get("controller_seconds", 0))
        stop_reason = "interrupted"
        try:
            for trial in manifest["plan"]:
                trial_dir = run / "trials" / trial["trial_id"]
                if (trial_dir / "result.json").exists():
                    continue
                # A crash may have left unknown side effects. Record it, never replay in that world.
                if (trial_dir / "started.json").exists():
                    from .runtime import cleanup_interrupted
                    cleanup = cleanup_interrupted(trial_dir / "logs", cfg["runtime"])
                    if not cleanup.get("cleanup_confirmed"):
                        stop_reason = "interrupted_cleanup_failed"
                        break
                    write_json(trial_dir / "result.json", {**trial, "status": "interrupted_runner",
                               "passed": False, "usage": {}, "error": "Controller interrupted; not a model outcome"})
                    continue
                elapsed = consumed_seconds + time.monotonic() - started
                remaining = cfg["budgets"]["max_campaign_seconds"] - elapsed
                if remaining <= 0:
                    stop_reason = "campaign_time_budget"
                    break
                prior = load_results(run)
                token_limit = cfg["budgets"].get("max_total_tokens")
                if token_limit is not None:
                    measured = [r.get("usage", {}).get("total_tokens") for r in prior
                                if r["status"] != "fixture_error"]
                    if any(v is None for v in measured):
                        stop_reason = "token_usage_unavailable"
                        break
                    if sum(measured) >= token_limit:
                        stop_reason = "campaign_token_budget"
                        break
                trial_dir.mkdir(parents=True, exist_ok=True)
                # Reserve the bounded attempt's time before launch. A crash cannot reset its allowance.
                write_json(state_path, {"status": "running", "controller_seconds": elapsed + min(cfg["runtime"]["timeout_seconds"], remaining)})
                write_json(trial_dir / "started.json", {"started_at": utc_now(), **trial})
                workspace = trial_dir / "workspace"
                workspace.mkdir()
                skill_dir = trial_dir / "skills"
                skill_dir.mkdir()
                case = CASES[trial["case_id"]]
                result = {**trial, "started_at": utc_now(), "passed": False, "usage": {}}
                try:
                    oracle = case.prepare(workspace, trial["seed"])
                    write_json(trial_dir / "oracle.json", oracle)
                    for name in trial["selected_skills"]:
                        source_arm = "candidate" if trial["condition"] == "candidate" else "current"
                        copy_package(run / "snapshots" / source_arm / name, skill_dir / name)
                except Exception as exc:
                    result.update(status="fixture_error", error=f"{type(exc).__name__}: {exc}")
                    write_json(trial_dir / "result.json", result)
                    progress(f"{trial['trial_id']}: fixture_error")
                    continue
                prompt = case.prompt()
                if trial["mode"] == "explicit" and trial["condition"] != "baseline":
                    prompt = f"/skill:{case.skill} {prompt}"
                (trial_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
                runtime_cfg = copy.deepcopy(cfg["runtime"])
                runtime_cfg["skill_order"] = trial["selected_skills"]
                runtime_cfg["timeout_seconds"] = min(runtime_cfg["timeout_seconds"], remaining)
                try:
                    observed = runner(workspace, skill_dir, prompt, runtime_cfg, trial_dir / "logs")
                    result.update(observed)
                except Exception as exc:
                    result.update(status="runner_error", error=f"{type(exc).__name__}: {exc}")
                if result.get("cleanup_confirmed", True):
                    try:
                        grading = case.grade(workspace, oracle)
                        result["grading"] = grading
                        result["passed"] = result["status"] == "completed" and grading["passed"]
                    except Exception as exc:
                        result.update(status="grader_error", error=f"{type(exc).__name__}: {exc}", passed=False)
                else:
                    result.update(status="runner_error", error="cleanup_not_confirmed; grading skipped", passed=False)
                result["finished_at"] = utc_now()
                write_json(trial_dir / "result.json", result)
                write_json(state_path, {"status": "running", "controller_seconds": consumed_seconds + time.monotonic() - started})
                progress(f"{trial['trial_id']}: {result['status']}, passed={result['passed']}")
                if not result.get("cleanup_confirmed", True):
                    stop_reason = "cleanup_failed"
                    break
            else:
                stop_reason = "complete"
        finally:
            write_json(state_path, {"status": stop_reason, "updated_at": utc_now(),
                       "controller_seconds": consumed_seconds + time.monotonic() - started})
    return {"run_dir": str(run), "status": stop_reason, "recorded_trials": len(load_results(run))}


def smoke_cases(config, output):
    """Run known reference CLI procedures in the same isolated image, without a model."""
    from .cases import CASES
    from .reference import reference_commands
    from .runtime import preflight, run_reference
    runtime = copy.deepcopy(config["runtime"])
    runtime["required_tools"] = sorted({tool for key in config["cases"] for tool in CASES[key].tools})
    check = preflight(runtime)
    if not check.get("ok"):
        raise ValueError("CLI smoke preflight failed: " + str(check.get("errors")))
    runtime["image"] = check["image_id"]
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    write_json(output / "manifest.json", {"kind": "reference_cli_smoke", "preflight": check,
               "runtime": runtime, "engine_hash": engine_hash()})
    rows = []
    for key in config["cases"]:
        case = CASES[key]
        directory = output / key
        workspace = directory / "workspace"
        workspace.mkdir(parents=True)
        oracle = case.prepare(workspace, config["seed"])
        write_json(directory / "oracle.json", oracle)
        result = run_reference(workspace, reference_commands(key), runtime, directory / "logs")
        grade = case.grade(workspace, oracle) if result.get("cleanup_confirmed") else {"passed": False, "details": ["cleanup failed"]}
        row = {"case_id": key, "runtime": result, "grading": grade,
               "passed": result["status"] == "completed" and grade["passed"]}
        write_json(directory / "result.json", row)
        rows.append(row)
        if not result.get("cleanup_confirmed"):
            break
    write_json(output / "smoke.json", {"kind": "reference_cli_smoke", "results": rows,
               "passed": len(rows) == len(config["cases"]) and all(r["passed"] for r in rows),
               "note": "Real reference CLI execution, no GLM/Pi task outcome or skill effectiveness claim."})
    return rows
