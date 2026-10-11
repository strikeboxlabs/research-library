---
name: kill
description: Signal one identified owned process or Bash job and verify its termination separately. Use when a suspended collector, stale PID or successful signal request is confused with cleanup.
---

# Stop the selected owned job

Read this entire SKILL.md before acting. Require ownership/stop authority and a current process or job identity. This procedure uses Bash's builtin; inspect `type kill` and `help kill` to confirm it. No conditional resources are required. Finish with signal status and verified exit, including any unresolved children.

For an owned job in this interactive shell:

~~~bash
jobs -l
~~~

Define `job` as the exact observed jobspec, for example `%1` only if that row is the intended collector. Then:

~~~bash
kill -s TERM -- "$job"
signal_status=$?
wait -f "$job"
exit_status=$?
~~~

A successful kill means the signal request succeeded, not that the job already exited. `wait -f` waits for termination rather than a job-control state change, and can block; preserve its result and inspect a job that does not stop within the task's window. A terminated child can give wait a nonzero status. If stopped, the job may need deliberate continuation to handle TERM; inspect its state rather than repeatedly launching replacements. A jobspec is local to this shell, while a numeric PID can be reused. Do not use PID zero, negative values or broad names for a one-process task. Sending a signal to one numeric PID does not guarantee all descendants ended. Prefer the application's graceful stop mechanism when it has one.

Reference: [Bash jobs, kill and wait](https://manpages.debian.org/bookworm/bash/bash.1.en.html).
