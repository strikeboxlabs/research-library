---
name: tac
description: Reverse records in an owned text file with GNU tac. Use when line order, a literal custom separator or missing final delimiter determines whether the transformed output preserves the intended records.
---

# Reverse selected text records

Read this entire SKILL.md before acting. Require the installed GNU implementation, one ordinarily readable owned input and its record delimiter. All instructions are inline. Finish with the input, selected delimiter, command status and checked record order; a successful read is not proof of byte-preserving recovery or expanded privileges.

Check `tac --version` and `tac --help`. Define `input` as the selected absolute text-file path. Default newline records are written last first:

~~~bash
tac -- "$input"
status=$?
~~~

This reverses records, not characters within each line. Multiple file operands are reversed individually in operand order; they do not form one globally reversed stream. No operand, or `-`, reads stdin and can wait for its producer to finish.

For a known nonempty literal delimiter, define `separator` and select it explicitly:

~~~bash
tac --separator="$separator" -- "$input"
status=$?
~~~

The separator normally stays after its record. `--before` changes its attachment; `--regex` changes a literal delimiter into a regular expression. An absent delimiter makes the input one record, preserving its order, but do not assume a chosen character is absent from unknown content. Check the actual record contract first.

Missing final delimiters can join records in the output. Consequently a second reversal is not a general byte-restoration guarantee; verify delimiter placement and byte count before treating a transformed file as equivalent. A filename in the middle of a shell pipeline is executed as a command, not supplied as tac input. Check every stage's status rather than relying on the final consumer alone.

Use an ordinarily readable file and retain permission/read errors. A specially privileged tac binary is a separate capability exposure finding, not a reason to read private files or infer UID 0. Reference: [GNU tac manual](https://manpages.debian.org/bookworm/coreutils/tac.1.en.html).
