"""Known wrong solutions must fail even when their outputs look plausible."""
import json
from pathlib import Path
import shutil
import sqlite3
import tarfile
import tempfile
import unittest

from skillbench.cases import CASES
from skillbench.reporting import case_diagnostics


class ChallengeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def solved(self, name):
        case = CASES[name]
        work = self.root / name
        oracle = case.prepare(work, 44)
        case.solve(work, oracle)
        return case, work, oracle

    def test_event_type_identity_and_atomic_shard_rejection(self):
        case, work, oracle = self.solved('jq-reconcile-events')
        rows = oracle['expected_json']['result/records.json']
        self.assertEqual(len([r for r in rows if r['tenant'] == 'east' and r['id'] in (0, '0')]), 2)
        path = work / 'result/records.json'
        # The tempting valid prefix of a rejected shard must not leak into output.
        prefix = json.loads((work / 'input/part-6.jsonl').read_text().splitlines()[0])
        path.write_text(json.dumps(rows + [prefix]))
        self.assertFalse(case.grade(work, oracle)['passed'])
        # Conflating numeric and string IDs drops a real, selected entity.
        path.write_text(json.dumps([r for r in rows if not (r['tenant'] == 'east' and r['id'] == '0')]))
        self.assertFalse(case.grade(work, oracle)['passed'])
        path.write_text(json.dumps(rows))
        report = oracle['expected_json']['result/report.json'].copy()
        report['accepted_shards'] = report['accepted_shards'] + ['part-7.jsonl']
        (work / 'result/report.json').write_text(json.dumps(report))
        self.assertFalse(case.grade(work, oracle)['passed'])

    def test_filtering_before_resolving_revisions_keeps_stale_active_records(self):
        case, work, oracle = self.solved('jq-reconcile-events')
        winners = {}
        for shard in sorted((work / 'input').glob('part-[0-5].jsonl')):
            for line in shard.read_text().splitlines():
                row = json.loads(line)
                if row['active'] is not True:
                    continue
                key = row['tenant'], type(row['id']), row['id']
                if key not in winners or row['revision'] > winners[key]['revision']:
                    winners[key] = row
        wrong = sorted(winners.values(), key=lambda r: (r['tenant'], isinstance(r['id'], str), r['id']))
        self.assertNotEqual(wrong, oracle['expected_json']['result/records.json'])
        (work / 'result/records.json').write_text(json.dumps(wrong))
        self.assertFalse(case.grade(work, oracle)['passed'])

    def test_archive_first_last_and_concatenated_occurrences_fail(self):
        case, work, oracle = self.solved('tar-manifest-recovery')
        files = json.loads((work / 'input/deployment.json').read_text())['files']
        item = files[0]
        with tarfile.open(work / 'input/history.tar') as archive:
            versions = [archive.extractfile(m).read() for m in archive if m.name == item['path']]
        self.assertEqual(len(versions), 3)
        for data in (versions[0], versions[-1], b''.join(versions)):
            (work / 'result/restored' / item['path']).write_bytes(data)
            self.assertFalse(case.grade(work, oracle)['passed'])

    def test_wal_commits_are_required_and_input_sidecars_are_protected(self):
        case, work, oracle = self.solved('sqlite-wal-export')
        scratch = work / 'scratch'
        scratch.mkdir()
        shutil.copy(work / 'input/orders.db', scratch / 'stale.db')
        with sqlite3.connect(scratch / 'stale.db') as db:
            self.assertEqual(db.execute("SELECT count(*) FROM orders WHERE status='paid'").fetchone()[0], 0)
        for name in ('orders.db', 'orders.db-wal'):
            shutil.copy(work / 'input' / name, scratch / name)
        with sqlite3.connect(scratch / 'orders.db') as db:
            self.assertEqual(db.execute("SELECT count(*) FROM orders WHERE status='paid'").fetchone()[0], 16)
        path = work / 'result/paid-orders.json'
        original = path.read_bytes()
        path.write_text('[]')
        self.assertFalse(case.grade(work, oracle)['passed'])
        path.write_bytes(original)
        (work / 'input/orders.db-shm').write_bytes(b'new sidecar')
        self.assertFalse(case.grade(work, oracle)['checks']['inputs_unchanged'])

    def test_ceiling_requires_all_planned_baselines_without_infrastructure_errors(self):
        plan = [{'case_id': 'jq-exact-text', 'condition': 'baseline'}] * 2
        row = {'case_id': 'jq-exact-text', 'condition': 'baseline', 'status': 'completed', 'passed': True}
        for rows, expected in (([row], False), ([row, row], True),
                               ([row, dict(row, status='runner_error')], False),
                               ([row, dict(row, passed=False)], False)):
            self.assertEqual(case_diagnostics(rows, plan)['jq-exact-text']['baseline_at_ceiling'], expected)
