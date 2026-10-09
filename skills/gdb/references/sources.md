# GDB sources

Maintenance notes for [the GDB skill](../SKILL.md). Consult when checking a source or updating the guidance.

The following rolling upstream manual sections were reviewed on 2026-10-09. They are not tied to an installed GDB version:

- [Files](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Files.html): executable, core and symbol artifacts; `info files`.
- [File options](https://sourceware.org/gdb/current/onlinedocs/gdb.html/File-Options.html): positional inputs and `-iex`/`-ex` ordering.
- [Mode options](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Mode-Options.html): `-q`, `-nx`, `-batch` and version reporting.
- [Backtraces](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Backtrace.html): stack depth, frame interpretation and optimized-out values.
- [Threads](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Threads.html): thread selection and all-thread backtraces.
- [Startup](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Startup.html): early automatic-loading control.
- [Frame information](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Frame-Info.html): frame selection, arguments and locals.
- [Sample session](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Sample-Session.html): a worked investigation informing the follow-up steps.

The offline-core sequence combines these documented commands with diagnostic judgement. Independent build matching, the initial 12-frame bound and completion criteria are choices made for this procedure. Linux execution and agent evaluation have not been run; compatibility across versions remains unmeasured.
