"""Actual-CLI smoke references for the seven disposable benchmark fixtures.

These scripts read only worker-visible inputs and invoke jq, GNU tar or sqlite3.
They never consume private grader answers. Python provides argument framing and
report construction where useful. Running one checks the CLI/fixture/grader
integration, not skill discovery, model quality or the optimal command sequence.

Requirements: Bash, Python 3, GNU tar and SQLite's CLI with JSON output support,
plus jq for its cases. The caller provides a fresh fixture workspace and enforces
the outer process/container deadline. All expected command failures are handled.
"""

from __future__ import annotations

from textwrap import dedent


_HEADER = "#!/usr/bin/env bash\nset -euo pipefail\numask 077\nmkdir -p result scratch\n"

_SCRIPTS = {
    "jq-exact-text": r'''
        jq -s -e 'length == 1 and (.[0] | type == "object" and (.file | type == "string"))' \
          input/response.json > /dev/null
        jq -j '.file' input/response.json > result/extracted.txt
    ''',
    "jq-record-filter": r'''
        jq -s -e 'all(.[]; type == "object")' input/records.jsonl > /dev/null
        jq -s 'map(select(.selected == true))' input/records.jsonl > result/selected.json
        jq '{status: "complete", selected_count: length}' result/selected.json > result/report.json
    ''',
    "jq-late-malformed": r'''
        python3 - <<'PY'
        import json
        from pathlib import Path
        import subprocess

        error_line = None
        with Path("input/records.jsonl").open("rb") as source:
            for line_number, line in enumerate(source, 1):
                checked = subprocess.run(
                    ["jq", "-s", "-e", 'length == 1 and (.[0] | type == "object")'],
                    input=line, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=20,
                )
                if checked.returncode:
                    error_line = line_number
                    Path("scratch/validation.stderr").write_bytes(checked.stderr)
                    break
        if error_line is not None:
            report = {"status": "invalid_input", "accepted": False,
                      "selected_count": None, "error_line": error_line}
        else:
            selected = subprocess.run(
                ["jq", "-s", "map(select(.selected == true))", "input/records.jsonl"],
                check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20,
            )
            Path("result/selected.json").write_bytes(selected.stdout)
            report = {"status": "complete", "accepted": True,
                      "selected_count": len(json.loads(selected.stdout)), "error_line": None}
        Path("result/report.json").write_text(json.dumps(report) + "\n", encoding="utf-8")
        PY
    ''',
    "tar-selected-members": r'''
        python3 - <<'PY'
        import json
        from pathlib import Path, PurePosixPath
        import subprocess

        members = json.loads(Path("input/selection.json").read_text(encoding="utf-8"))
        if not isinstance(members, list) or not members:
            raise ValueError("Expected a nonempty list of selected archive member names")
        for member in members:
            if not isinstance(member, str) or not member or PurePosixPath(member).is_absolute() or ".." in PurePosixPath(member).parts:
                raise ValueError("Invalid selected member path")
        with Path("scratch/archive-list.txt").open("wb") as listing:
            subprocess.run(["tar", "--list", "--file=input/archive.tar"],
                           stdout=listing, check=True, timeout=20)
        Path("result/extracted").mkdir()
        subprocess.run(
            ["tar", "--extract", "--file=input/archive.tar", "--directory=result/extracted",
             "--no-same-owner", "--no-same-permissions", "--keep-old-files", "--", *members],
            check=True, timeout=20,
        )
        PY
    ''',
    "tar-truncated": r'''
        python3 - <<'PY'
        import json
        from pathlib import Path
        import subprocess

        with Path("scratch/archive-list.txt").open("wb") as listing:
            inspected = subprocess.run(
                ["tar", "--list", "--file=input/archive.tar"],
                stdout=listing, stderr=subprocess.PIPE, timeout=20,
            )
        Path("scratch/archive-list.stderr").write_bytes(inspected.stderr)
        # GNU --occurrence=1 ends this selected extraction after that member;
        # the separate full listing above checks the rest of the archive.
        member = "bundle/complete.txt"
        extracted = subprocess.run(
            ["tar", "--extract", "--to-stdout", "--occurrence=1",
             "--file=input/archive.tar", "--", member],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20,
        )
        Path("scratch/member-extraction.stderr").write_bytes(extracted.stderr)
        recovered = []
        if extracted.returncode == 0:
            destination = Path("result/extracted") / member
            destination.parent.mkdir(parents=True)
            destination.write_bytes(extracted.stdout)
            recovered.append(member)
        complete = inspected.returncode == 0
        report = {"status": "complete_archive" if complete else "partial_archive",
                  "archive_complete": complete, "recovered": recovered}
        Path("result/report.json").write_text(json.dumps(report) + "\n", encoding="utf-8")
        PY
    ''',
    "sqlite-typed-export": r'''
        sqlite3 -init /dev/null -readonly -batch -bail -json input/records.db \
          'SELECT id, name, note FROM records WHERE enabled = 1 ORDER BY id;' > result/rows.json
    ''',
    "sqlite-schema-gap": r'''
        python3 - <<'PY'
        import json
        from pathlib import Path
        import subprocess

        def query(sql):
            completed = subprocess.run(
                ["sqlite3", "-init", "/dev/null", "-readonly", "-batch", "-bail", "-json",
                 "input/records.db", sql],
                check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20,
            )
            return json.loads(completed.stdout or b"[]")

        tables = [row["name"] for row in query(
            "SELECT name FROM sqlite_schema WHERE type = 'table' "
            "AND substr(name, 1, 7) <> 'sqlite_' ORDER BY name;"
        )]
        exists = "records" in tables
        count = query('SELECT count(*) AS n FROM "records";')[0]["n"] if exists else None
        report = {"status": "complete" if exists else "missing_table", "table": "records",
                  "row_count": count, "available_tables": tables}
        Path("result/report.json").write_text(json.dumps(report) + "\n", encoding="utf-8")
        PY
    ''',
}


