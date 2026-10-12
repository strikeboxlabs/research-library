---
name: grep
description: Search text and readable log trees with GNU grep and interpret credential-looking records. Use when match logic, recursive scope or partial/error handling changes the conclusion.
---

# State what a selected line proves

Read this entire SKILL.md before acting; reuse complete current context. Select literal/regex and record boundaries deliberately, retain producer/filter errors, and finish with the actual matches or qualified no-match result. A match in partial output does not establish that the producer completed.

For readable application/system logs, backups or suspected misplaced secrets, read [log evidence and credential candidates](references/log-evidence.md) fully before recursive selection or interpreting a candidate.

Define `input` as an existing text file, `needle` as a literal value and `matches` as a fresh output file:

~~~bash
LC_ALL=C grep -nF -- "$needle" "$input" > "$matches"
status=$?
~~~

Inspect `status`: GNU grep normally returns 0 for selected lines, 1 for none, and 2 for an error. Preserve stderr. A pipeline normally exposes only its last command's status unless the shell is configured otherwise. `-q` can return success after a match even if another input error occurs, so avoid it for completeness claims.

`-F` treats punctuation literally; `-E` selects extended regular expressions. Use `-x` for a whole-line match. `-w` means a word-boundary match, not equality of an arbitrary field; underscores and digits participate in word characters. For structured JSON or LDIF, a line match can lose record associations or miss encoded values; use the format's parser.

Multiple `-e` patterns and patterns in a `-f` file are alternatives: **any** can select a line. They do not require every pattern. Successive filters can express AND, but inspect all relevant exit statuses and preserve the unfiltered input.

BackendTwo's word-list filters require several letters and exclude others. That reduces candidates but does not implement positional hints, repeated-letter counts or the full game's rules. Do not report the remaining candidates as a mathematically complete solution without those constraints. Similarly, finding a password-looking string in a failed-login log is a lead, not proof of its owner or present validity.

Binary input can produce a generic match message; `-I` can hide it entirely. Do not reflexively use `-a` on arbitrary bytes and print control characters to a terminal. Decode the actual container first, or retain binary evidence for an appropriate reader. Locale affects classes and case handling; the example's `LC_ALL=C` deliberately uses byte-oriented matching, not language-aware case folding.

Piping results through `grep -v Binary` removes lines containing that case-sensitive text; it does not instruct the first grep to skip binary files. It can discard real text matches and leave other binary diagnostics. Select binary handling on the searching command and retain its errors instead.

## Search captured text, not a filename containing that text

In `grep -F -- "$needle" "$text"`, the last argument names a file. Quoting it prevents shell splitting but does not turn it into input content. A health check that passes captured HTML there can return an error and trigger recovery even when the desired text is present.

If `text` already holds the intended text and `needle` is the literal marker:

~~~bash
printf '%s\n' "$text" | LC_ALL=C grep -nF -- "$needle"
status=$?
~~~

Branch on 0 (selected text), 1 (no selected text), or 2 (grep error); do not combine both nonzero cases into an application-failure diagnosis. Check the producing command's status separately: finding a marker in partial/error output does not make that producer successful. Shell command substitution also discards trailing newlines and cannot preserve NUL bytes; retain a file when exact input matters.

See the [GNU grep input rules](https://www.gnu.org/software/grep/doc/html_node/grep-Programs.html) and [exit-status/pipeline guidance](https://www.gnu.org/software/grep/manual/html_node/Usage.html).
