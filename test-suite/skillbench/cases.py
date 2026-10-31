"""Seeded, disposable fixtures and private artifact graders.

These cases use Python's standard library to construct data and calibrate graders.
Neither preparation nor ``solve`` establishes that a Linux CLI or worker succeeded.
Oracle dictionaries are JSON serializable and must remain outside worker access.
The controller must stop worker processes before grading; graders are not a sandbox.
"""

from __future__ import annotations

import base64
from dataclasses import dataclass
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import random
import sqlite3
import stat
import tarfile
from typing import Callable


MAX_ARTIFACT_BYTES = 1_048_576
MAX_TREE_ENTRIES = 128


class ArtifactError(ValueError):
    """An artifact cannot be read safely or does not meet its format contract."""


def _link(info: os.stat_result) -> bool:
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0)
        & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    )


def _safe_path(workspace: Path, relative: str) -> Path:
    """Reject absolute/traversing names and symlinks/reparse points in the path."""
    name = PurePosixPath(relative)
    if not relative or name.is_absolute() or ".." in name.parts or "\\" in relative:
        raise ArtifactError("invalid artifact path")
    if any(":" in part for part in name.parts):
        raise ArtifactError("invalid artifact path")
    root = Path(workspace).absolute()
    info = root.lstat()
    if _link(info) or not stat.S_ISDIR(info.st_mode):
        raise ArtifactError("workspace is not an ordinary directory")
    current = root
    for index, part in enumerate(name.parts):
        current = current / part
        info = current.lstat()
        if _link(info):
            raise ArtifactError("symlink or reparse point rejected")
        if index < len(name.parts) - 1 and not stat.S_ISDIR(info.st_mode):
            raise ArtifactError("artifact parent is not a directory")
    return current


def _read(workspace: Path, relative: str, maximum: int = MAX_ARTIFACT_BYTES) -> bytes:
    path = _safe_path(workspace, relative)
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode) or before.st_size > maximum:
        raise ArtifactError("artifact is not a bounded regular file")
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    flags |= getattr(os, "O_NONBLOCK", 0)
    if os.open in os.supports_dir_fd and hasattr(os, "O_NOFOLLOW"):
        # Open each Linux directory relative to its descriptor. A parent swapped
        # for a symlink after lstat must not redirect an evaluator's file read.
        directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
        parent = os.open(Path(workspace).absolute(), directory_flags)
        try:
            parts = PurePosixPath(relative).parts
            for part in parts[:-1]:
                child = os.open(part, directory_flags, dir_fd=parent)
                os.close(parent)
                parent = child
            descriptor = os.open(parts[-1], flags, dir_fd=parent)
        finally:
            os.close(parent)
    else:
        descriptor = os.open(path, flags)
    with os.fdopen(descriptor, "rb") as stream:
        opened = os.fstat(stream.fileno())
        if (not stat.S_ISREG(opened.st_mode) or opened.st_size > maximum
                or (before.st_dev, before.st_ino) != (opened.st_dev, opened.st_ino)):
            raise ArtifactError("artifact changed or is not a bounded regular file")
        data = stream.read(maximum + 1)
    if len(data) > maximum:
        raise ArtifactError("artifact exceeds size limit")
    return data


def _tree(workspace: Path, relative: str) -> tuple[set[str], set[str]]:
    root = _safe_path(workspace, relative)
    if not root.is_dir():
        raise ArtifactError("artifact tree is not a directory")
    files: set[str] = set()
    directories: set[str] = set()
    pending = [root]
    entries = 0
    while pending:
        directory = pending.pop()
        with os.scandir(directory) as children:
            for entry in children:
                entries += 1
                if entries > MAX_TREE_ENTRIES:
                    raise ArtifactError("artifact tree exceeds entry limit")
                info = entry.stat(follow_symlinks=False)
                if _link(info):
                    raise ArtifactError("symlink or reparse point rejected")
                path = Path(entry.path)
                name = path.relative_to(Path(workspace).absolute()).as_posix()
                if stat.S_ISDIR(info.st_mode):
                    directories.add(name)
                    pending.append(path)
                elif stat.S_ISREG(info.st_mode):
                    files.add(name)
                else:
                    raise ArtifactError("special artifact file rejected")
    return files, directories


