"""No network calls: exercise proposal containment, accounting, and API parsing."""

import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from skillbench import optimizer


SKILL = "---\nname: fixture-tool\ndescription: Inspect fixture files.\n---\nRead the selected task.\n"


class FakeResponse(io.BytesIO):
    def geturl(self):
        return "https://api.z.ai/api/paas/v4/chat/completions"


class OptimizerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "canonical" / "fixture-tool"
        self.source.mkdir(parents=True)
        (self.source / "SKILL.md").write_text(SKILL, encoding="utf-8")
        (self.source / "references").mkdir()
        (self.source / "references" / "inspect.md").write_text("Check the actual bytes.\n", encoding="utf-8")
        (self.source / "scripts").mkdir()
        (self.source / "scripts" / "helper.sh").write_text("echo existing\n", encoding="utf-8")
        self.destination = self.root / "candidates" / "candidate-1"
        self.proposal = {"hypothesis": "Connect the command to evidence.", "changes": [{"path": "SKILL.md", "content": SKILL + "Verify the intended bytes.\n"}]}
        self.config = {"optimizer": {"endpoint": "https://api.z.ai/api/paas/v4/chat/completions", "model": "glm-5.3-flash", "api_key_env": "SKILLBENCH_TEST_KEY", "max_tokens": 4096, "temperature": 0.2, "timeout_seconds": 30}}
        self.environment = patch.dict(os.environ, {"SKILLBENCH_TEST_KEY": "example-private-api-key-1234"})
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def response(self, proposal=None, **overrides):
        document = {"choices": [{"finish_reason": "stop", "message": {"content": json.dumps(proposal or self.proposal)}}], "usage": {"prompt_tokens": 300, "completion_tokens": 120, "total_tokens": 420, "completion_tokens_details": {"reasoning_tokens": 50, "untrusted": "do not retain"}}}
        document.update(overrides)
        return FakeResponse(json.dumps(document).encode())

    def test_apply_copies_complete_package_without_mutating_source(self):
        original = {path.relative_to(self.source): path.read_bytes() for path in self.source.rglob("*") if path.is_file()}
        result = optimizer.apply_proposal(self.source, self.destination, self.proposal)
        self.assertEqual(result["candidate_path"], str(self.destination))
        self.assertEqual((self.destination / "SKILL.md").read_text(), self.proposal["changes"][0]["content"])
        for relative, content in original.items():
            self.assertEqual((self.source / relative).read_bytes(), content)
            if relative != Path("SKILL.md"):
                self.assertEqual((self.destination / relative).read_bytes(), content)
        (self.destination / "scripts" / "helper.sh").write_text("changed")
        self.assertEqual((self.source / "scripts" / "helper.sh").read_bytes(), original[Path("scripts/helper.sh")])
        self.assertFalse(list(self.destination.parent.glob(".skillbench-proposal-*")))

    def test_rejects_escape_glob_helpers_and_new_files(self):
        for path in ("../SKILL.md", "/tmp/file.md", "C:/file.md", "references\\inspect.md", "references/../SKILL.md", "references/*.md", "references/[a].md", "scripts/helper.sh", "README.md", "references/new.md", "references//inspect.md"):
            with self.subTest(path=path):
                proposal = {"hypothesis": "Bad path", "changes": [{"path": path, "content": "content"}]}
                with self.assertRaises(optimizer.OptimizerError):
                    optimizer.apply_proposal(self.source, self.destination, proposal)
                self.assertFalse(self.destination.exists())

    def test_all_changes_validated_before_copying(self):
        self.proposal["changes"].append({"path": "../escape.md", "content": "invalid"})
        with self.assertRaises(optimizer.OptimizerError):
            optimizer.apply_proposal(self.source, self.destination, self.proposal)
        self.assertFalse(self.destination.parent.exists())
        self.assertEqual((self.source / "SKILL.md").read_text(), SKILL)

    def test_name_declaration_must_remain_exact(self):
        for content in (SKILL.replace("fixture-tool", "different"), SKILL.replace("name: fixture-tool", "name:  fixture-tool"), SKILL.replace("name: fixture-tool", "name: fixture-tool\nname: fixture-tool"), "No frontmatter"):
            self.proposal["changes"][0]["content"] = content
            with self.subTest(content=content), self.assertRaises(optimizer.OptimizerError):
                optimizer.apply_proposal(self.source, self.destination, self.proposal)

    def test_existing_destination_and_source_overlap_rejected(self):
        self.destination.mkdir(parents=True)
        for destination in (self.destination, self.source, self.source / "candidate", self.source.parent):
            with self.subTest(destination=destination), self.assertRaises(optimizer.OptimizerError):
                optimizer.apply_proposal(self.source, destination, self.proposal)

    def test_empty_duplicate_and_extra_operation_rejected(self):
        for changes in ([], [self.proposal["changes"][0]] * 2, [{"path": "SKILL.md", "content": ""}], [{"path": "SKILL.md", "content": SKILL, "delete": True}]):
            with self.subTest(changes=changes), self.assertRaises(optimizer.OptimizerError):
                optimizer.apply_proposal(self.source, self.destination, {"hypothesis": "test", "changes": changes})

    def test_symlink_inside_package_rejected(self):
        target = self.root / "outside.md"
        target.write_text("outside")
        link = self.source / "references" / "link.md"
        try:
            link.symlink_to(target)
        except OSError:
            self.skipTest("Host does not permit creating symlinks")
        with self.assertRaises(optimizer.OptimizerError):
            optimizer.apply_proposal(self.source, self.destination, self.proposal)
        self.assertEqual(target.read_text(), "outside")

    def test_candidate_parent_symlink_rejected(self):
        outside = self.root / "outside"
        outside.mkdir()
        link = self.root / "linked-parent"
        try:
            link.symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest("Host does not permit creating symlinks")
        with self.assertRaises(optimizer.OptimizerError):
            optimizer.apply_proposal(self.source, link / "candidate", self.proposal)
        self.assertEqual(list(outside.iterdir()), [])

    def test_source_change_during_copy_leaves_no_candidate(self):
        actual_copy = optimizer.shutil.copytree

        def mutate_source(*args, **kwargs):
            result = actual_copy(*args, **kwargs)
            if Path(args[0]) == self.source:
                (self.source / "SKILL.md").write_text(SKILL + "Concurrent edit")
            return result

        with patch.object(optimizer.shutil, "copytree", side_effect=mutate_source):
            with self.assertRaisesRegex(optimizer.OptimizerError, "changed"):
                optimizer.apply_proposal(self.source, self.destination, self.proposal)
        self.assertFalse(self.destination.exists())
        self.assertEqual(list(self.destination.parent.iterdir()), [])

    def test_prompt_has_complete_resources_and_redacted_bounded_evidence(self):
        content = "Complete resource.\n" * 1000
        (self.source / "references" / "inspect.md").write_text(content, newline="\n")
        evidence = [{"split": "development", "trace": "API_KEY=private-value Bearer another-value " + os.environ["SKILLBENCH_TEST_KEY"], "expected_answer": "hidden answer"}]
        messages = optimizer.build_proposal_prompt(self.source, evidence, self.config)
        payload = json.loads(messages[1]["content"])
        self.assertEqual(payload["resources"]["references/inspect.md"], content)
        serialized = json.dumps(payload)
        for secret in ("private-value", "another-value", os.environ["SKILLBENCH_TEST_KEY"], "hidden answer"):
            self.assertNotIn(secret, serialized)
        self.assertIn("[REDACTED]", serialized)
        large = [{"split": "dev", "trace": "x" * 50000} for _ in range(100)]
        payload = json.loads(optimizer.build_proposal_prompt(self.source, large, self.config)[1]["content"])
        self.assertGreater(payload["evidence_items_omitted"], 0)
        self.assertLessEqual(len(json.dumps(payload["development_evidence"])), optimizer.MAX_EVIDENCE_CHARS)

    def test_protected_evidence_rejected(self):
        for split in ("validation", "test", "holdout", "held_out"):
            with self.subTest(split=split), self.assertRaises(optimizer.OptimizerError):
                optimizer.build_proposal_prompt(self.source, [{"split": split}], self.config)

    def test_documented_auth_variables_are_not_mistaken_for_real_keys(self):
        text = SKILL + "Use Authorization: Bearer $TOKEN.\npassword = pathlib.Path(input).read_bytes()\n"
        (self.source / "SKILL.md").write_text(text, newline="\n")
        payload = json.loads(optimizer.build_proposal_prompt(self.source, [], self.config)[1]["content"])
        self.assertEqual(payload["resources"]["SKILL.md"], text)
        self.proposal["changes"][0]["content"] = text + "Check the result.\n"
        with patch.object(optimizer, "urlopen", return_value=self.response()):
            result = optimizer.propose_candidate(self.source, self.destination, [], self.config)
        self.assertEqual(result["proposal"]["changes"][0]["content"], text + "Check the result.\n")

    def test_selected_resource_is_complete_and_selection_is_enforced(self):
        self.config["optimizer"]["selected_resources"] = []
        payload = json.loads(optimizer.build_proposal_prompt(self.source, [], self.config)[1]["content"])
        self.assertEqual(list(payload["resources"]), ["SKILL.md"])
        self.assertEqual(payload["allowed_paths"], ["SKILL.md"])
        self.proposal["changes"] = [{"path": "references/inspect.md", "content": "Altered"}]
        with patch.object(optimizer, "urlopen", return_value=self.response()):
            with self.assertRaisesRegex(optimizer.OptimizerError, "not supplied"):
                optimizer.propose_candidate(self.source, self.destination, [], self.config)

    def test_valid_api_response_records_generation_usage_and_no_key(self):
        self.config["optimizer"]["reasoning_effort"] = "low"
        with patch.object(optimizer, "urlopen", return_value=self.response()) as mocked:
            result = optimizer.propose_candidate(self.source, self.destination, [{"split": "dev"}], self.config)
        mocked.assert_called_once()
        request = mocked.call_args.args[0]
        payload = json.loads(request.data)
        self.assertEqual(payload["model"], "glm-5.3-flash")
        self.assertEqual(payload["reasoning_effort"], "low")
        self.assertNotIn("thinking", payload)
        self.assertNotIn("tools", payload)
        self.assertEqual(result["generation"]["usage"]["total_tokens"], 420)
        self.assertEqual(result["generation"]["usage"]["completion_tokens_details"], {"reasoning_tokens": 50})
        self.assertIsNone(result["generation"]["cost_usd"])
        self.assertNotIn(os.environ["SKILLBENCH_TEST_KEY"], json.dumps(result))

    def test_large_complete_replacement_is_not_silently_truncated(self):
        self.proposal["changes"][0]["content"] = SKILL + "Useful detail.\n" * 1000
        with patch.object(optimizer, "urlopen", return_value=self.response()):
            optimizer.propose_candidate(self.source, self.destination, [], self.config)
        self.assertEqual((self.destination / "SKILL.md").read_text(), self.proposal["changes"][0]["content"])

    def test_rejected_paid_proposal_retains_usage(self):
        self.proposal["changes"][0]["path"] = "../outside.md"
        with patch.object(optimizer, "urlopen", return_value=self.response()):
            with self.assertRaises(optimizer.OptimizerError) as caught:
                optimizer.propose_candidate(self.source, self.destination, [], self.config)
        self.assertEqual(caught.exception.generation["usage"]["total_tokens"], 420)
        self.assertFalse(self.destination.exists())
        self.assertEqual(caught.exception.generation["proposed_paths"], ["../outside.md"])

    def test_truncated_response_rejected_even_when_json_is_parseable(self):
        response = self.response()
        document = json.loads(response.getvalue())
        document["choices"][0]["finish_reason"] = "length"
        with patch.object(optimizer, "urlopen", return_value=FakeResponse(json.dumps(document).encode())):
            with self.assertRaisesRegex(optimizer.OptimizerError, "complete response"):
                optimizer.propose_candidate(self.source, self.destination, [], self.config)

    def test_malformed_and_oversized_responses_are_rejected(self):
        for raw in (b"not json", b"[]", b"x" * (optimizer.MAX_RESPONSE_BYTES + 1)):
            with self.subTest(size=len(raw)), patch.object(optimizer, "urlopen", return_value=FakeResponse(raw)):
                with self.assertRaises(optimizer.OptimizerError):
                    optimizer.propose_candidate(self.source, self.destination, [], self.config)
        self.assertFalse(self.destination.exists())

    def test_api_key_echo_is_not_written(self):
        self.proposal["hypothesis"] = os.environ["SKILLBENCH_TEST_KEY"]
        with patch.object(optimizer, "urlopen", return_value=self.response()):
            with self.assertRaisesRegex(optimizer.OptimizerError, "credentials"):
                optimizer.propose_candidate(self.source, self.destination, [], self.config)
        self.assertFalse(self.destination.exists())

    def test_http_and_transport_errors_are_sanitized_without_retry(self):
        for error in (HTTPError("https://example.test", 401, "SECRET ERROR", {}, None), URLError("SECRET ERROR")):
            with self.subTest(error=type(error)), patch.object(optimizer, "urlopen", side_effect=error) as mocked:
                with self.assertRaises(optimizer.OptimizerError) as caught:
                    optimizer.propose_candidate(self.source, self.destination, [], self.config)
                self.assertNotIn("SECRET ERROR", str(caught.exception))
                self.assertEqual(caught.exception.generation["request_count"], 1)
                mocked.assert_called_once()

    def test_redirect_is_refused_before_followup_request(self):
        with self.assertRaisesRegex(optimizer.OptimizerError, "redirects"):
            optimizer._NoRedirect().redirect_request(None, None, 302, "Found", {}, "https://other.test")

    def test_limits_and_endpoint_checked_before_request(self):
        variants = (("max_tokens", 0), ("max_tokens", optimizer.MAX_OUTPUT_TOKENS + 1), ("temperature", float("nan")), ("timeout_seconds", 0), ("endpoint", "http://api.z.ai/chat/completions"), ("endpoint", "https://user:key@api.z.ai/chat/completions"), ("endpoint", "https://api.z.ai/chat/completions?key=secret"), ("reasoning_effort", "none"))
        for key, value in variants:
            configuration = {**self.config["optimizer"], key: value}
            with self.subTest(key=key, value=value), patch.object(optimizer, "urlopen") as mocked:
                with self.assertRaises(optimizer.OptimizerError):
                    optimizer.propose_candidate(self.source, self.destination, [], configuration)
                mocked.assert_not_called()


if __name__ == "__main__":
    unittest.main()
