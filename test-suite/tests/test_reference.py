"""Reference validation; real CLI checks run only on a suitable Linux host."""

import ast
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import unittest

from skillbench.cases import CASES
from skillbench.reference import reference_commands


class ReferenceScriptTests(unittest.TestCase):
    def test_every_case_has_a_bounded_script_using_its_cli(self):
        for case_id, case in CASES.items():
            with self.subTest(case=case_id):
                script = reference_commands(case_id)
                self.assertTrue(script.startswith("#!/usr/bin/env bash\nset -euo pipefail\n"))
                self.assertLess(len(script), 16_384)
                self.assertIn(case.skill, script)
                self.assertIn("input/", script)
                self.assertIn("result/", script)
                for forbidden in ("oracle", "expected_json", "expected_files", "skillbench.cases"):
                    self.assertNotIn(forbidden, script)

    def test_embedded_python_has_valid_syntax(self):
        for case_id in CASES:
            with self.subTest(case=case_id):
                script = reference_commands(case_id)
                marker = "python3 - <<'PY'\n"
                if marker in script:
                    embedded = script.split(marker, 1)[1].rsplit("\nPY\n", 1)[0]
                    ast.parse(embedded, filename=f"reference:{case_id}")

    def test_unknown_case_fails_clearly(self):
        with self.assertRaisesRegex(KeyError, "Unknown CLI reference case"):
            reference_commands("missing-case")


class LinuxCliReferenceTests(unittest.TestCase):
    """Each generated test is an actual CLI smoke run, never an oracle writer."""

    def run_reference(self, case_id):
        if not sys.platform.startswith("linux"):
            self.skipTest("Actual CLI references require Linux; this is not a Linux execution result")
        case = CASES[case_id]
        for tool in ("bash", "python3", *case.tools):
            if shutil.which(tool) is None:
                self.skipTest(f"Required Linux executable is unavailable: {tool}")
        with tempfile.TemporaryDirectory(prefix="skillbench-cli-reference-") as temporary:
            for seed in (11, 9321):
                with self.subTest(seed=seed):
                    workspace = Path(temporary) / str(seed)
                    oracle = case.prepare(workspace, seed)
                    script = reference_commands(case_id)
                    syntax = subprocess.run(["bash", "--noprofile", "--norc", "-n"],
                                            input=script, text=True, capture_output=True, timeout=10)
                    self.assertEqual(syntax.returncode, 0, syntax.stderr)
                    process = subprocess.Popen(
                        ["bash", "--noprofile", "--norc", "-s"], cwd=workspace,
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        text=True, start_new_session=True,
                    )
                    try:
                        stdout, stderr = process.communicate(script, timeout=60)
                    except subprocess.TimeoutExpired:
                        os.killpg(process.pid, signal.SIGKILL)
                        process.communicate()
                        self.fail("Actual CLI reference exceeded its 60-second smoke deadline")
                    self.assertEqual(process.returncode, 0, f"stdout={stdout}\nstderr={stderr}")
                    report = case.grade(workspace, oracle)
                    self.assertTrue(report["passed"], report)


def _cli_test(case_id):
    def run(self):
        self.run_reference(case_id)
    run.__name__ = "test_" + case_id.replace("-", "_")
    return run


for _case_id in CASES:
    setattr(LinuxCliReferenceTests, "test_" + _case_id.replace("-", "_"), _cli_test(_case_id))


if __name__ == "__main__":
    unittest.main()