def _snapshot(workspace: Path) -> dict:
    files, directories = _tree(workspace, "input")
    return {
        "files": {name: hashlib.sha256(_read(workspace, name)).hexdigest()
                  for name in sorted(files)},
        "directories": sorted(directories),
    }


def _json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def _json_read(workspace: Path, relative: str) -> object:
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ArtifactError("duplicate JSON key")
            result[key] = value
        return result

    def invalid_constant(_value):
        raise ArtifactError("non-finite JSON number")

    try:
        return json.loads(_read(workspace, relative, 65_536).decode("utf-8"),
                          object_pairs_hook=unique, parse_constant=invalid_constant)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as error:
        raise ArtifactError("invalid or excessively nested JSON") from error


def _typed_equal(actual: object, expected: object) -> bool:
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        return actual.keys() == expected.keys() and all(
            _typed_equal(actual[key], value) for key, value in expected.items()
        )
    if isinstance(expected, list):
        return len(actual) == len(expected) and all(
            _typed_equal(left, right) for left, right in zip(actual, expected)
        )
    return actual == expected


def _expected(raw: dict[str, bytes] | None = None, structured: dict | None = None) -> dict:
    return {
        "expected_files": {name: base64.b64encode(value).decode("ascii")
                           for name, value in (raw or {}).items()},
        "expected_json": structured or {},
    }


def _write(workspace: Path, relative: str, data: bytes) -> None:
    path = workspace / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(data)


def _token(rng: random.Random) -> str:
    return f"{rng.getrandbits(64):016x}"


def _exact_text(workspace: Path, rng: random.Random) -> dict:
    content = f"record={_token(rng)}\nQuotes: \"yes\"; slash: \\; tab:\t\nUnicode: café λ\nno final newline"
    _write(workspace, "input/response.json", _json_bytes({"file": content, "encoding": "utf-8"}))
    return _expected({"result/extracted.txt": content.encode("utf-8")})


def _record_filter(workspace: Path, rng: random.Random) -> dict:
    records = [
        {"id": _token(rng), "selected": True, "text": "first\nsecond", "value": 0},
        {"id": _token(rng), "selected": False},
        {"id": _token(rng), "selected": "true"},
        {"id": _token(rng), "selected": None},
        {"id": _token(rng)},
        {"id": _token(rng), "selected": True, "text": "café,\"quoted\"", "value": False},
    ]
    rng.shuffle(records)
    duplicate = next(row for row in records if row.get("selected") is True)
    records.insert(rng.randrange(len(records) + 1), dict(duplicate))
    encoded = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in records).encode("utf-8")
    _write(workspace, "input/records.jsonl", encoded)
    selected = [row for row in records if row.get("selected") is True]
    return _expected(structured={
        "result/selected.json": selected,
        "result/report.json": {"status": "complete", "selected_count": len(selected)},
    })


def _late_malformed(workspace: Path, rng: random.Random) -> dict:
    count = rng.randrange(7, 12)
    records = [{"id": _token(rng), "selected": index % 2 == 0} for index in range(count)]
    encoded = "".join(json.dumps(row) + "\n" for row in records)
    encoded += '{"id": "broken", "selected": true\n'
    _write(workspace, "input/records.jsonl", encoded.encode("utf-8"))
    return _expected(structured={"result/report.json": {
        "status": "invalid_input", "accepted": False,
        "selected_count": None, "error_line": count + 1,
    }})


def _archive(members: list[tuple[str, bytes]]) -> bytes:
    output = io.BytesIO()
    with tarfile.open(fileobj=output, mode="w", format=tarfile.USTAR_FORMAT) as archive:
        for name, content in members:
            info = tarfile.TarInfo(name)
            info.size, info.mode, info.mtime = len(content), 0o600, 0
            archive.addfile(info, io.BytesIO(content))
    return output.getvalue()


def _selected_members(workspace: Path, rng: random.Random) -> dict:
    members = [
        ("bundle/report note.txt", f"report {_token(rng)}\n".encode()),
        ("bundle/-n.txt", bytes(rng.randrange(256) for _ in range(31))),
        ("bundle/quo'te.txt", f"literal dollar $ and quote: {_token(rng)}".encode()),
        ("bundle/unselected.txt", b"This member must not be extracted.\n"),
    ]
    _write(workspace, "input/archive.tar", _archive(members))
    _write(workspace, "input/selection.json", _json_bytes([name for name, _ in members[:3]]))
    return _expected({f"result/extracted/{name}": data for name, data in members[:3]})


