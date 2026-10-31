"""Bounded Docker/Pi execution; no host-shell worker backend.

The caller supplies disposable fixture and skill directories, never an evaluator
checkout. Events describe observable calls, not whether the model understood them.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import tempfile
import threading
import time
from typing import Iterable
from urllib.parse import urlsplit
import uuid


PI_FLAGS = ["--mode", "json", "--print", "--no-session", "--no-skills",
            "--no-extensions", "--no-mcp", "--no-prompt-templates",
            "--no-context-files", "--no-themes", "--no-approve", "--offline"]
EMPTY_USAGE = {"input_tokens": None, "output_tokens": None,
               "total_tokens": None, "cost_usd": None}
_ENV_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")
_TOOL_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.+-]*\Z")
_OWNED_NAME = re.compile(r"skillbench-[a-f0-9]{32}\Z")
PI_REQUIRED_TOOLS = ("python3", "pi", "bash", "rg", "fd")

# Executed only inside the container, after its mounts and resource limits exist.
# No credential is serialized into this payload or written to models.json.
_BOOTSTRAP = """import json, os, pathlib, sys
os.umask(0o077)
payload = json.loads(sys.argv[1])
agent = pathlib.Path('/home/worker/.pi/agent')
agent.mkdir(parents=True, exist_ok=True)
(agent / 'settings.json').write_text(json.dumps(payload['settings']), encoding='utf-8')
if payload['models']:
    (agent / 'models.json').write_text(json.dumps(payload['models']), encoding='utf-8')
os.execvp('pi', ['pi', *payload['argv']])
"""

_INVENTORY = """import json, os, pathlib, shutil, subprocess, sys
tools = json.loads(sys.argv[1])
def command(args):
    p = subprocess.run(args, capture_output=True, text=True, timeout=15)
    return {'returncode': p.returncode, 'stdout': p.stdout[:80000], 'stderr': p.stderr[:2000]}
def resolve_tool(name):
    return shutil.which(name) or (shutil.which('fdfind') if name == 'fd' else None)
result = {'uid': os.getuid(), 'tools': {name: resolve_tool(name) for name in tools},
          'os_release': pathlib.Path('/etc/os-release').read_text()[:8000],
          'pi_version': command(['pi', '--version']),
          'pi_help': command(['pi', '--help'])}
