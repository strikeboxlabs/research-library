---
name: sort
description: Sort and deduplicate a selected line-oriented record file with GNU sort while preserving the intended equality rule. Use when sample counts, numeric ordering, locale or pipeline failures make a distinct-record result misleading.
---

# Choose what makes records equal

Read this entire SKILL.md before acting. Establish the input's record framing, whole-line versus selected-field equality, comparison rule and fresh output path. Finish with sort's status, the retained distinct records and their count; report incomplete input or failed output separately. This task has no additional required resources.

Define `input` as an existing absolute line-oriented data file and `output` as a fresh absolute path. For bytewise whole-line deduplication:

~~~bash
sort --version
(set -C; LC_ALL=C sort -u -- "$input" > "$output")
~~~

Check status before counting. A failed read/write can leave partial output; a downstream `wc` succeeding would not repair it. A no-clobber refusal requires a new destination. Blank lines are records too. Sort normally adds a final newline to an unterminated last line, so its output's line count can differ from a raw input newline count.

~~~bash
LC_ALL=C sort -c -u -- "$output"
wc -l < "$output"
~~~

`-u` emits one record per equal comparison key. Locale, `-k`, case folding or numeric options change that equality. Plain C-locale text ordering places `10` before `2`; `-n` changes ordering. Combining `-n -u` can collapse different textual forms of the same number, so omit it when exact record spellings matter. Selected-field deduplication can discard rows whose other fields differ.

A count describes the acquired sample under that comparison rule, not the complete producer's possible outputs or statistical security. Preserve the actual input file rather than silently combining earlier appended runs. For large private inputs, use supported `-T "$temp_dir"` with a defined private temporary directory; sorting can spill data to disk.

See [GNU sort's packaged manual](https://manpages.debian.org/bookworm/coreutils/sort.1.en.html) for equality, locale and option behavior.
