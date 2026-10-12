---
name: tail
description: Read a bounded log suffix, follow a selected GNU/Linux log, or extract a binary suffix from a verified byte boundary with tail.
---

# Read a file suffix or observe a log writer

Read this entire SKILL.md before acting; reuse complete current context. For logs, identify the path, writer and observation window; stop the owned follower at completion. For binary extraction, establish the format's byte boundary and preserve the original. No conditional resources are required. Finish with relevant output/diagnostics and coverage limits; no output is not a successful job result.

## Extract from a verified byte boundary

Define `source` as an acquired local file, `first_byte` as a positive one-based position justified by its format, and `suffix_file` as a fresh output path:

~~~bash
tail -c "+$first_byte" -- "$source" > "$suffix_file"
~~~

`-c +2` starts at byte two, skipping exactly one byte. Without the plus, `-c 2` selects the final two bytes; `-n` counts lines. Check exit status and expected output length before parsing the suffix. An offset beyond EOF can yield empty output without validating your format assumption. Avoid text decoding or shell variables for binary bytes; do not strip a header simply to force a comparison to match.

## Observe a selected log writer

Define `log_file` as the selected absolute file. First take a finite suffix:

~~~bash
tail -n 40 -- "$log_file"
~~~

For subsequent events only, keep the follower foreground and apply the worker's execution/output budget:

~~~bash
tail -n 0 -F -- "$log_file"
~~~

GNU `-F` follows the filename and retries when it disappears. Plain `-f` follows the opened descriptor, so a renamed old log can stay selected while new writes go elsewhere. Choose descriptor following deliberately when that old file is the evidence. `-n 0` omits existing lines; use the snapshot to avoid losing prior context.

An in-place truncation can reset the reader, but erased bytes cannot be recovered by tail. A writer that immediately clears its error log can race the follower. Correlate scheduled-job timing, exit status and separate captured streams; two one-minute-spaced files suggest a cadence but do not prove the scheduler configuration.

For date-named application logs, select the actual generated filename and retain the writer's date/timezone and configured directory. A glob such as `web-*.log` expands to matching paths when the shell starts tail; it does not discover tomorrow's newly named file. Following by name handles replacement of a selected path, not arbitrary new names. If the application changes its daily filename, stop the owned follower and select the observed new file. A PHP error-log setting and an application request log can name different files; neither path alone proves all requests or variables were recorded.

Preserve observation timestamps and the exact file/error. Missing permissions/path, delayed buffering, no invocation and a successful quiet command are distinct possibilities. Stop this follower with Ctrl-C or the tracked worker session; `--pid` is useful only when the relevant writer PID and that implementation's support are established.

Reference: [GNU tail](https://www.gnu.org/software/coreutils/manual/html_node/tail-invocation.html); installed help resolves implementation differences.