_SCRIPTS.update({
    'jq-reconcile-events': r'''
        python3 - <<'PY'
        import json, subprocess
        from pathlib import Path
        contract = json.loads(Path('input/export-contract.json').read_text())
        accepted, rejected, winners = [], [], {}
        # jq validates each physical JSONL record, including schema/type checks.
        predicate = """length == 1 and (.[0] | type == "object" and
          (.tenant | type == "string") and
          ((.id | type == "string") or (.id | type == "number" and floor == .)) and
          (.revision | type == "number" and . > 0 and floor == .) and
          has("active") and (.value | type == "string"))"""
        for name in contract['shards']:
            rows, valid = [], True
            for line in Path('input', name).read_bytes().splitlines():
                p = subprocess.run(['jq', '-s', '-e', predicate], input=line,
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=20)
                if p.returncode:
                    valid = False
                    break
                rows.append(json.loads(line))
            if not valid:
                rejected.append(name)
                continue
            accepted.append(name)
            for row in rows:
                key = row['tenant'], type(row['id']).__name__, row['id']
                if key not in winners or row['revision'] > winners[key]['revision']:
                    winners[key] = row
        selected = [r for r in winners.values() if r['active'] is True]
        selected.sort(key=lambda r: (r['tenant'], isinstance(r['id'], str), r['id']))
        Path('result/records.json').write_text(json.dumps(selected))
        Path('result/report.json').write_text(json.dumps({'accepted_shards': sorted(accepted),
            'rejected_shards': sorted(rejected), 'selected_count': len(selected)}))
        PY
    ''',
    'tar-manifest-recovery': r'''
        python3 - <<'PY'
        import hashlib, json, subprocess, tarfile
        from pathlib import Path
        wanted = json.loads(Path('input/deployment.json').read_text())['files']
        # Enumerate exact member names without parsing tar's display quoting.
        with tarfile.open('input/history.tar') as archive:
            counts = {}
            for member in archive:
                counts[member.name] = counts.get(member.name, 0) + 1
        for item in wanted:
            found = None
            for occurrence in range(1, counts.get(item['path'], 0) + 1):
                data = subprocess.run(['tar', '-xOf', 'input/history.tar',
                    '--occurrence=' + str(occurrence), '--', item['path']],
                    check=True, capture_output=True, timeout=20).stdout
                if hashlib.sha256(data).hexdigest() == item['sha256']:
                    found = data
                    break
            if found is None:
                raise ValueError('No matching member revision')
            path = Path('result/restored') / item['path']
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(found)
        Path('result/report.json').write_text(json.dumps({'status': 'complete',
            'files': sorted(wanted, key=lambda r: r['path'])}))
        PY
    ''',
    'sqlite-wal-export': r'''
        cp input/orders.db input/orders.db-wal scratch/
        sqlite3 -init /dev/null -readonly -batch -bail -json scratch/orders.db \
          "SELECT o.id, c.name AS customer, o.amount_cents, o.note FROM orders o JOIN customers c ON c.id=o.customer_id WHERE o.status='paid' ORDER BY o.id" > result/paid-orders.json
        sqlite3 -init /dev/null -readonly -batch -bail -json scratch/orders.db \
          "SELECT 'complete' AS status, count(*) AS paid_count, sum(amount_cents) AS total_cents FROM orders WHERE status='paid'" > scratch/report-array.json
        python3 - <<'PY'
        import json
        from pathlib import Path
        Path('result/report.json').write_text(json.dumps(json.loads(Path('scratch/report-array.json').read_text())[0]))
        PY
    ''',
})


def reference_commands(case_id: str) -> str:
    """Return a Bash smoke procedure for one registered fixture; never its answer."""
    try:
        body = _SCRIPTS[case_id]
    except KeyError:
        raise KeyError(f"Unknown CLI reference case: {case_id}") from None
    return _HEADER + dedent(body).strip() + "\n"