def _truncated_archive(workspace: Path, rng: random.Random) -> dict:
    first = f"complete member {_token(rng)}\n".encode()
    later = bytes(rng.randrange(256) for _ in range(4096))
    archive = _archive([("bundle/complete.txt", first), ("bundle/truncated.bin", later)])
    # Two headers and one complete padded member precede the truncated payload.
    _write(workspace, "input/archive.tar", archive[:2048])
    return _expected({"result/extracted/bundle/complete.txt": first}, {
        "result/report.json": {"status": "partial_archive", "archive_complete": False,
                               "recovered": ["bundle/complete.txt"]},
    })


def _typed_export(workspace: Path, rng: random.Random) -> dict:
    rows = [
        (rng.randrange(10, 100), "comma,name", "line one\nline two", 1),
        (rng.randrange(110, 200), "café", None, 1),
        (rng.randrange(210, 300), 'quote"name', "", 1),
        (rng.randrange(310, 400), "not selected", "hidden", 0),
    ]
    connection = sqlite3.connect(workspace / "input" / "records.db")
    try:
        connection.execute("CREATE TABLE records (id INTEGER PRIMARY KEY, name TEXT NOT NULL, note TEXT, enabled INTEGER NOT NULL)")
        connection.executemany("INSERT INTO records VALUES (?, ?, ?, ?)", rows)
        connection.commit()
    finally:
        connection.close()
    expected = [{"id": row[0], "name": row[1], "note": row[2]} for row in rows if row[3] == 1]
    return _expected(structured={"result/rows.json": expected})


def _schema_gap(workspace: Path, rng: random.Random) -> dict:
    connection = sqlite3.connect(workspace / "input" / "records.db")
    try:
        connection.execute("CREATE TABLE events (id INTEGER PRIMARY KEY, message TEXT)")
        connection.execute("INSERT INTO events VALUES (?, ?)", (rng.randrange(1, 10000), _token(rng)))
        connection.commit()
    finally:
        connection.close()
    return _expected(structured={"result/report.json": {
        "status": "missing_table", "table": "records", "row_count": None,
        "available_tables": ["events"],
    }})


@dataclass(frozen=True)
class Case:
    id: str
    skill: str
    family: str
    split: str
    description: str
    tools: tuple[str, ...]
    request: str
    builder: Callable[[Path, random.Random], dict]

    def prepare(self, workspace: Path, seed: int) -> dict:
        workspace = Path(workspace).absolute()
        workspace.mkdir(parents=True, exist_ok=True)
        (workspace / "input").mkdir()  # Refuse to overlay an earlier fixture.
        rng = random.Random(seed)
        _write(workspace, "input/untouched.txt", f"preserve {_token(rng)}\n".encode())
        oracle = self.builder(workspace, rng)
        oracle.update({"case_id": self.id, "seed": seed, "input_snapshot": _snapshot(workspace)})
        return oracle

    def prompt(self) -> str:
        return (self.request + "\n\nWork relative to the supplied workspace. Preserve every input file "
                "and its bytes, including input/untouched.txt. Place only the requested final artifacts "
                "under result/; use a separate scratch/ directory for temporary work. Create output "
                "directories as needed. Do not install packages, contact external services or modify "
                "files outside this workspace. Explain any limitation honestly.")

    def grade(self, workspace: Path, oracle: dict) -> dict:
        workspace = Path(workspace).absolute()
        checks: dict[str, bool] = {"oracle_case": oracle.get("case_id") == self.id}
        details: list[str] = []

        def check(label, operation):
            try:
                checks[label] = bool(operation())
            except (OSError, ValueError, RecursionError, OverflowError):
                checks[label] = False
            if not checks[label]:
                details.append(f"Failed: {label}")

        check("inputs_unchanged", lambda: _snapshot(workspace) == oracle["input_snapshot"])
        expected_paths = set(oracle["expected_files"]) | set(oracle["expected_json"])
        check("result_file_set", lambda: _tree(workspace, "result")[0] == expected_paths)
        for name, encoded in oracle["expected_files"].items():
            check(f"bytes:{name}", lambda name=name, encoded=encoded:
                  _read(workspace, name) == base64.b64decode(encoded, validate=True))
        for name, expected in oracle["expected_json"].items():
            check(f"json:{name}", lambda name=name, expected=expected:
                  _typed_equal(_json_read(workspace, name), expected))
        return {"passed": all(checks.values()), "checks": checks, "details": details}

    def solve(self, workspace: Path, oracle: dict) -> None:
        """Write private known-good answers solely to calibrate artifact graders."""
        if oracle.get("case_id") != self.id:
            raise ValueError("oracle does not belong to this case")
        workspace = Path(workspace)
        for name, encoded in oracle["expected_files"].items():
            _write(workspace, name, base64.b64decode(encoded, validate=True))
        for name, value in oracle["expected_json"].items():
            _write(workspace, name, _json_bytes(value))


