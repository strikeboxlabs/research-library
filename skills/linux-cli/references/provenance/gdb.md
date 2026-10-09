# GDB core-analysis provenance

Companion to [the GDB card](../gdb.md). The card retains current verification status and material limits; this file supplies the detailed evidence on demand.

## Sources

Reviewed on 2026-10-09. These are rolling upstream manuals, not captured help from an identified installed GDB version. Compatibility with a particular target build remains unmeasured.

- S1: [GDB: Commands to Specify Files](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Files.html), file/symbol/core sections. Supports artifact roles and format/debug-information requirements.
- S2: [GDB: Choosing Files](https://sourceware.org/gdb/current/onlinedocs/gdb.html/File-Options.html), positional arguments and `-iex`/`-ex`. Supports command inputs and early setup.
- S3: [GDB: Choosing Modes](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Mode-Options.html), quiet/startup/batch/version options. Supports `-q`, `-nx`, `-batch` and version reporting.
- S4: [GDB: Backtraces](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Backtrace.html), frame counts, all-thread backtraces, optimized arguments. Supports stack collection and interpretation.
- S5: [GDB: Threads](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Threads.html) and [Startup](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Startup.html), thread selection and early automatic-loading control.
- S6: [GDB: Information About a Frame](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Frame-Info.html), frame selection, arguments and locals. Supports follow-up inspection.
- S7: [GDB: Sample Session](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Sample-Session.html), progression from stopped program to inspecting state. Informs the investigation shape; the offline-core procedure is synthesis.

## Command and claim mapping

| Card section / command / claim | Support | Scope and limits |
|---|---|---|
| Preconditions: core, executable, format and symbols | S1 file/symbol/core sections; S2 positional arguments | Documented artifact roles. Requiring independent build provenance is conservative synthesis; lack of a warning is not proof of a match. |
| `gdb --version`, `-q`, `-nx`, `-batch` | S3 version, quiet, startup and batch options | Documented invocation semantics; no installed-version capture is available. |
| Positional binary/core arguments; `-iex` and `-ex` | S2 choosing files / command execution | Documented inputs and command timing. |
| `set auto-load off` before artifact loading | S5 Startup / early initialization | Documented startup control, combined here with the early command option. |
| `info files` | S1 file information | Reports loaded file information; does not independently establish build provenance. |
| `info threads`, `thread apply all bt 12` | S5 Threads; S4 Backtraces | Documented thread/backtrace commands. The depth of 12 is an editorial bound, not a required diagnostic limit. |
| Usable frames localise the stop; select an application frame | S4 Backtraces; S6 frame information; S7 worked session | The stop location alone does not establish when an earlier fault occurred; the decision branch is diagnostic synthesis. |
| `??` frames, symbol warnings and source-level limits | S1 symbol files; S4 Backtraces | Missing symbols/unwinding are possible limitations, not a unique diagnosis from `??`. |
| `<optimized out>` values | S4 optimized arguments | That value is unavailable in this inspection; do not invent it. |
| `thread N`, `frame M`, `info args`, `info locals` | S5 Threads; S6 frame information | Use identifiers actually observed. Reopening the same offline core for a targeted batch is synthesis. |
| Load failure and unavailable source-level inspection | S1, S2, S4, S6 relevant artifact/stack sections | Error-driven recovery, not a promise that any core can be analysed. |
| Report capture, timeout/truncation recovery, completion evidence | Procedural synthesis using the documented observations above | Shell file capture retains output; a partial report or completed backtrace cannot by itself prove root cause. |

## Execution evidence

Procedure execution: not-run. Agent evaluation: not-run. No Linux environment was available during preparation. The proposed cases are described in the repository's evaluation material; no successful run or compatibility matrix is claimed here.
