---
name: strace
description: Trace Linux file and network system calls to identify actual config paths and failed operations. Use when source/build assumptions disagree with runtime behaviour or acquired traces need descriptor, byte-count and process context.
---

# Trace the operation that fails

Read this entire SKILL.md before acting. Choose controlled capture or review of an existing trace; capture requires the intended command/account, while offline review needs the original trace and its capture options when available. Finish with the relevant call, return value and process/descriptor context; identify truncation or missing context explicitly.

For a new capture, use the installed `strace --version` and help to confirm available filters. Start by launching a short, reproducible command under the same account and environment as the failure. Tracing executes that command, including its network requests and writes; it is not a dry run.

Define `cmd` as a Bash array containing the actual executable and separate arguments, and `trace` as a new absolute output filename. For example, set the array from the approved reproduction rather than constructing an `eval` string:

~~~bash
umask 077
strace -f -s 256 -e trace=%file,%network -o "$trace" -- "${cmd[@]}"
~~~

`-f` follows child processes; `-o` separates trace output from the program's stdout/stderr. This filter exposes filename and network calls, not every read/write. Expand it to selected `read`, `write` or descriptor calls only when needed. `-s` limits string rendering, not trace duration or file growth.

Interpret the call **and its return value**. An `openat` ending in `ENOENT` proves an attempted lookup, not that the program needs that particular file; many programs try several fallback paths. `EACCES` identifies a denied operation. A successful open does not prove a config value was accepted. Follow subsequent calls and correlate with the program's own error.

Record the concrete path seen in the trace. Config locations can be compiled in and differ from another machine's manual or walkthrough. A failed `connect` identifies a destination attempt, not the application protocol's final outcome.

For a running process, `-p PID` changes this into an attachment and needs appropriate ptrace permission. Check ownership, namespace and ptrace policy before assuming root is required. Tracing can affect timing and privileged-program behaviour. Prefer a disposable reproduction; protect traces containing arguments or payloads, stop when the needed event is captured and retain the process outcome alongside the trace.

When a privileged helper behaves differently under tracing, add `%creds` to the filter for an already approved, non-destructive reproduction. Linux can suppress set-user-ID/set-group-ID and file-capability transitions when the process is ptraced. An **illustrative** sequence `setreuid(...) = -1 EPERM`, then `access(..., R_OK) = -1 EACCES`, describes that traced context; it does not prove the file is absent or normally unreadable by the helper. `access()` tests real IDs, while an actual open normally uses effective credentials; `faccessat` flags can change that comparison. Preserve the failed identity transition before interpreting the path check.

A final `exit_group(0)` only reports the program's chosen status, even if it printed an error. Inspect ownership/mode, mount restrictions and the helper's code before deciding on another execution. Do not rerun a database-reset/delete action outside the tracer merely to recover its usual privileges. See [execve privilege rules](https://man7.org/linux/man-pages/man2/execve.2.html) and [access identity semantics](https://man7.org/linux/man-pages/man2/access.2.html).

## Interpret an acquired input trace

Set `trace` to the existing trace copy. Locate candidate reads without altering it:

~~~bash
grep -nF -C 2 -- 'read(0' "$trace"
~~~

This is a text locator, not a syscall parser. No matches do not establish that no input was read: filters, formatting or another descriptor may account for it. Review surrounding PID and open/dup/close calls where captured. Descriptor 0 can refer to a terminal, pipe, file or socket; it does not inherently mean keyboard input.

**Illustrative:** `read(0, "STATUS\n", 4096) = 7` reports seven bytes returned, not 4096. A shorter positive read is valid; zero for a positive requested count indicates EOF, and `-1` is an error. Rendered escapes represent bytes, while `...` can mark omitted data. Associate unfinished/resumed calls and descriptor reuse with the correct process; concatenating every displayed read can fabricate a stream. If bytes or context are missing, preserve that limit rather than reconstructing an exact secret from fragments.

Resolve filter and tracing options with the [upstream strace manual](https://github.com/strace/strace/blob/master/doc/strace.1.in).
