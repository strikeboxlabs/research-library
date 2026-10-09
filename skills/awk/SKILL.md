---
name: awk
description: Filter text with awk while separating data, regular expressions and program source. Use when shell interpolation, CSV quoting or binary data makes a short awk command unsafe or misleading.
---

# Keep the program fixed and choose the match semantics

Identify the implementation before using extensions: `awk` may be gawk, mawk or another implementation. Match the actual data format, not its filename suffix.

Define `input` as an absolute text-file path and `needle` as the literal text to find. For a bounded literal substring search that preserves backslashes in the search value:

~~~bash
AWK_NEEDLE="$needle" awk 'index($0, ENVIRON["AWK_NEEDLE"]) { print; if (++n == 20) exit }' "$input"
~~~

An empty needle matches every record; decide whether that is intended. The 20-match limit makes this a sample, not an exhaustive inventory. Absolute input paths also avoid treating names such as `x=y` as command-line assignments.

When regular-expression matching is intended, use a fixed program and pass the expression as data, for example `awk -v pat="$pattern" '$0 ~ pat' "$input"`, with `pattern` defined and reviewed. `-v` assignments interpret backslash escapes; the environment form above is useful when literal bytes must survive unchanged. Neither shell quoting nor `-v` turns a regex into a literal string. Use field equality for exact field matches instead of a substring search when the schema requires it.

Do not interpolate an application's username into `/.../` program text or build a shell command string around it. Quotes, slashes and other syntax can change the program, its arguments or its file inputs. `system()`, pipes, redirection and `getline` are active operations, not ordinary filtering.

`-F,` does not parse quoted CSV fields or embedded newlines. Use `gawk --csv` only when installed help confirms support, or a CSV-aware parser. CSV mode changes record/field processing and supersedes normal FS/RS assumptions.

Awk prints records with an output record separator and is not a byte-preserving file-transfer tool. A binary archive returned through an awk-backed endpoint may be altered or truncated even if the HTTP request succeeds. Check the acquired file's format, size and integrity before blaming tar or gzip.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Awkward pp. 13–18. Sources: GNU [variable passing](https://www.gnu.org/software/gawk/manual/html_node/Using-Shell-Variables.html), [string functions](https://www.gnu.org/software/gawk/manual/html_node/String-Functions.html), [CSV support](https://www.gnu.org/software/gawk/manual/html_node/Comma-Separated-Fields.html), [escape processing](https://www.gnu.org/software/gawk/manual/gawk.html).