print(json.dumps(result))
"""


def _number(value):
    return (value if isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(value) and value >= 0 else None)


def _message_key(message: dict):
    """Only stable identities justify dropping repeated finalized messages."""
    if message.get("id"):
        return ("id", str(message["id"]))
    if message.get("timestamp") is not None:
        return ("timestamp", hashlib.sha256(json.dumps(message, sort_keys=True,
                separators=(",", ":")).encode()).hexdigest())
    return None


def parse_events(records: Iterable[dict]) -> dict:
    """Parse Pi JSON events without adding delta/turn/agent copies of usage.

    Prefer message_end, then turn_end, then agent_end for older event streams.
    Repeated text without a message identity is not assumed to be a duplicate.
    An all-zero/missing usage object is unknown, and incomplete aggregate fields
    remain None. Pi's zero-priced custom model metadata does not establish free
    requests, so zero reported dollar cost also remains unknown.
    """
    ends, turns, agents, auxiliary = [], [], [], []
    calls, reads, unkeyed_calls = {}, [], 0
    malformed = 0
    settled = False
    for record in records:
        if not isinstance(record, dict):
            malformed += 1
            continue
        kind = record.get("type")
        message = record.get("message")
        if kind in ("message_end", "turn_end") and isinstance(message, dict):
            if message.get("role") == "assistant":
                (ends if kind == "message_end" else turns).append(message)
        elif kind == "agent_end" and isinstance(record.get("messages"), list):
            agents.extend(m for m in record["messages"]
                          if isinstance(m, dict) and m.get("role") == "assistant")
        elif kind == "compaction_end" and isinstance(record.get("result"), dict):
            if record["result"].get("usage"):
                auxiliary.append({"usage": record["result"]["usage"]})
        elif kind == "agent_settled":
            settled = True
        if kind in ("tool_execution_start", "tool_execution_end"):
            identity = record.get("toolCallId")
            if identity:
                previous = calls.setdefault(str(identity), {})
                previous.update({k: v for k, v in record.items() if v is not None})
            elif kind == "tool_execution_start":
                unkeyed_calls += 1

    messages, seen = [], set()
    source = "message_end" if ends else "turn_end" if turns else "agent_end"
    for message in ends or turns or agents:
        key = _message_key(message)
        if key is not None and key in seen:
            continue
        if key is not None:
            seen.add(key)
        messages.append(message)
    # Older streams may expose calls in assistant content without lifecycle events.
    for message in messages:
        for item in message.get("content", []) if isinstance(message.get("content"), list) else []:
            if isinstance(item, dict) and item.get("type") in ("toolCall", "tool_call") and item.get("id"):
                calls.setdefault(str(item["id"]), {"toolName": item.get("name"),
                                                   "args": item.get("arguments", {})})
    for call in calls.values():
        args = call.get("args", {})
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except ValueError:
                args = {}
        if call.get("toolName") == "read" and isinstance(args, dict):
            path = args.get("path", args.get("file_path"))
            if isinstance(path, str) and (path == "/skills" or path.startswith("/skills/")):
                reads.append({"path": path, "offset": args.get("offset"), "limit": args.get("limit"),
                              "is_error": call.get("isError")})

    usage_rows = []
    for message in [*messages, *auxiliary]:
        raw = message.get("usage")
        row = dict(EMPTY_USAGE)
        if isinstance(raw, dict):
            row.update({"input_tokens": _number(raw.get("input", raw.get("input_tokens"))),
                        "output_tokens": _number(raw.get("output", raw.get("output_tokens"))),
                        "total_tokens": _number(raw.get("totalTokens", raw.get("total_tokens")))})
            cost = raw.get("cost")
            candidate = _number(cost.get("total")) if isinstance(cost, dict) else _number(raw.get("cost_usd"))
            row["cost_usd"] = candidate if candidate is not None and candidate > 0 else None
            if not any(row[k] is not None and row[k] > 0 for k in EMPTY_USAGE):
                row = dict(EMPTY_USAGE)
        usage_rows.append(row)
    usage = {key: (sum(row[key] for row in usage_rows)
                   if usage_rows and all(row[key] is not None for row in usage_rows) else None)
             for key in EMPTY_USAGE}
    last = messages[-1] if messages else {}
    final_text = "\n".join(item.get("text", "") for item in last.get("content", [])
                           if isinstance(item, dict) and item.get("type") == "text") if isinstance(last.get("content"), list) else ""
    return {"usage": usage, "model_ids": sorted({str(m["model"]) for m in messages if m.get("model")}),
            "provider_ids": sorted({str(m["provider"]) for m in messages if m.get("provider")}),
            "model_calls": len(messages), "tool_calls": len(calls) + unkeyed_calls,
            "skill_reads": reads, "final_text": final_text, "stop_reason": last.get("stopReason"),
            "agent_settled": settled, "usage_source": source if messages else None,
            "auxiliary_usage_records": len(auxiliary), "malformed_events": malformed}


def _settings_payload(config: dict, skill_names: list[str]) -> dict:
    provider, model = str(config.get("provider", "zai")), str(config.get("model", ""))
    if not _TOOL_NAME.fullmatch(provider) or not model or model.startswith("-") or any(ord(c) < 32 for c in model):
        raise ValueError("provider and exact model must be configured")
    key_name = str(config.get("api_key_env", "ZAI_API_KEY"))
    if not _ENV_NAME.fullmatch(key_name):
        raise ValueError("api_key_env must be an environment variable name")
    thinking = config.get("thinking", "medium")
    if thinking not in ("off", "minimal", "low", "medium", "high", "xhigh", "max"):
        raise ValueError("unsupported thinking level")
    settings = {"defaultProvider": provider, "defaultModel": model, "defaultThinkingLevel": thinking,
                "enableInstallTelemetry": False, "enableAnalytics": False,
                "cacheWarming": "off", "retry": {"enabled": False, "provider": {"maxRetries": 0}},
                "compaction": {"enabled": False}}
    models = None
    base_url = config.get("base_url")
    if base_url:
        parsed = urlsplit(str(base_url))
        if parsed.scheme not in ("https", "http") or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError("base_url must be an HTTP(S) endpoint without embedded credentials")
        model_config = {"id": model, "name": model, "reasoning": bool(config.get("reasoning", True)),
                        "input": ["text"], "contextWindow": int(config.get("context_window", 131072)),
                        "maxTokens": int(config.get("max_tokens", 8192))}
        if model_config["contextWindow"] <= 0 or model_config["maxTokens"] <= 0:
            raise ValueError("model token limits must be positive")
        sampling = {key: config[key] for key in ("temperature", "top_p") if key in config}
        if sampling:
            if any(_number(v) is None for v in sampling.values()):
                raise ValueError("sampling values must be finite nonnegative numbers")
            model_config["samplingParams"] = sampling
        models = {"providers": {provider: {"baseUrl": base_url,
                    "api": config.get("api", "openai-completions"),
                    "apiKey": "${" + key_name + "}", "models": [model_config]}}}
    elif any(key in config for key in ("temperature", "top_p", "context_window", "max_tokens", "reasoning")):
        raise ValueError("explicit model metadata/sampling requires base_url")
    argv = [*PI_FLAGS, "--provider", provider, "--model", model, "--thinking", thinking,
            "--tools", "read,write,edit,bash,grep,find,ls"]
    for name in skill_names:
        argv.extend(["--skill", "/skills/" + name])
    return {"settings": settings, "models": models, "argv": argv}


def _identity(config: dict) -> tuple[int, int]:
    uid = int(config.get("uid", os.getuid() if hasattr(os, "getuid") else 1000))
    gid = int(config.get("gid", os.getgid() if hasattr(os, "getgid") else 1000))
    if uid <= 0 or gid < 0:
        raise ValueError("worker uid must be nonroot; use an unprivileged invoking account or explicit uid/gid")
    return uid, gid


def _docker_base(config: dict, name: str, *, offline: bool = False, entrypoint: str = "python3") -> list[str]:
    image = str(config.get("image", ""))
    if not image or image.startswith("-") or any(c.isspace() for c in image):
        raise ValueError("a prebuilt Docker image is required")
    uid, gid = _identity(config)
    cpus = float(config.get("cpus", 1))
    pids = int(config.get("pids_limit", 128))
    memory = str(config.get("memory", "1g"))
    if not math.isfinite(cpus) or cpus <= 0 or pids <= 0 or not re.fullmatch(r"[1-9][0-9]*[bkmgBKMG]?", memory):
        raise ValueError("cpus, pids_limit and memory must specify positive bounds")
    network = "none" if offline else str(config.get("network", "bridge"))
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", network) or network == "host":
        raise ValueError("network must be none, bridge, or a dedicated Docker network; host sharing is forbidden")
    return [str(config.get("docker_binary", "docker")), "run", "--rm", "--pull", "never", "-i",
            "--name", name, "--label", "skillbench.owner=skillbench", "--user", f"{uid}:{gid}",
            "--cap-drop", "ALL", "--security-opt", "no-new-privileges", "--pids-limit", str(pids),
            "--memory", memory, "--memory-swap", memory, "--cpus", str(cpus), "--read-only",
            "--network", network, "--log-driver", "none", "--init", "--workdir", "/workspace",
            "--tmpfs", "/tmp:rw,nosuid,nodev,mode=1777,size=128m",
            "--tmpfs", f"/home/worker:rw,nosuid,nodev,mode=700,uid={uid},gid={gid},size=64m",
            "--env", "HOME=/home/worker", "--env", "PI_CODING_AGENT_DIR=/home/worker/.pi/agent",
            "--env", "PI_OFFLINE=1", "--env", "PI_SKIP_VERSION_CHECK=1", "--env", "NO_COLOR=1",
            "--env", "LANG=C.UTF-8", "--entrypoint", entrypoint]


def _cleanup(docker: str, name: str) -> list[str]:
    errors = []
    for operation in (["kill", name], ["rm", "--force", name]):
        try:
            result = subprocess.run([docker, *operation], capture_output=True, timeout=5, check=False)
            stderr = result.stderr.decode("utf-8", errors="replace") if isinstance(result.stderr, bytes) else str(result.stderr)
            if result.returncode and "No such container" not in stderr and "is not running" not in stderr:
                errors.append(f"docker {operation[0]} failed: {stderr[:500]}")
        except (OSError, subprocess.TimeoutExpired) as exc:
            errors.append(f"docker {operation[0]} cleanup failed: {type(exc).__name__}")
    return errors


def _capture(argv: list[str], env: dict, prompt: bytes, timeout: float, cap: int,
             stdout_path: Path, stderr_path: Path, docker: str, name: str) -> dict:
    """Consume both pipes continuously and bound their combined retained bytes."""
    started = time.monotonic()
    process = None
    threads = []
    total = 0
    lock = threading.Lock()
    overflow = threading.Event()
    read_errors = []
    status, error, cleanup_errors = "completed", None, []
    cleanup_done = False
    try:
        with stdout_path.open("wb") as stdout_file, stderr_path.open("wb") as stderr_file:
            process = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, env=env, shell=False)

            def consume(pipe, target):
                nonlocal total
                try:
                    while True:
                        chunk = pipe.read1(65536)
                        if not chunk:
                            break
                        with lock:
                            keep = min(len(chunk), max(0, cap - total))
                            total += keep
                            if keep < len(chunk):
                                overflow.set()
                        if keep:
                            target.write(chunk[:keep])
                except (OSError, ValueError) as exc:
                    read_errors.append(type(exc).__name__)

            def send_prompt():
                try:
                    process.stdin.write(prompt)
                    process.stdin.close()
                except (OSError, ValueError):
                    pass

            for pipe, target in ((process.stdout, stdout_file), (process.stderr, stderr_file)):
                thread = threading.Thread(target=consume, args=(pipe, target), daemon=True)
                thread.start()
                threads.append(thread)
            writer = threading.Thread(target=send_prompt, daemon=True)
            writer.start()
            while process.poll() is None:
                remaining = timeout - (time.monotonic() - started)
                if overflow.is_set():
                    status, error = "budget_exceeded", "output_limit"
                    break
                if remaining <= 0:
                    status, error = "timeout", "wall_time_limit"
                    break
                overflow.wait(min(0.05, remaining))
            if process.poll() is None:
                cleanup_errors.extend(_cleanup(docker, name))
                cleanup_done = True
                process.terminate()
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=3)
            for thread in threads:
                thread.join(timeout=3)
            writer.join(timeout=1)
            if any(thread.is_alive() for thread in threads):
                status, error = "runner_error", "stream_did_not_close"
            elif overflow.is_set() and status == "completed":
                status, error = "budget_exceeded", "output_limit"
            elif read_errors and status == "completed":
                status, error = "runner_error", "stream_read_error"
    except (OSError, subprocess.TimeoutExpired) as exc:
        status, error = "runner_error", f"process_error:{type(exc).__name__}"
    finally:
        if not cleanup_done:
            cleanup_errors.extend(_cleanup(docker, name))
        if process is not None:
            if process.poll() is None:
                process.kill()
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    cleanup_errors.append("docker client did not stop")
            for pipe in (process.stdin, process.stdout, process.stderr):
                if pipe is not None:
                    pipe.close()
    if cleanup_errors and status == "completed":
        status, error = "runner_error", "container_cleanup_failed"
    return {"status": status, "error": error, "returncode": process.returncode if process else None,
            "elapsed_seconds": round(time.monotonic() - started, 6), "output_bytes": total,
            "cleanup_errors": cleanup_errors, "cleanup_confirmed": not cleanup_errors,
            "container_name": name}


def _write_marker(path: Path, payload: dict) -> None:
    temporary = path.with_suffix(".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    temporary.replace(path)


def cleanup_interrupted(log_dir: Path, config: dict) -> dict:
    """Reap only the owned container recorded durably before this run launched.

    A missing marker means run_worker never reached its launch boundary. A
    malformed marker requires operator attention; it never broadens cleanup.
    """
    path = Path(log_dir) / "runtime.json"
    if not path.exists():
        return {"cleanup_confirmed": True, "errors": [], "container_name": None,
                "reason": "no_launch_record"}
    try:
        marker = json.loads(path.read_text(encoding="utf-8"))
        name = marker.get("container_name")
        if not isinstance(name, str) or not _OWNED_NAME.fullmatch(name):
            raise ValueError("invalid owned container name in runtime marker")
        errors = _cleanup(str(config.get("docker_binary", "docker")), name)
        result = {"cleanup_confirmed": not errors, "errors": errors, "container_name": name}
        _write_marker(path, {**marker, "cleanup_confirmed": not errors,
                             "cleanup_errors": errors, "state": "interrupted_cleaned" if not errors else "cleanup_failed"})
        return result
    except (OSError, ValueError, TypeError, AttributeError) as exc:
        return {"cleanup_confirmed": False, "errors": [str(exc)], "container_name": None}


def _skill_names(directory: Path, config: dict) -> list[str]:
    names = []
    for path in directory.iterdir():
        if path.is_symlink() or not path.is_dir() or not (path / "SKILL.md").is_file():
            raise ValueError("skills_dir must contain only complete skill package directories")
        if any(p.is_symlink() for p in path.rglob("*")):
            raise ValueError("skill snapshots must not contain symlinks")
        names.append(path.name)
    order = config.get("skill_order", sorted(names))
    if not isinstance(order, list) or len(order) != len(names) or set(order) != set(names):
        raise ValueError("skill_order must list every mounted package exactly once")
    return order


def run_worker(workspace: Path, skills_dir: Path, prompt: str, config: dict, log_dir: Path) -> dict:
    """Run exactly one disposable Docker worker and retain bounded raw output."""
    result = {"status": "runner_error", "returncode": None, "elapsed_seconds": 0,
              "usage": dict(EMPTY_USAGE), "model_ids": [], "tool_calls": 0, "skill_reads": [],
              "error": None, "cleanup_confirmed": True}
    try:
        workspace, skills_dir, log_dir = Path(workspace).resolve(), Path(skills_dir).resolve(), Path(log_dir).resolve()
        if not workspace.is_dir() or not skills_dir.is_dir():
            raise ValueError("workspace and skills_dir must be existing disposable directories")
        if workspace == skills_dir or workspace in skills_dir.parents or skills_dir in workspace.parents:
            raise ValueError("workspace and skills_dir must be disjoint")
        if log_dir == workspace or workspace in log_dir.parents or log_dir == skills_dir or skills_dir in log_dir.parents:
            raise ValueError("logs must remain outside worker mounts")
        if any("," in str(path) or "\n" in str(path) for path in (workspace, skills_dir)):
            raise ValueError("Docker mount paths cannot contain commas or newlines")
        names = _skill_names(skills_dir, config)
        payload = _settings_payload(config, names)
        timeout, cap = float(config.get("timeout_seconds", 180)), int(config.get("max_output_bytes", 8 * 1024 * 1024))
        if not math.isfinite(timeout) or timeout <= 0 or cap <= 0:
            raise ValueError("timeout_seconds and max_output_bytes must be positive")
        if not isinstance(prompt, str) or not prompt.strip() or len(prompt.encode()) > 1024 * 1024:
            raise ValueError("prompt must be nonempty and at most 1 MiB")
        key_name = str(config.get("api_key_env", "ZAI_API_KEY"))
        if not os.environ.get(key_name):
            raise ValueError(f"required API credential environment variable is unset: {key_name}")
        name = "skillbench-" + uuid.uuid4().hex
        argv = _docker_base(config, name)
        argv += ["--mount", f"type=bind,source={workspace},target=/workspace",
                 "--mount", f"type=bind,source={skills_dir},target=/skills,readonly",
                 "--env", key_name, str(config["image"]), "-c", _BOOTSTRAP, json.dumps(payload)]
        log_dir.mkdir(parents=True, exist_ok=True)
        stdout_path, stderr_path = log_dir / "events.jsonl", log_dir / "stderr.log"
        _write_marker(log_dir / "runtime.json", {"container_name": name, "state": "launching",
                                                "cleanup_confirmed": False})
        result.update(_capture(argv, dict(os.environ), prompt.encode(), timeout, cap,
                               stdout_path, stderr_path, argv[0], name))
        _write_marker(log_dir / "runtime.json", {"container_name": name, "state": result["status"],
                     "cleanup_confirmed": result["cleanup_confirmed"],
                     "cleanup_errors": result.get("cleanup_errors", [])})
        records, bad_lines = [], 0
        for line in stdout_path.read_text(encoding="utf-8", errors="replace").split("\n"):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except ValueError:
                bad_lines += 1
        result.update(parse_events(records))
        result["malformed_events"] += bad_lines
        result.update({"events_path": str(stdout_path), "stderr_path": str(stderr_path)})
        if result["status"] == "completed":
            if result["returncode"] == 137:
                result.update(status="budget_exceeded", error="worker_killed")
            elif result["returncode"] != 0:
                result.update(status="runner_error", error="worker_process_failed")
            elif not result["model_calls"]:
                result.update(status="runner_error", error="missing_finalized_assistant_message")
            elif bad_lines:
                result.update(status="runner_error", error="malformed_event_stream")
            elif result["model_ids"] and any(model != str(config["model"]) for model in result["model_ids"]):
                result.update(status="runner_error", error="model_mismatch")
            elif result["stop_reason"] in ("error", "aborted"):
                result.update(status="runner_error", error="provider_or_agent_error")
            elif result["stop_reason"] == "length":
                result.update(status="budget_exceeded", error="model_output_limit")
        return result
    except (OSError, ValueError, TypeError) as exc:
        result["error"] = f"invalid_runtime:{exc}"
        return result


def run_reference(workspace: Path, script: str, config: dict, log_dir: Path) -> dict:
    """Execute an evaluator-authored reference in the image, without a model/key.

    Only /workspace is mounted, and networking is disabled. This validates a
    reference procedure; the outside grader still checks its artifact/state.
    """
    result = {"status": "runner_error", "returncode": None, "elapsed_seconds": 0,
              "usage": {key: 0 for key in EMPTY_USAGE}, "model_ids": [], "model_calls": 0,
              "tool_calls": 0, "skill_reads": [], "error": None, "cleanup_confirmed": True}
    try:
        workspace, log_dir = Path(workspace).resolve(), Path(log_dir).resolve()
        if not workspace.is_dir():
            raise ValueError("reference workspace must be an existing disposable directory")
        if log_dir == workspace or workspace in log_dir.parents:
            raise ValueError("logs must remain outside worker mounts")
        if "," in str(workspace) or "\n" in str(workspace):
            raise ValueError("Docker mount paths cannot contain commas or newlines")
        if not isinstance(script, str) or not script.strip() or len(script.encode()) > 1024 * 1024:
            raise ValueError("reference script must be nonempty and at most 1 MiB")
        timeout, cap = float(config.get("timeout_seconds", 180)), int(config.get("max_output_bytes", 8 * 1024 * 1024))
        if not math.isfinite(timeout) or timeout <= 0 or cap <= 0:
            raise ValueError("timeout_seconds and max_output_bytes must be positive")
        name = "skillbench-" + uuid.uuid4().hex
        argv = _docker_base(config, name, offline=True, entrypoint="bash")
        argv += ["--mount", f"type=bind,source={workspace},target=/workspace",
                 str(config["image"]), "-c", script]
        log_dir.mkdir(parents=True, exist_ok=True)
        stdout_path, stderr_path = log_dir / "stdout.log", log_dir / "stderr.log"
        _write_marker(log_dir / "runtime.json", {"container_name": name, "state": "launching",
                                                "kind": "reference", "cleanup_confirmed": False})
        result.update(_capture(argv, dict(os.environ), b"", timeout, cap, stdout_path, stderr_path, argv[0], name))
        if result["status"] == "completed":
            if result["returncode"] == 137:
                result.update(status="budget_exceeded", error="reference_killed")
            elif result["returncode"] != 0:
                result.update(status="runner_error", error="reference_process_failed")
        _write_marker(log_dir / "runtime.json", {"container_name": name, "state": result["status"],
                     "kind": "reference", "cleanup_confirmed": result["cleanup_confirmed"],
                     "cleanup_errors": result.get("cleanup_errors", [])})
        result.update({"stdout_path": str(stdout_path), "stderr_path": str(stderr_path)})
        return result
    except (OSError, ValueError, TypeError) as exc:
        result["error"] = f"invalid_runtime:{exc}"
        return result


def preflight(config: dict) -> dict:
    """Offline Docker/image/Pi checks; never contact a model provider."""
    report = {"ok": False, "errors": [], "image_id": None}
    docker = str(config.get("docker_binary", "docker"))
    try:
        _settings_payload(config, [])
        name = "skillbench-preflight-" + uuid.uuid4().hex
        argv = _docker_base(config, name, offline=True)
        tools = config.get("required_tools", [])
        if not isinstance(tools, list) or any(not isinstance(tool, str) or not _TOOL_NAME.fullmatch(tool) for tool in tools):
            raise ValueError("required_tools must be executable names")
        info = subprocess.run([docker, "info", "--format", "{{.OSType}}"], capture_output=True, text=True, timeout=15)
        if info.returncode or info.stdout.strip() != "linux":
            raise ValueError("Docker must be reachable and use Linux containers")
        inspect = subprocess.run([docker, "image", "inspect", "--format", "{{.Id}}", str(config["image"])],
                                 capture_output=True, text=True, timeout=15)
        if inspect.returncode or not re.fullmatch(r"sha256:[a-f0-9]{64}", inspect.stdout.strip()):
            raise ValueError("configured image is not present locally; build or pull it before running")
        report["image_id"] = inspect.stdout.strip()
        required = sorted(set([*PI_REQUIRED_TOOLS, *tools]))
        argv += [report["image_id"], "-c", _INVENTORY, json.dumps(required)]
        with tempfile.TemporaryDirectory(prefix="skillbench-preflight-") as directory:
            out, err = Path(directory) / "stdout", Path(directory) / "stderr"
            outcome = _capture(argv, dict(os.environ), b"", 45, 256 * 1024, out, err, docker, name)
            if outcome["status"] != "completed" or outcome["returncode"] != 0:
                raise ValueError("image inventory failed: " + str(outcome["error"] or "nonzero exit")
                                 + "; " + err.read_text(errors="replace")[:1000])
            inventory = json.loads(out.read_text())
        report["inventory"] = inventory
        if inventory["uid"] == 0:
            report["errors"].append("image probe unexpectedly ran as root")
        missing = [name for name in required if not inventory["tools"].get(name)]
        if missing:
            report["errors"].append("missing image tools: " + ", ".join(missing))
        help_result, version_result = inventory["pi_help"], inventory["pi_version"]
        if help_result["returncode"] or version_result["returncode"]:
            report["errors"].append("Pi help/version probe failed")
        version = version_result["stdout"].strip()
        report["pi_version"] = version
        expected = str(config.get("pi_version", "1.3.0"))
        if not re.search(r"(?<![0-9.])" + re.escape(expected) + r"(?![0-9.])", version):
            report["errors"].append(f"Pi version mismatch: expected {expected}, observed {version}")
        missing_flags = [flag for flag in PI_FLAGS if flag.startswith("--") and flag not in help_result["stdout"]]
        if missing_flags:
            report["errors"].append("Pi is missing required flags: " + ", ".join(missing_flags))
        report["api_key_present"] = bool(os.environ.get(str(config.get("api_key_env", "ZAI_API_KEY"))))
        report["ok"] = not report["errors"]
    except (OSError, ValueError, TypeError, KeyError, subprocess.TimeoutExpired) as exc:
        report["errors"].append(str(exc))
    return report
