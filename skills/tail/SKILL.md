---
name: tail
description: Read a bounded log suffix or follow a selected GNU/Linux log with tail. Use for scheduled-job errors, truncation and rotation without mistaking silence for success.
---

# Observe a selected log writer

Read this entire SKILL.md before acting; reuse complete current context. Identify the actual log path, writer and observation window. Capture relevant lines/diagnostics and stop the owned follower when the question is answered or the window ends; no output is not a successful job result.

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

Preserve observation timestamps and the exact file/error. Missing permissions/path, delayed buffering, no invocation and a successful quiet command are distinct possibilities. Stop this follower with Ctrl-C or the tracked worker session; `--pid` is useful only when the relevant writer PID and that implementation's support are established.

Reference: [GNU tail](https://www.gnu.org/software/coreutils/manual/html_node/tail-invocation.html); installed help resolves implementation differences.
