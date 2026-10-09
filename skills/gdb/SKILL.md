---
name: gdb
description: Analyse existing native core dumps with GDB. Use for SIGSEGV or SIGABRT crashes, stack traces, missing symbols, and inconclusive backtraces when a core dump and matching executable are available.
---

# GDB — examine an existing native core dump

Tier: A.

## Identity and selection

- Executable: `gdb`; aliases/search terms: GNU debugger, native crash, core dump, SIGSEGV, SIGABRT, stack trace.
- Use for: locating a crash in a native program using an existing core and its matching executable.
- Choose another approach when: the failure is a managed-runtime exception without a useful native core, or the question is about a running process's historical behaviour. This skill does not cover those investigations.

## Preconditions

Requires Linux with file access and shell command execution. The installed GDB must support the core's target architecture/format. The core and executable must be readable. Establish the executable's build identity from artifact provenance; a familiar filename or absence of a GDB warning alone does not prove a match. Source-level interpretation also needs suitable debug information.

This procedure uses batch commands and local artifacts. It does not require a persistent terminal or a live process. Record `gdb --version` for reproducibility.

## Procedure

### Locate the crash and identify the next useful inspection

**Question:** Which thread/frame and available program state explain where this program stopped, and what further evidence is needed to explain why?

**Inputs and effects:** Define `binary` and `core` as absolute paths to the actual artifacts. Define `report` as a fresh output file in the task's evidence directory. Define them in the same shell invocation as the command. The command reads the artifacts and writes the report; it does not attach to or restart the program.

**Actions:** This batch is a synthesis of documented commands and a worked investigation; it has not been executed here. Disable startup and automatic script loading for a predictable initial inspection. Capture a bounded stack depth from each thread.

~~~bash
gdb -q -nx -batch -iex 'set auto-load off' -ex 'info files' -ex 'info threads' -ex 'thread apply all bt 12' "$binary" "$core" > "$report" 2>&1
~~~

Inspect the exit status and the report. The initial 12-frame limit is an editorial choice; expand a relevant stack when the needed caller is omitted. A completed batch does not itself establish a cause.

**Observe and decide:**

| Observation | Meaning and limits | Next action |
|---|---|---|
| Usable frames and source locations | Localises the stop; the top frame may be where earlier corruption became visible. | Select a relevant application frame and inspect its arguments/locals against the suspected failure. |
| `??` frames or a symbol warning | Available symbols/unwinding may be insufficient. | Record addresses/modules and obtain matching debug artifacts before making a source-level claim. |
| Binary/core mismatch warning or unknown provenance | A reliable correspondence has not been established. | Resolve the build identity; keep the diagnosis provisional. |
| A value is `<optimized out>` | That value is unavailable in this inspection. | Use other available state or an appropriate reproduction; do not substitute an assumed value. |

For a targeted follow-up, reopen the same core in batch mode and add `-ex 'thread N'`, `-ex 'frame M'`, `-ex 'info args'`, and `-ex 'info locals'`, replacing N and M with identifiers actually observed. Keep the startup options and write a new report. Retain the relevant excerpts and compare them with the source or stated hypothesis.

**Finish when:** Report the artifact/build match status, observed signal or stop context, relevant thread/frame, and evidence supporting the conclusion. If the evidence only localises the crash, say what specific additional artifact or reproduction would test the cause. Do not equate the presence of a backtrace with a root-cause finding.

## Failure and recovery

| Failure | Discriminating check | Recovery |
|---|---|---|
| Core cannot be loaded | Inspect the actual GDB error, supplied paths, and target format/architecture. | Correct the artifact or use a GDB build that supports it; retain the failure as evidence. |
| Source-level inspection is unavailable | Check symbol availability and whether the selected frame contains usable debug information. | Obtain matching artifacts or limit the conclusion to the available addresses/state. |
| Output is truncated or the batch times out | Compare the saved report with what the harness returned. | Read the retained file or query selected threads/frames; do not infer absence from missing output. |

## Verification and gaps

- Source review: checked 2026-10-09 against rolling upstream documentation recorded in the provenance companion.
- Execution: not-run. No Linux environment was available in this preparation session.
- Agent evaluation: not-run.
- Known gaps: no measured version/platform matrix, live attach, core collection, remote targets, reverse debugging, or deadlock diagnosis. The recipe and its diagnostic branches still need an isolated Linux execution test.

Sources and claim mapping: [GDB provenance](references/provenance.md). Read for source checks, version conflicts or maintenance.
