---
name: cut
description: Select known delimiter-separated fields from acquired local text with GNU cut. Use when a small field projection is needed and delimiterless lines or quoted data can make apparently clean output misleading.
---

# Project fields under the actual text contract

Read this entire SKILL.md before acting. Establish the record delimiter, field delimiter and selected field before transforming the preserved input. No conditional resources are required. Finish with the selected data, status and format/coverage limits; cut does not validate records or their acquisition.

Check `cut --version` for GNU coreutils. Define `input` as an existing local text file and `output` as a fresh distinct path. For records whose first field precedes a literal slash:

~~~bash
umask 077
LC_ALL=C cut -s -d '/' -f 1 -- "$input" > "$output"
status=$?
~~~

`-f` numbers fields from one; `-d` replaces the default tab delimiter. `-s` deliberately omits records with no delimiter. Without it, those records pass through unchanged, even when a later field was requested. Decide whether omission is acceptable, and inspect rejected records separately when completeness matters. A leading delimiter yields an empty first field; an unavailable selected field can also produce empty output rather than an error.

The **illustrative** record `alpha/beta` yields `alpha`. This is delimiter splitting, not path normalization. Repeated delimiters create empty fields; `-d ' '` does not collapse a run of spaces like a whitespace parser. The delimiter must be a single supported character, not a regular expression or a multi-character separator.

Quoted CSV fields, escaped delimiters and structured JSON/XML need their format parser. A slash inside a quoted value remains a delimiter to cut. `-b` selects bytes and is not Unicode character slicing; do not substitute it for a text contract without checking encoding and implementation behavior.

Check status and diagnostics before consuming the output; a failed read can leave partial data. Never redirect onto the input or an alias, because the shell truncates the destination first. In a pipeline, retain the producer's status separately or use the task's deliberate pipefail handling. A successful projection of an incomplete producer is still incomplete.

Human-readable service tables can mix states and protocols. Field extraction alone cannot establish that every selected port was open, that a scan finished or that rows belong to one host. Use the source tool's structured output for those associations.

Reference: [GNU cut packaged manual](https://manpages.debian.org/bookworm/coreutils/cut.1.en.html); installed help resolves implementation differences.
