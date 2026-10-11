---
name: ltrace
description: Trace dynamic library calls in a trusted Linux program to diagnose input handling or dependency behavior. Use when a library-call observation is needed and static symbols alone cannot explain a local application result.
---

# Observe a selected library-call path

Read this entire SKILL.md before acting. Use a trusted, unprivileged executable with reviewed effects and a benign input that reaches the selected path. Finish with the invocation, observed call/result and trace limitations, or the missing permission/runtime condition.

Define `program` as that executable's absolute path and `trace` as a fresh private output file. Add only the reviewed arguments required by the program:

~~~bash
ltrace --version
umask 077
ltrace -s 128 -o "$trace" -- "$program"
~~~

This launches the program. `-s` limits displayed string length; trace output can contain application data. Check stderr and termination status before treating an empty trace as absence of calls. Use `-e 'malloc+free'` when those are the selected calls; quote filters against shell expansion. Use `-f` only when child behavior is part of the task.

ltrace observes intercepted library calls; direct syscalls, inlined functions and unsupported/static linking can escape that view. Argument decoding depends on available function prototypes. Tracing can change timing and privilege behavior, so a traced SUID program does not demonstrate ordinary elevated execution. Do not use a privileged or unknown executable to test a metadata finding.

See the [ltrace manual](https://manpages.debian.org/bookworm/ltrace/ltrace.1.en.html) for filters, prototype configuration and supported tracing options.
