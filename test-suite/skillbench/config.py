from __future__ import annotations

import copy
from pathlib import Path

from .common import positive, read_json


def load_config(path):
    path = Path(path).resolve()
    raw = read_json(path)
    return validate_config(raw, path.parent)


def validate_config(raw, base):
    from .cases import CASES
    if not isinstance(raw, dict):
        raise ValueError("Configuration must be an object")
    allowed = {"schema_version", "library_root", "runs_root", "runtime", "cases", "conditions",
               "repetitions", "seed", "selection", "budgets", "candidate_root", "optimizer"}
    if set(raw) - allowed:
        raise ValueError(f"Unknown config fields: {sorted(set(raw) - allowed)}")
    cfg = copy.deepcopy(raw)
    if cfg.get("schema_version") != 1:
        raise ValueError("schema_version must be 1")
    for key, default in (("library_root", ".."), ("runs_root", "../runs/skillbench")):
        cfg[key] = str((Path(base) / cfg.get(key, default)).resolve())
    if not (Path(cfg["library_root"]) / "skills").is_dir():
        raise ValueError("library_root must contain skills/")
    if Path(cfg["runs_root"]).is_relative_to(Path(cfg["library_root"]) / "skills"):
        raise ValueError("runs_root must be outside published skills")
    if cfg.get("candidate_root"):
        cfg["candidate_root"] = str((Path(base) / cfg["candidate_root"]).resolve())
    cfg.setdefault("cases", [k for k, c in CASES.items() if c.split == "development"])
    if not isinstance(cfg["cases"], list) or not cfg["cases"] or any(k not in CASES for k in cfg["cases"]):
        raise ValueError("cases must be a nonempty list of registered case IDs")
    if len(set(cfg["cases"])) != len(cfg["cases"]):
        raise ValueError("Duplicate case IDs")
    cfg.setdefault("conditions", ["baseline", "current"])
    if (not isinstance(cfg["conditions"], list) or not cfg["conditions"]
            or len(set(cfg["conditions"])) != len(cfg["conditions"])
            or any(x not in {"baseline", "current", "candidate"} for x in cfg["conditions"])):
        raise ValueError("conditions must be unique baseline/current/candidate values")
    if "candidate" in cfg["conditions"] and not cfg.get("candidate_root"):
        raise ValueError("candidate condition requires candidate_root containing skill folders")
    positive(cfg.setdefault("repetitions", 3), "repetitions", integer=True)
    if not isinstance(cfg.setdefault("seed", 1701), int) or isinstance(cfg["seed"], bool):
        raise ValueError("seed must be an integer")
    selection = cfg.setdefault("selection", {})
    if set(selection) - {"mode", "catalog_size", "distractors"}:
        raise ValueError("Unknown selection settings")
    if selection.setdefault("mode", "explicit") not in {"explicit", "discovery"}:
        raise ValueError("selection.mode must be explicit or discovery")
    positive(selection.setdefault("catalog_size", 1), "catalog_size", integer=True)
    if selection.setdefault("distractors", "similar") not in {"similar", "random"}:
        raise ValueError("distractors must be similar or random")
    limits = cfg.setdefault("budgets", {})
    if set(limits) - {"max_trials", "max_campaign_seconds", "max_total_tokens"}:
        raise ValueError("Unknown budgets settings")
    positive(limits.setdefault("max_trials", 100), "max_trials", integer=True)
    positive(limits.setdefault("max_campaign_seconds", 7200), "max_campaign_seconds")
    if limits.get("max_total_tokens") is not None:
        positive(limits["max_total_tokens"], "max_total_tokens", integer=True)
    runtime = cfg.setdefault("runtime", {})
    runtime_fields = {"image", "provider", "model", "base_url", "api", "api_key_env", "timeout_seconds",
                      "max_output_bytes", "memory", "cpus", "pids_limit", "uid", "gid", "network", "docker_binary",
                      "pi_version", "thinking", "context_window", "max_tokens", "reasoning", "temperature", "top_p"}
    if not isinstance(runtime, dict) or set(runtime) - runtime_fields:
        raise ValueError("Unknown runtime settings; credentials must be environment references")
    if not runtime.get("image") or not runtime.get("model"):
        raise ValueError("runtime.image and runtime.model are required")
    positive(runtime.setdefault("timeout_seconds", 180), "runtime.timeout_seconds")
    if not isinstance(cfg.get("optimizer", {}), dict):
        raise ValueError("optimizer must be an object")
    if any(k in cfg.get("optimizer", {}) for k in ("api_key", "key", "token", "password")):
        raise ValueError("Optimizer credentials must use api_key_env")
    return cfg