_CASES = (
    Case("jq-exact-text", "jq", "json-text", "development",
         "Extract Unicode text without adding or removing bytes.", ("jq",),
         "Extract the string field file from input/response.json into result/extracted.txt as UTF-8. "
         "Preserve its exact decoded text, including whitespace and whether it ends with a newline; "
         "do not include JSON quotation marks.", _exact_text),
    Case("jq-record-filter", "jq", "json-records", "development",
         "Select boolean-true JSON records without type coercion or deduplication.", ("jq",),
         "Read every JSON object in input/records.jsonl. Write a JSON array to result/selected.json "
         "containing exactly the complete records whose selected field is the boolean true, in input "
         "order, retaining duplicates. Write result/report.json with exactly status (complete) and "
         "selected_count (integer). Only accept the result if the entire input is valid.", _record_filter),
    Case("jq-late-malformed", "jq", "json-invalid-stream", "holdout",
         "Reject a late malformed record instead of accepting a valid prefix.", ("jq",),
         "Validate every line of input/records.jsonl as one JSON object before accepting the selected "
         "boolean-true records. On valid input write result/selected.json as an ordered array and "
         "result/report.json with status complete, accepted true, selected_count and error_line null. "
         "On malformed input publish no selected.json; write only result/report.json with exactly "
         "status invalid_input, accepted false, selected_count null and error_line equal to the "
         "one-based malformed line number. A valid prefix is not an accepted result.", _late_malformed),
    Case("tar-selected-members", "tar", "archive-selection", "development",
         "Extract exact selected archive members with unusual names.", ("tar",),
         "Extract only the exact archive member names listed in input/selection.json from "
         "input/archive.tar into result/extracted/, preserving their member paths and bytes. "
         "Do not extract other members or execute any archive content.", _selected_members),
    Case("tar-truncated", "tar", "archive-incomplete", "holdout",
         "Recover a complete member without claiming a truncated archive is complete.", ("tar",),
         "Inspect input/archive.tar for completeness. Recover bundle/complete.txt under "
         "result/extracted/ with its full member path if that member is intact. Do not publish partial "
         "members. Write result/report.json with exactly status (complete_archive or partial_archive), "
         "archive_complete (boolean), and recovered (array of recovered member names). Do not execute "
         "archive content; a recovered early member does not establish archive completeness.", _truncated_archive),
    Case("sqlite-typed-export", "sqlite3", "database-export", "development",
         "Export selected SQLite rows with correct types and text framing.", ("sqlite3",),
         "Inspect the existing input/records.db and export records where enabled equals 1. Write "
         "result/rows.json as a JSON array ordered by numeric id; each object must contain exactly "
         "id, name and note with their stored types and values. Preserve NULL separately from an "
         "empty string and preserve embedded punctuation and newlines. Use read-only inspection "
         "or an owned scratch copy.", _typed_export),
    Case("sqlite-schema-gap", "sqlite3", "database-missing-schema", "holdout",
         "Distinguish a missing requested table from a valid empty result.", ("sqlite3",),
         "Inspect input/records.db and report the count of rows in table records, without creating "
         "or changing a database. Write only result/report.json with exactly status (complete if "
         "the table exists, otherwise missing_table), table (records), row_count (integer if the "
         "table exists, otherwise null), and available_tables (sorted names of ordinary user tables). "
         "Use read-only inspection or an owned scratch copy.", _schema_gap),
)

CASES: dict[str, Case] = {case.id: case for case in _CASES}
