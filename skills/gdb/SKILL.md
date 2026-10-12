---
name: gdb
description: Examine Linux native core dumps or a controlled live reproduction with GDB. Use for crashes, stack traces, missing or relocated module symbols, instruction boundaries, controlled execution changes and before/after memory evidence with matching artifacts.
---

# GDB native analysis

Read this entire SKILL.md before acting. Select offline core inspection or the conditional live procedure below, and read that reference fully before executing a target. Finish with build/stop context and supporting state, not a backtrace or discovered string alone.

For missing external/library symbols, read [matching separate debug files](references/separate-debug-files.md) fully before selecting or relocating debug artifacts.

For symbols from a module already loaded in an approved remote kernel fixture, read [loaded module symbols](references/loaded-module-symbols.md) fully before correlating its current section addresses. Starting that fixture and loading modules are separate tasks.

For an existing core, establish that it and the executable come from the same build; filenames or the absence of a GDB warning are insufficient. GDB must support the target architecture/format. Source-level interpretation needs matching debug information. For an explicitly requested controlled reproduction, including selecting a forked worker, use [live instruction and memory inspection](references/live-debugging.md). For an explicitly requested change to the next instruction, read [controlled execution changes](references/control-flow.md) fully as well as the live procedure. Core collection is outside this skill's scope.

## Inspect the core

In the same shell invocation, define `binary` and `core` as the actual absolute artifact paths, and `report` as a fresh output file. Record `gdb --version` with the investigation.

~~~bash
gdb -q -nx -batch -iex 'set auto-load off' -ex 'info files' -ex 'info threads' -ex 'thread apply all bt 12' "$binary" "$core" > "$report" 2>&1
~~~

This reads the artifacts and writes the report without attaching to or restarting a process. Startup and automatic script loading are disabled for a predictable inspection. Check the exit status and saved report. The 12-frame limit is a starting point; expand a relevant stack if it omits a needed caller.

## Follow an application frame to a conclusion

Suppose the first report identifies an assertion failure and an application frame `item_at`. The following abbreviated output is **illustrative**, not an executed capture:

~~~text
Program terminated with signal SIGABRT, Aborted.
#0 ... in ... libc ...
...
#3 item_at (items=..., length=4, index=4) at list.c:18
18      assert(index < length);
~~~

The library frame locates the abort mechanism. Select the application frame to inspect the failed condition. Define `thread_id` and `frame_id` from the actual report (1 and 3 in this illustration), and `detail_report` as a new output:

~~~bash
gdb -q -nx -batch -iex 'set auto-load off' -ex "thread $thread_id" -ex "frame $frame_id" -ex 'info args' -ex 'info locals' -ex 'list' "$binary" "$core" > "$detail_report" 2>&1
~~~

With matching source and available values confirming `length=4`, `index=4` and the assertion, the supported conclusion is that the index equals the length at this check. This explains the assertion failure; it does not establish how the index acquired that value. Follow the source and the next relevant caller frame to investigate its origin. Repeated batch calls against an offline core need no persistent session.

If the application frame instead shows `??`, or the index is `<optimized out>`, do not reuse the illustrated explanation. Retain the stop address/module and obtainable state; obtain matching debug artifacts or a controlled reproduction. `list` failing because source files are absent is different from missing debug symbols: argument names/values may still be available. Never substitute a similarly named binary merely to obtain a prettier trace.

If loading fails, inspect GDB's error, path readability and target format/architecture. If output is truncated or times out, inspect the retained report or query selected threads/frames; missing output is incomplete evidence.

Report the build-match status, signal/stop context, relevant frame and supporting state. A backtrace alone does not prove root cause. If the evidence only locates the crash, identify the missing artifact or reproduction needed to explain it.

For command details, use the matching GDB manual's [frame inspection](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Frame-Info.html) and [backtrace](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Backtrace.html) sections.
