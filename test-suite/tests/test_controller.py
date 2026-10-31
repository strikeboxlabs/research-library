import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from skillbench.campaign import create_campaign, load_results, run_campaign, verify_campaign
from skillbench.cases import CASES
from skillbench.common import copy_package, read_json, write_json
from skillbench.config import validate_config
from skillbench.planning import build_plan, library_inventory
from skillbench.reporting import make_report, paired_comparison, summarize


class ControllerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name, desc in (("jq", "JSON record filtering"), ("python3", "JSON programming"), ("tar", "archive files")):
            p = self.root / "library" / "skills" / name
            p.mkdir(parents=True)
            (p / "SKILL.md").write_text(f"---\nname: {name}\ndescription: {desc}\n---\nUseful instructions.\n", encoding="utf-8")
        self.cfg = validate_config({"schema_version": 1, "library_root": "library", "runs_root": "runs",
            "runtime": {"image": "owned-fixture", "model": "fake-model"}, "cases": ["jq-exact-text"],
            "repetitions": 2, "conditions": ["baseline", "current"],
            "selection": {"mode": "discovery", "catalog_size": 2, "distractors": "similar"}}, self.root)

    def test_invalid_configs(self):
        for update in ({"conditions": ["candidate"]}, {"seed": True}, {"repetitions": -1},
                       {"cases": ["missing"]}, {"surprise": 1}):
            with self.subTest(update=update), self.assertRaises(ValueError):
                validate_config({**self.cfg, **update}, self.root)

    def test_paired_schedule_and_distractors(self):
        plan = build_plan(self.cfg, library_inventory(self.cfg["library_root"]))
        self.assertEqual(plan, build_plan(self.cfg, library_inventory(self.cfg["library_root"])))
        self.assertEqual(len(plan), 4)
        for row in plan:
            if row["condition"] == "baseline":
                self.assertEqual(row["selected_skills"], [])
            else:
                self.assertEqual(set(row["selected_skills"]), {"jq", "python3"})
            counterpart = next(r for r in plan if r["block_id"] == row["block_id"] and r["condition"] != row["condition"])
            self.assertEqual(row["seed"], counterpart["seed"])

    def test_no_overlay_and_links(self):
        source = self.root / "library" / "skills" / "jq"
        dest = self.root / "copy" / "jq"
        copy_package(source, dest)
        with self.assertRaises(ValueError):
            copy_package(source, dest)
        with (source / "SKILL.md").open("a", encoding="utf-8") as f:
            f.write("[missing](references/missing.md)\n")
        with self.assertRaises(ValueError):
            copy_package(source, self.root / "bad" / "jq")

    def run_fake(self, run):
        calls = []
        def runner(workspace, skills, prompt, config, logs):
            calls.append(prompt)
            oracle = read_json(workspace.parent / "oracle.json")
            # Test double has controller privileges; real workers never receive oracle access.
            CASES["jq-exact-text"].solve(workspace, oracle)
            return {"status": "completed", "elapsed_seconds": 1.2, "usage": {"total_tokens": 100, "cost_usd": None}}
        run_campaign(run, runner=runner, progress=lambda _: None)
        return calls

    def test_campaign_snapshot_grading_and_resume(self):
        run = create_campaign(self.cfg, {"ok": True, "image_id": "sha256:owned-fixture"})
        calls = self.run_fake(run)
        self.assertEqual(len(calls), 4)
        self.assertTrue(all(r["passed"] for r in load_results(run)))
        self.assertEqual(self.run_fake(run), [])
        report = make_report(run)
        self.assertEqual(report["conditions"]["current"]["total_tokens_per_success"], 100)
        self.assertEqual(read_json(run / "manifest.json")["config"]["runtime"]["image"], "sha256:owned-fixture")

    def test_snapshot_mutation_prevents_resume(self):
        run = create_campaign(self.cfg, {"ok": True})
        p = run / "snapshots" / "current" / "jq" / "SKILL.md"
        p.write_text("changed", encoding="utf-8")
        with self.assertRaises(ValueError):
            verify_campaign(run)

    def test_plan_mutation_prevents_resume(self):
        run = create_campaign(self.cfg, {"ok": True})
        manifest = read_json(run / "manifest.json")
        manifest["plan"][0]["seed"] += 1
        write_json(run / "manifest.json", manifest)
        with self.assertRaises(ValueError):
            verify_campaign(run)

    def test_interrupted_usage_stops_token_limited_resume(self):
        self.cfg["budgets"]["max_total_tokens"] = 1000
        run = create_campaign(self.cfg, {"ok": True})
        first = read_json(run / "manifest.json")["plan"][0]
        write_json(run / "trials" / first["trial_id"] / "started.json", first)
        self.assertEqual(self.run_fake(run), [])
        self.assertEqual(read_json(run / "state.json")["status"], "token_usage_unavailable")

    def test_optimizer_trial_budget_is_aggregate(self):
        from skillbench.cli import optimize
        self.cfg["optimizer"] = {"model": "fake"}
        self.cfg["budgets"]["max_trials"] = 4
        source_run = create_campaign(self.cfg, {"ok": True})
        self.run_fake(source_run)
        def propose(source, target, evidence, config):
            copy_package(source, target)
            return {"generation": {"usage": {"total_tokens": 10}}, "hypothesis": "test"}
        def execute(config):
            run = create_campaign(config, {"ok": True})
            self.run_fake(run)
            return {"run_dir": str(run)}
        with patch("skillbench.optimizer.propose_candidate", side_effect=propose) as proposer, patch("skillbench.cli.execute_new", side_effect=execute):
            result = optimize(self.cfg, "jq", source_run, 3)
        self.assertEqual(proposer.call_count, 1)
        self.assertEqual(result["worker_trials"], 4)
        self.assertEqual(result["status"], "optimization_trial_budget")
        self.assertEqual(result["known_total_tokens"], 410)

    def test_optimizer_unknown_proposal_usage_stops_before_evaluation(self):
        from skillbench.cli import optimize
        self.cfg["optimizer"] = {"model": "fake"}
        self.cfg["budgets"]["max_total_tokens"] = 1000
        source_run = create_campaign(self.cfg, {"ok": True})
        self.run_fake(source_run)
        with patch("skillbench.optimizer.propose_candidate", return_value={"generation": {"usage": {}}}) as proposer, patch("skillbench.cli.execute_new") as execute:
            result = optimize(self.cfg, "jq", source_run, 3)
        self.assertEqual(proposer.call_count, 1)
        execute.assert_not_called()
        self.assertFalse(result["token_accounting_complete"])

    def test_interrupted_not_replayed(self):
        run = create_campaign(self.cfg, {"ok": True})
        manifest = read_json(run / "manifest.json")
        first = manifest["plan"][0]
        write_json(run / "trials" / first["trial_id"] / "started.json", first)
        self.assertEqual(len(self.run_fake(run)), 3)
        self.assertEqual(sum(r["status"] == "interrupted_runner" for r in load_results(run)), 1)

    def test_unknown_usage_stops_token_limited_campaign(self):
        self.cfg["budgets"]["max_total_tokens"] = 1000
        run = create_campaign(self.cfg, {"ok": True})
        result = run_campaign(run, runner=lambda *a: {"status": "completed", "usage": {"total_tokens": None}}, progress=lambda _: None)
        self.assertEqual(result["status"], "token_usage_unavailable")
        self.assertEqual(len(load_results(run)), 1)

    def test_failed_trials_count_cost_and_timeouts_count_failure(self):
        rows = [{"condition": "current", "status": "completed", "passed": True, "usage": {"total_tokens": 10}},
                {"condition": "current", "status": "timeout", "passed": False, "usage": {"total_tokens": 20}}]
        result = summarize(rows)["current"]
        self.assertEqual(result["pass_rate"], .5)
        self.assertEqual(result["total_tokens_per_success"], 30)
        self.assertIsNone(result["cost_usd"])

    def test_even_sample_median_and_output_budget_failures(self):
        rows = [{"condition": "current", "status": "completed", "passed": True, "elapsed_seconds": 1},
                {"condition": "current", "status": "budget_exceeded", "passed": False, "elapsed_seconds": 100}]
        result = summarize(rows)["current"]
        self.assertEqual(result["median_seconds"], 50.5)
        self.assertEqual(result["pass_rate"], .5)

    def test_interruption_is_not_complete(self):
        run = create_campaign(self.cfg, {"ok": True})
        with self.assertRaises(KeyboardInterrupt):
            run_campaign(run, runner=lambda *a: (_ for _ in ()).throw(KeyboardInterrupt()), progress=lambda _: None)
        self.assertEqual(read_json(run / "state.json")["status"], "interrupted")

    def test_existing_windows_lock_never_probes_with_kill(self):
        from skillbench.campaign import campaign_lock
        import socket
        folder = self.root / "lock-test"
        folder.mkdir()
        write_json(folder / "controller.lock", {"host": socket.gethostname(), "pid": 123})
        with patch("skillbench.campaign.Path", side_effect=lambda p: p), patch("skillbench.campaign.os.name", "nt"), patch("skillbench.campaign.os.kill") as kill:
            with self.assertRaises(ValueError):
                with campaign_lock(folder):
                    pass
            kill.assert_not_called()

    def test_few_families_do_not_get_confidence_interval(self):
        rows = [{"block_id": str(i), "case_id": "one", "family": "one", "condition": arm,
                 "status": "completed", "passed": arm == "candidate"} for i in range(20) for arm in ("current", "candidate")]
        result = paired_comparison(rows)
        self.assertEqual(result["paired_trials"], 20)
        self.assertIsNone(result["family_bootstrap_95pct"])


if __name__ == "__main__":
    unittest.main()
