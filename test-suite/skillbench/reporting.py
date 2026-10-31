"""Descriptive results, paired differences and explicit coverage/measurement gaps."""
from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import random
import statistics

from .campaign import load_results
from .common import read_json, write_json

INVALID = {"fixture_error", "grader_error", "runner_error", "interrupted_runner"}


def summarize(results):
    groups = defaultdict(list)
    for result in results:
        groups[result["condition"]].append(result)
    out = {}
    for condition, rows in groups.items():
        eligible = [r for r in rows if r["status"] not in INVALID]
        successes = sum(bool(r.get("passed")) for r in eligible)
        metrics = {}
        for name in ("total_tokens", "cost_usd"):
            values = [r.get("usage", {}).get(name) for r in rows]
            # Include spend on ALL attempts; incomplete accounting cannot be a zero-cost win.
            total = sum(values) if values and all(isinstance(v, (int, float)) for v in values) else None
            metrics[name] = total
            metrics[name + "_per_success"] = total / successes if total is not None and successes else None
            metrics[name + "_missing_trials"] = sum(v is None for v in values)
        times = sorted(r["elapsed_seconds"] for r in eligible if isinstance(r.get("elapsed_seconds"), (int, float)))
        out[condition] = {"assigned_recorded": len(rows), "evaluated": len(eligible), "passed": successes,
                          "pass_rate": successes / len(eligible) if eligible else None,
                          "recorded_pass_rate_including_infrastructure": successes / len(rows) if rows else None,
                          "statuses": dict(Counter(r["status"] for r in rows)),
                          "median_seconds": statistics.median(times) if times else None, **metrics}
    return out


def paired_comparison(results, challenger="candidate", incumbent="current"):
    blocks = defaultdict(dict)
    for row in results:
        blocks[row["block_id"]][row["condition"]] = row
    families = defaultdict(list)
    wins = losses = ties = 0
    for pair in blocks.values():
        if challenger not in pair or incumbent not in pair:
            continue
        a, b = pair[challenger], pair[incumbent]
        if a["status"] in INVALID or b["status"] in INVALID:
            continue
        delta = int(bool(a["passed"])) - int(bool(b["passed"]))
        families[a.get("family", a["case_id"])].append(delta)
        wins += delta > 0
        losses += delta < 0
        ties += delta == 0
    family_means = [sum(v)/len(v) for v in families.values()]
    interval = None
    # Tiny pilot families do not justify a deceptively precise bootstrap interval.
    if len(family_means) >= 5:
        rng = random.Random(9351)
        draws = sorted(sum(rng.choices(family_means, k=len(family_means)))/len(family_means) for _ in range(2000))
        interval = [draws[50], draws[1949]]
    return {"challenger": challenger, "incumbent": incumbent, "paired_trials": wins+losses+ties,
            "wins": wins, "losses": losses, "ties": ties, "task_families": len(families),
            "family_macro_pass_rate_delta": sum(family_means)/len(family_means) if family_means else None,
            "family_bootstrap_95pct": interval,
            "decision": "descriptive_only_no_automatic_promotion",
            "note": "Repeated seeds are not independent task families. Pilot results do not establish library-wide gains."}


def make_report(run):
    run = Path(run)
    manifest = read_json(run / "manifest.json")
    rows = load_results(run)
    summary = {"schema_version": 1, "run_dir": str(run), "planned_trials": len(manifest["plan"]),
               "recorded_trials": len(rows), "conditions": summarize(rows),
               "comparisons": [paired_comparison(rows, c, "current")
                               for c in ("baseline", "candidate") if c in manifest["config"]["conditions"]],
               "case_coverage": {k: dict(Counter(r["status"] for r in rows if r["case_id"] == k))
                                 for k in manifest["config"]["cases"]}}
    write_json(run / "report.json", summary)
    lines = ["# Skill experiment results", "", "Observed results only. See manifest.json for exact inputs and image identity.", "",
             "| Condition | Evaluated | Passed | Pass rate | Total tokens | Tokens / success |", "|---|---:|---:|---:|---:|---:|"]
    for name, value in summary["conditions"].items():
        fmt = lambda v: "unknown" if v is None else f"{v:.3f}" if isinstance(v, float) else str(v)
        lines.append("| " + " | ".join([name]+[fmt(value[k]) for k in ("evaluated", "passed", "pass_rate", "total_tokens", "total_tokens_per_success")]) + " |")
    lines += ["", "Failures/timeouts remain in the measured trial denominator. Infrastructure/grader errors are reported separately.",
              "Cost and usage include all recorded attempts; missing measurements remain unknown.",
              "", "Paired comparisons and case/status coverage are in report.json. No automatic promotion is performed.",
              "These artifact graders do not independently grade every claim in the final prose response."]
    (run / "report.md").write_text("\n".join(lines)+"\n", encoding="utf-8")
    return summary
