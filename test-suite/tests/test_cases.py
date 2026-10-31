"""Fixture/grader tests; these are not Linux CLI or model performance tests."""

import copy
import json
from pathlib import Path
import sqlite3
import tarfile
import tempfile
import unittest

from skillbench.cases import CASES, MAX_ARTIFACT_BYTES


class CaseTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="skillbench-cases-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def fixture(self, case_id, seed=123, solved=False):
        workspace = self.root / f"{case_id}-{seed}"
        case = CASES[case_id]
        oracle = case.prepare(workspace, seed)
        if solved:
            case.solve(workspace, oracle)
        return case, workspace, oracle

    def test_metadata_and_private_oracles_are_serializable(self):
        self.assertEqual(len(CASES), 10)
        for case_id, case in CASES.items():
            with self.subTest(case=case_id):
                self.assertEqual(case.id, case_id)
                self.assertIn(case.split, ("development", "holdout"))
                self.assertIsInstance(case.tools, tuple)
                self.assertEqual(case.tools, (case.skill,))
                self.assertTrue(case.description and case.family and case.prompt())
                _, workspace, oracle = self.fixture(case_id)
                self.assertEqual(json.loads(json.dumps(oracle)), oracle)
                self.assertFalse(case.grade(workspace, oracle)["passed"])

    def test_reference_answers_pass_for_multiple_seeds(self):
        for case_id in CASES:
            for seed in (0, 127, 99991):
                with self.subTest(case=case_id, seed=seed):
                    case, workspace, oracle = self.fixture(case_id, seed, solved=True)
                    report = case.grade(workspace, oracle)
                    self.assertTrue(report["passed"], report)

    def test_same_seed_reproduces_oracle_and_different_seed_changes_inputs(self):
        for case_id, case in CASES.items():
            with self.subTest(case=case_id):
                first = case.prepare(self.root / f"{case_id}-first", 77)
                second = case.prepare(self.root / f"{case_id}-second", 77)
                third = case.prepare(self.root / f"{case_id}-third", 78)
                self.assertEqual(first, second)
                self.assertNotEqual(first["input_snapshot"], third["input_snapshot"])

    def test_preparation_refuses_existing_input(self):
        case, workspace, _ = self.fixture("jq-exact-text")
        with self.assertRaises(FileExistsError):
            case.prepare(workspace, 123)

    def test_input_mutation_and_addition_fail(self):
        for kind in ("mutate", "add"):
            case, workspace, oracle = self.fixture("jq-exact-text", seed=len(kind), solved=True)
            target = workspace / "input" / ("untouched.txt" if kind == "mutate" else "extra.txt")
            target.write_bytes(b"changed")
            report = case.grade(workspace, oracle)
            self.assertFalse(report["passed"])
            self.assertFalse(report["checks"]["inputs_unchanged"])

    def test_wrong_oracle_is_rejected(self):
        case, workspace, oracle = self.fixture("jq-exact-text", solved=True)
        oracle["case_id"] = "other-case"
        self.assertFalse(case.grade(workspace, oracle)["passed"])
        with self.assertRaises(ValueError):
            case.solve(workspace, oracle)

    def test_extra_newline_fails_exact_text(self):
        case, workspace, oracle = self.fixture("jq-exact-text", solved=True)
        output = workspace / "result/extracted.txt"
        output.write_bytes(output.read_bytes() + b"\n")
        self.assertFalse(case.grade(workspace, oracle)["passed"])

    def test_record_type_coercion_and_wrong_count_fail(self):
        case, workspace, oracle = self.fixture("jq-record-filter", solved=True)
        report = workspace / "result/report.json"
        report.write_text(json.dumps({"status": "complete", "selected_count": True}), encoding="utf-8")
        self.assertFalse(case.grade(workspace, oracle)["passed"])

    def test_malformed_input_has_valid_prefix_and_partial_output_is_rejected(self):
        case, workspace, oracle = self.fixture("jq-late-malformed", solved=True)
        lines = (workspace / "input/records.jsonl").read_text(encoding="utf-8").splitlines()
        for line in lines[:-1]:
            self.assertIsInstance(json.loads(line), dict)
        with self.assertRaises(json.JSONDecodeError):
            json.loads(lines[-1])
        (workspace / "result/selected.json").write_text("[]", encoding="utf-8")
        report = case.grade(workspace, oracle)
        self.assertFalse(report["passed"])
        self.assertFalse(report["checks"]["result_file_set"])

    def test_truncated_fixture_preserves_first_member_but_is_not_complete(self):
        case, workspace, oracle = self.fixture("tar-truncated")
        archive = workspace / "input/archive.tar"
        with tarfile.open(archive, mode="r:") as stream:
            member = stream.next()
            content = stream.extractfile(member).read()
            self.assertTrue(content.startswith(b"complete member "))
            with self.assertRaises(tarfile.ReadError):
                stream.getmembers()
        case.solve(workspace, oracle)
        report_path = workspace / "result/report.json"
        report = json.loads(report_path.read_text())
        report["archive_complete"] = True
        report_path.write_text(json.dumps(report), encoding="utf-8")
        self.assertFalse(case.grade(workspace, oracle)["passed"])

    def test_tar_selected_bytes_match_source_members_and_unselected_fails(self):
        case, workspace, oracle = self.fixture("tar-selected-members", solved=True)
        with tarfile.open(workspace / "input/archive.tar", "r:") as archive:
            for name in json.loads((workspace / "input/selection.json").read_text()):
                self.assertEqual(archive.extractfile(name).read(),
                                 (workspace / "result/extracted" / name).read_bytes())
        (workspace / "result/extracted/bundle/unselected.txt").write_bytes(b"extra")
        self.assertFalse(case.grade(workspace, oracle)["passed"])

    def test_sqlite_fixture_rows_match_expected_types(self):
        _, workspace, oracle = self.fixture("sqlite-typed-export")
        connection = sqlite3.connect(workspace / "input/records.db")
        try:
            rows = connection.execute("SELECT id, name, note FROM records WHERE enabled=1 ORDER BY id").fetchall()
        finally:
            connection.close()
        expected = oracle["expected_json"]["result/rows.json"]
        self.assertEqual(rows, [(row["id"], row["name"], row["note"]) for row in expected])
        self.assertTrue(any(row[2] is None for row in rows))
        self.assertTrue(any(row[2] == "" for row in rows))

    def test_missing_table_is_not_empty_success(self):
        case, workspace, oracle = self.fixture("sqlite-schema-gap", solved=True)
        report = copy.deepcopy(oracle["expected_json"]["result/report.json"])
        report.update(status="complete", row_count=0)
        (workspace / "result/report.json").write_text(json.dumps(report), encoding="utf-8")
        self.assertFalse(case.grade(workspace, oracle)["passed"])

    def test_duplicate_keys_nonfinite_values_and_oversized_json_fail(self):
        invalid = (
            '{"status":"complete","status":"complete","selected_count":2}',
            '{"status":"complete","selected_count":NaN}',
            " " * 65_537,
            "[" * 1500 + "]" * 1500,
        )
        for index, contents in enumerate(invalid):
            case, workspace, oracle = self.fixture("jq-record-filter", seed=index, solved=True)
            (workspace / "result/report.json").write_text(contents, encoding="utf-8")
            self.assertFalse(case.grade(workspace, oracle)["passed"])

    def test_oversized_binary_output_fails(self):
        case, workspace, oracle = self.fixture("jq-exact-text", solved=True)
        with (workspace / "result/extracted.txt").open("wb") as output:
            output.truncate(MAX_ARTIFACT_BYTES + 1)
        self.assertFalse(case.grade(workspace, oracle)["passed"])

    def test_symlink_output_is_rejected_without_reading_target(self):
        case, workspace, oracle = self.fixture("jq-exact-text", solved=True)
        output = workspace / "result/extracted.txt"
        outside = self.root / "outside.txt"
        outside.write_bytes(output.read_bytes())
        output.unlink()
        try:
            output.symlink_to(outside)
        except OSError as error:
            self.skipTest(f"Host does not permit symlink creation: {error}")
        self.assertFalse(case.grade(workspace, oracle)["passed"])

    def test_symlink_result_directory_is_rejected(self):
        case, workspace, oracle = self.fixture("jq-exact-text", solved=True)
        result = workspace / "result"
        elsewhere = self.root / "elsewhere"
        result.rename(elsewhere)
        try:
            result.symlink_to(elsewhere, target_is_directory=True)
        except OSError as error:
            self.skipTest(f"Host does not permit symlink creation: {error}")
        self.assertFalse(case.grade(workspace, oracle)["passed"])

    def test_excessive_result_tree_is_rejected(self):
        case, workspace, oracle = self.fixture("jq-exact-text", solved=True)
        for index in range(130):
            (workspace / "result" / f"extra-{index}").touch()
        self.assertFalse(case.grade(workspace, oracle)["passed"])


if __name__ == "__main__":
    unittest.main()
