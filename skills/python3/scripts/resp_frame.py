"""Encode one RESP command from exact argument files; perform no network I/O."""
import argparse
import json
from pathlib import Path
import sys


def frame(parts):
    if not parts:
        raise ValueError("at least one argument is required")
    return (b"*" + str(len(parts)).encode("ascii") + b"\r\n"
            + b"".join(b"$" + str(len(p)).encode("ascii") + b"\r\n"
                       + p + b"\r\n" for p in parts))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-string", action="store_true",
                        help="emit a JSON string only when the framed bytes are UTF-8")
    parser.add_argument("argument_files", nargs="+")
    args = parser.parse_args()
    try:
        parts = [Path(p).read_bytes() for p in args.argument_files]
        data = frame(parts)
        if args.json_string:
            data = json.dumps(data.decode("utf-8"), ensure_ascii=True).encode("ascii")
    except (OSError, UnicodeError, ValueError) as error:
        parser.exit(1, f"encoding failed: {error}\n")
    sys.stdout.buffer.write(data)


if __name__ == "__main__":
    main()
