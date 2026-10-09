---
name: strace
description: Trace Linux file and network system calls to identify actual config paths and failed operations. Use when source/build assumptions disagree with a program's runtime behaviour.
---

# Trace the operation that fails

Use the installed `strace --version` and help to confirm available filters. Start by launching a short, reproducible command under the same account and environment as the failure. Tracing executes that command, including its network requests and writes; it is not a dry run.

Define `cmd` as a Bash array containing the actual executable and separate arguments, and `trace` as a new absolute output filename. For example, set the array from the approved reproduction rather than constructing an `eval` string:

~~~bash
umask 077
strace -f -s 256 -e trace=%file,%network -o "$trace" -- "${cmd[@]}"
~~~

`-f` follows child processes; `-o` separates trace output from the program's stdout/stderr. This filter exposes filename and network calls, not every read/write. Expand it to selected `read`, `write` or descriptor calls only when needed. `-s` limits string rendering, not trace duration or file growth.

Interpret the call **and its return value**. An `openat` ending in `ENOENT` proves an attempted lookup, not that the program needs that particular file; many programs try several fallback paths. `EACCES` identifies a denied operation. A successful open does not prove a config value was accepted. Follow subsequent calls and correlate with the program's own error.

Record the concrete path seen in the trace. Config locations can be compiled in and differ from another machine's manual or walkthrough. A failed `connect` identifies a destination attempt, not the application protocol's final outcome.

For a running process, `-p PID` changes this into an attachment and needs appropriate ptrace permission. Check ownership, namespace and ptrace policy before assuming root is required. Tracing can affect timing and privileged-program behaviour. Prefer a disposable reproduction; protect traces containing arguments or payloads, stop when the needed event is captured and retain the process outcome alongside the trace.

Documentation reviewed 2026-10-09; Linux execution untested. Case: AdmirerToo p. 19. Source: [upstream strace manual](https://github.com/strace/strace/blob/master/doc/strace.1.in).
