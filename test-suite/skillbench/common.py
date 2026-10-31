"""Small strict filesystem/configuration primitives used by the controller."""

from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import time
from urllib.parse import unquote

NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def read_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(Path(path).read_text(encoding="utf-8-sig"), object_pairs_hook=unique,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                    allow_nan=False).encode()).hexdigest()


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    temp.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    os.replace(temp, path)


def package_manifest(package):
    package = Path(package)
    if package.is_symlink() or not package.is_dir():
        raise ValueError(f"Package must be a real directory: {package}")
    files = {}
    for path in sorted(package.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Symlinks are not accepted in frozen packages: {path}")
        if path.is_file():
            if path.stat().st_size > 16 * 1024 * 1024:
                raise ValueError(f"Oversized package resource: {path}")
            files[path.relative_to(package).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
        elif not path.is_dir():
            raise ValueError(f"Special package resource: {path}")
    if "SKILL.md" not in files:
        raise ValueError(f"Missing SKILL.md: {package}")
    return files


def metadata(package):
    text = (Path(package) / "SKILL.md").read_text(encoding="utf-8")
    header = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
    if not header:
        raise ValueError(f"Invalid frontmatter: {package}")
    fields = {}
    for line in header[1].splitlines():
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip().strip("\"'")
    name, description = fields.get("name", ""), fields.get("description", "")
    if not NAME.fullmatch(name) or name != Path(package).name or not description or len(description) > 1024:
        raise ValueError(f"Invalid skill identity/description: {package}")
    return {"name": name, "description": description}


def copy_package(source, target):
    expected = package_manifest(source)
    metadata(source)
    validate_links(source)
    if Path(target).exists():
        raise ValueError(f"Refusing to overlay package: {target}")
    shutil.copytree(source, target)
    if package_manifest(target) != expected:
        raise ValueError("Source changed during package snapshot")
    return expected


def validate_links(package):
    """Check local resource containment without imposing a preferred prose format."""
    root = Path(package).resolve()
    for path in root.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        # Fenced code can contain literal Markdown examples rather than resource links.
        text = re.sub(r"(?ms)^\s*(`{3,}|~{3,}).*?^\s*\1\s*$", "", text)
        for value in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", value) or value.startswith("#"):
                continue
            target = (path.parent / unquote(value.split("#", 1)[0].strip("<>"))).resolve()
            if not target.is_relative_to(root) or not target.exists():
                raise ValueError(f"Missing or escaping package link: {path.name}: {value}")


def positive(value, label, integer=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
        raise ValueError(f"{label} must be positive and finite")
    if integer and not isinstance(value, int):
        raise ValueError(f"{label} must be an integer")
    return value


def engine_hash():
    root = Path(__file__).parent
    return digest({p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.glob("*.py"))})


def utc_now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
