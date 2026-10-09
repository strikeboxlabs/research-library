---
name: gdb
description: Examine existing Linux native core dumps with GDB. Use for crashes, stack traces, missing symbols and inconclusive frames when a core and matching executable are available.
---

# GDB core analysis

Establish that the core and executable come from the same build; filenames or the absence of a GDB warning are insufficient. GDB must support the core's architecture/format. Source-level interpretation needs matching debug information. This skill covers existing cores; live debugging and core collection are outside its scope.

## Inspect the core

In the same shell invocation, define `binary` and `core` as the actual absolute artifact paths, and `report` as a fresh output file. Record `gdb --version` with the investigation.

~~~bash
gdb -q -nx -batch -iex 'set auto-load off' -ex 'info files' -ex 'info threads' -ex 'thread apply all bt 12' "$binary" "$core" > "$report" 2>&1
~~~

This reads the artifacts and writes the report without attaching to or restarting a process. Startup and automatic script loading are disabled for a predictable inspection. Check the exit status and saved report. The 12-frame limit is a starting point; expand a relevant stack if it omits a needed caller.

| Finding | Interpretation and next step |
|---|---|
| Usable frames/source locations | These locate the stop; earlier corruption may have caused it. Select a relevant application frame and inspect its state. |
| `??` or symbol warnings | Symbols or unwinding may be insufficient. Retain addresses/modules and obtain matching debug artifacts before making source-level claims. |
| Binary/core mismatch or uncertain build identity | Resolve the artifact match before relying on the interpretation. |
| `<optimized out>` | The value is unavailable. Use other state or a suitable reproduction; do not infer the missing value. |

For targeted inspection, reopen the same core with the same startup options and add `-ex 'thread N'`, `-ex 'frame M'`, `-ex 'info args'` and `-ex 'info locals'`. Substitute observed thread/frame identifiers and write a new report. Separate batch calls against an offline core do not require a persistent debugger session.

If loading fails, inspect GDB's error, path readability and target format/architecture. If output is truncated or times out, inspect the retained report or query selected threads/frames; missing output is incomplete evidence.

Report the build-match status, signal/stop context, relevant frame and supporting state. A backtrace alone does not prove root cause. If the evidence only locates the crash, identify the missing artifact or reproduction needed to explain it.

Validation: documentation reviewed; Linux execution and agent performance remain untested. [Sources](references/sources.md) are available for source checks and maintenance.
