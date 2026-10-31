"""Runtime tests use owned Python subprocesses or mocked Docker, never an API."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

from skillbench import runtime


def assistant(text="done", stamp=1, **changes):
    result = {"role": "assistant", "timestamp": stamp, "model": "fixture-model", "provider": "zai",
              "content": [{"type": "text", "text": text}], "stopReason": "stop",
              "usage": {"input": 100, "output": 20, "totalTokens": 120,
                        "cost": {"total": 0.003}}}
    result.update(changes)
    return result


class EventTests(unittest.TestCase):
    def test_finalized_usage_not_streamed_and_repeated_copies(self):
        first, second = assistant(), assistant("more", stamp=2)
        records = [{"type": "message_update", "usage": {"input": 9999, "output": 9999}},
                   {"type": "message_end", "message": first},
                   {"type": "turn_end", "message": first},
                   {"type": "agent_end", "messages": [first]},
                   {"type": "message_end", "message": first},
                   {"type": "message_end", "message": second},
                   {"type": "agent_end", "messages": [second]},
                   {"type": "agent_settled"}]
        result = runtime.parse_events(records)
        self.assertEqual(result["model_calls"], 2)
        self.assertEqual(result["usage"]["total_tokens"], 240)
        self.assertEqual(result["usage"]["cost_usd"], 0.006)
        self.assertEqual(result["final_text"], "more")
        self.assertTrue(result["agent_settled"])

    def test_older_turn_and_agent_fallbacks(self):
        message = assistant()
        for record in ({"type": "turn_end", "message": message},
                       {"type": "agent_end", "messages": [message, message]}):
            result = runtime.parse_events([record])
            self.assertEqual(result["model_calls"], 1)
            self.assertEqual(result["usage"]["input_tokens"], 100)

    def test_identical_text_is_not_always_a_duplicate(self):
        first, second = assistant(stamp=1), assistant(stamp=2)
        result = runtime.parse_events([{"type": "message_end", "message": m} for m in (first, second)])
        self.assertEqual(result["model_calls"], 2)

    def test_unknown_usage_is_not_zero_or_partial_total(self):
        for usage in (None, {}, {"input": 0, "output": 0, "totalTokens": 0, "cost": {"total": 0}}):
            result = runtime.parse_events([{"type": "message_end", "message": assistant(usage=usage)}])
            self.assertEqual(result["usage"], runtime.EMPTY_USAGE)
        result = runtime.parse_events([{"type": "message_end", "message": assistant()},
                                       {"type": "message_end", "message": assistant(stamp=2, usage={"output": 4})}])
        self.assertIsNone(result["usage"]["input_tokens"])
        self.assertIsNone(result["usage"]["total_tokens"])
        self.assertEqual(result["usage"]["output_tokens"], 24)

    def test_zero_cost_metadata_and_invalid_counts_are_unknown(self):
        result = runtime.parse_events([{"type": "message_end", "message": assistant(
            usage={"input": 10, "output": -2, "totalTokens": float("nan"), "cost": {"total": 0}})}])
        self.assertEqual(result["usage"]["input_tokens"], 10)
        self.assertIsNone(result["usage"]["output_tokens"])
        self.assertIsNone(result["usage"]["total_tokens"])
        self.assertIsNone(result["usage"]["cost_usd"])

    def test_tool_lifecycles_are_deduplicated_and_reads_observed(self):
        records = [{"type": "tool_execution_start", "toolCallId": "a", "toolName": "read",
                    "args": {"path": "/skills/jq/SKILL.md", "offset": 1, "limit": 50}},
                   {"type": "tool_execution_end", "toolCallId": "a", "toolName": "read", "isError": False},
                   {"type": "tool_execution_start", "toolCallId": "b", "toolName": "bash",
                    "args": {"command": "cat /skills/jq/SKILL.md"}},
                   {"type": "tool_execution_start", "toolCallId": "c", "toolName": "read",
                    "args": {"path": "/workspace/input.json"}}]
        result = runtime.parse_events(records)
        self.assertEqual(result["tool_calls"], 3)
        self.assertEqual(result["skill_reads"], [{"path": "/skills/jq/SKILL.md", "offset": 1,
                                                   "limit": 50, "is_error": False}])

    def test_compaction_cost_is_included_when_exposed(self):
        result = runtime.parse_events([{"type": "message_end", "message": assistant()},
            {"type": "compaction_end", "result": {"usage": {"input": 10, "output": 2,
                                                               "totalTokens": 12, "cost": {"total": 0.001}}}}])
        self.assertEqual(result["usage"]["total_tokens"], 132)
        self.assertEqual(result["auxiliary_usage_records"], 1)


class LaunchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.workspace, self.skills, self.logs = (self.root / n for n in ("workspace", "skills", "logs"))
        self.workspace.mkdir()
        self.skills.mkdir()
        for name in ("jq", "tar"):
            (self.skills / name).mkdir()
            (self.skills / name / "SKILL.md").write_text("fixture", encoding="utf-8")
        self.config = {"image": "fixture-image", "model": "fixture-model", "uid": 1000, "gid": 1000}

    def fake_capture(self, argv, env, prompt, timeout, cap, stdout_path, stderr_path, docker, name):
        self.launch = (argv, env, prompt)
        stdout_path.write_text(json.dumps({"type": "message_end", "message": assistant()}) + "\n", encoding="utf-8")
        stderr_path.write_text("", encoding="utf-8")
        marker = json.loads((stdout_path.parent / "runtime.json").read_text())
        self.assertEqual(marker["state"], "launching")
        self.assertFalse(marker["cleanup_confirmed"])
        return {"status": "completed", "returncode": 0, "elapsed_seconds": 1, "error": None,
                "cleanup_confirmed": True}

    def test_docker_boundary_order_and_key_not_in_argv(self):
        self.config["skill_order"] = ["tar", "jq"]
        with patch.dict(os.environ, {"ZAI_API_KEY": "private-fixture-key"}), patch.object(runtime, "_capture", self.fake_capture):
            result = runtime.run_worker(self.workspace, self.skills, "@literal task", self.config, self.logs)
        self.assertEqual(result["status"], "completed")
        argv, env, prompt = self.launch
        self.assertNotIn("private-fixture-key", json.dumps(argv))
        self.assertEqual(env["ZAI_API_KEY"], "private-fixture-key")
        self.assertEqual(prompt, b"@literal task")
        self.assertEqual(argv.count("--mount"), 2)
        self.assertIn(f"type=bind,source={self.skills.resolve()},target=/skills,readonly", argv)
        self.assertIn(f"type=bind,source={self.workspace.resolve()},target=/workspace", argv)
        self.assertNotIn(str(self.logs), " ".join(argv))
        for flag in ("--read-only", "--cap-drop", "--pids-limit", "--memory", "--cpus", "--security-opt"):
            self.assertIn(flag, argv)
        payload = json.loads(argv[-1])
        pi = payload["argv"]
        self.assertEqual([pi[i + 1] for i, arg in enumerate(pi) if arg == "--skill"], ["/skills/tar", "/skills/jq"])
        for flag in runtime.PI_FLAGS:
            self.assertIn(flag, pi)
        self.assertFalse(payload["settings"]["retry"]["enabled"])
        self.assertFalse(payload["settings"]["compaction"]["enabled"])

    def test_custom_provider_serializes_reference_not_credential(self):
        config = {**self.config, "base_url": "https://example.invalid/v1", "temperature": 0.3}
        payload = runtime._settings_payload(config, [])
        provider = payload["models"]["providers"]["zai"]
        self.assertEqual(provider["apiKey"], "${ZAI_API_KEY}")
        self.assertEqual(provider["models"][0]["id"], "fixture-model")
        self.assertEqual(provider["models"][0]["samplingParams"], {"temperature": 0.3})

    def test_root_host_network_missing_key_and_bad_order_rejected(self):
        with patch.object(runtime, "_capture") as execute:
            for changes in ({"uid": 0}, {"network": "host"}, {"network": "container:other"}, {"skill_order": ["jq"]}):
                with patch.dict(os.environ, {"ZAI_API_KEY": "private-fixture-key"}):
                    result = runtime.run_worker(self.workspace, self.skills, "test", {**self.config, **changes}, self.logs)
                self.assertEqual(result["status"], "runner_error")
            with patch.dict(os.environ, {}, clear=True):
                result = runtime.run_worker(self.workspace, self.skills, "test", self.config, self.logs)
                self.assertIn("unset", result["error"])
            execute.assert_not_called()

    def test_logs_cannot_be_exposed_to_worker(self):
        result = runtime.run_worker(self.workspace, self.skills, "test", self.config, self.workspace / "logs")
        self.assertEqual(result["status"], "runner_error")
        self.assertIn("outside worker mounts", result["error"])

    def test_model_mismatch_is_not_a_completed_comparison(self):
        with patch.dict(os.environ, {"ZAI_API_KEY": "private-fixture-key"}), patch.object(runtime, "_capture", self.fake_capture):
            result = runtime.run_worker(self.workspace, self.skills, "test", {**self.config, "model": "different"}, self.logs)
        self.assertEqual(result["error"], "model_mismatch")

    def test_length_stop_is_a_worker_budget_failure(self):
        def capture(*args):
            result = self.fake_capture(*args)
            args[5].write_text(json.dumps({"type": "message_end", "message": assistant(stopReason="length")}) + "\n")
            return result
        with patch.dict(os.environ, {"ZAI_API_KEY": "private-fixture-key"}), patch.object(runtime, "_capture", capture):
            result = runtime.run_worker(self.workspace, self.skills, "test", self.config, self.logs)
        self.assertEqual(result["status"], "budget_exceeded")
        self.assertEqual(result["error"], "model_output_limit")

    def test_reference_has_one_mount_no_api_environment_and_no_network(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(runtime, "_capture", self.fake_capture):
            result = runtime.run_reference(self.workspace, "jq --version", self.config, self.logs)
        self.assertEqual(result["status"], "completed")
        self.assertTrue(result["cleanup_confirmed"])
        self.assertEqual(result["usage"]["cost_usd"], 0)
        argv, _, prompt = self.launch
        self.assertEqual(argv.count("--mount"), 1)
        self.assertEqual(argv[argv.index("--network") + 1], "none")
        self.assertEqual(argv[argv.index("--entrypoint") + 1], "bash")
        self.assertNotIn("ZAI_API_KEY", argv)
        self.assertNotIn("/skills", " ".join(argv))
        self.assertEqual(argv[-2:], ["-c", "jq --version"])
        self.assertEqual(prompt, b"")


class CaptureTests(unittest.TestCase):
    def run_capture(self, script, timeout=2, cap=1024):
        with tempfile.TemporaryDirectory() as directory:
            stdout, stderr = Path(directory) / "events", Path(directory) / "stderr"
            with patch.object(runtime, "_cleanup", return_value=[]) as cleanup:
                result = runtime._capture([sys.executable, "-c", script], dict(os.environ), b"", timeout,
                                          cap, stdout, stderr, "fixture-docker", "owned-container")
            return result, stdout.read_bytes(), stderr.read_bytes(), cleanup.call_args_list

    def test_timeout_cleans_owned_container(self):
        started = time.monotonic()
        result, _, _, cleanup = self.run_capture("import time; time.sleep(20)", timeout=0.15)
        self.assertEqual(result["status"], "timeout")
        self.assertEqual(result["error"], "wall_time_limit")
        self.assertLess(time.monotonic() - started, 5)
        self.assertTrue(cleanup)
        self.assertEqual(cleanup[-1].args, ("fixture-docker", "owned-container"))

    def test_combined_output_cap(self):
        result, stdout, stderr, cleanup = self.run_capture(
            "import os; os.write(1,b'x'*2048); os.write(2,b'y'*2048)", cap=1000)
        self.assertEqual(result["status"], "budget_exceeded")
        self.assertEqual(result["error"], "output_limit")
        self.assertLessEqual(len(stdout) + len(stderr), 1000)
        self.assertTrue(cleanup)
        self.assertTrue(result["cleanup_confirmed"])

    def test_normal_exit_cleans_and_preserves_separate_streams(self):
        result, stdout, stderr, cleanup = self.run_capture("import sys; print('events'); print('warning',file=sys.stderr)")
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["returncode"], 0)
        self.assertIn(b"events", stdout)
        self.assertIn(b"warning", stderr)
        self.assertTrue(cleanup)

    def test_cleanup_targets_name_with_kill_and_force_remove(self):
        done = subprocess.CompletedProcess([], 0, stdout=b"", stderr=b"")
        with patch.object(runtime.subprocess, "run", return_value=done) as execute:
            self.assertEqual(runtime._cleanup("docker", "owned-one"), [])
        self.assertEqual([call.args[0] for call in execute.call_args_list],
                         [["docker", "kill", "owned-one"], ["docker", "rm", "--force", "owned-one"]])


class PreflightTests(unittest.TestCase):
    def test_offline_inventory_image_pin_and_no_provider_call(self):
        image_id = "sha256:" + "a" * 64
        config = {"image": "fixture-image", "model": "fixture-model", "uid": 1000, "required_tools": ["jq"]}
        commands = []

        def control(argv, **kwargs):
            commands.append(argv)
            return subprocess.CompletedProcess(argv, 0, stdout="linux\n" if argv[1] == "info" else image_id + "\n", stderr="")

        def capture(argv, env, prompt, timeout, cap, stdout, stderr, docker, name):
            commands.append(argv)
            stdout.write_text(json.dumps({"uid": 1000, "tools": {name: "/usr/bin/" + name for name in json.loads(argv[-1])},
                "os_release": "Ubuntu", "pi_version": {"returncode": 0, "stdout": "1.3.0\n"},
                "pi_help": {"returncode": 0, "stdout": " ".join(runtime.PI_FLAGS)}}))
            stderr.write_text("")
            return {"status": "completed", "returncode": 0, "error": None}

        with patch.object(runtime.subprocess, "run", side_effect=control), patch.object(runtime, "_capture", side_effect=capture):
            report = runtime.preflight(config)
        self.assertTrue(report["ok"], report)
        self.assertEqual(report["image_id"], image_id)
        probe = commands[-1]
        self.assertEqual(probe[probe.index("--network") + 1], "none")
        self.assertNotIn("ZAI_API_KEY", probe)
        self.assertNotIn("--mount", probe)
        self.assertTrue(set(runtime.PI_REQUIRED_TOOLS).issubset(json.loads(probe[-1])))


class InterruptedTests(unittest.TestCase):
    def test_only_valid_saved_owned_name_can_be_cleaned(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "runtime.json"
            name = "skillbench-" + "a" * 32
            runtime._write_marker(path, {"container_name": name})
            with patch.object(runtime, "_cleanup", return_value=[]) as clean:
                result = runtime.cleanup_interrupted(Path(directory), {})
            clean.assert_called_once_with("docker", name)
            self.assertTrue(result["cleanup_confirmed"])
            runtime._write_marker(path, {"container_name": "important-container"})
            with patch.object(runtime, "_cleanup") as clean:
                result = runtime.cleanup_interrupted(Path(directory), {})
            clean.assert_not_called()
            self.assertFalse(result["cleanup_confirmed"])

    def test_missing_marker_never_runs_broad_cleanup(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(runtime, "_cleanup") as clean:
            result = runtime.cleanup_interrupted(Path(directory), {})
        self.assertTrue(result["cleanup_confirmed"])
        clean.assert_not_called()

    def test_cleanup_failure_is_exposed(self):
        with tempfile.TemporaryDirectory() as directory:
            runtime._write_marker(Path(directory) / "runtime.json", {"container_name": "skillbench-" + "a" * 32})
            with patch.object(runtime, "_cleanup", return_value=["Docker unreachable"]):
                result = runtime.cleanup_interrupted(Path(directory), {})
        self.assertFalse(result["cleanup_confirmed"])
        self.assertEqual(result["errors"], ["Docker unreachable"])


if __name__ == "__main__":
    unittest.main()
