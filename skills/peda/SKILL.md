---
name: peda
description: Use the installed PEDA GDB extension to correlate x86 registers, disassembly, stack strings and call arguments in a controlled Linux reproduction. Use when a plain trace misses the memory context of a comparison or library call.
---

# PEDA execution context

Read this entire SKILL.md before acting. Select the installed trusted PEDA entry script and matching executable before loading the extension. Starting/stepping runs the target; finish with the same-session stop, actual bytes/arguments and the supported branch or call conclusion. Neither a pretty stack string nor a debugger launch proves normal setuid behavior.

PEDA is a Python extension loaded inside GDB, not an independent executable. Require a compatible Python-enabled GDB and the installed PEDA folder with its resources. Define `peda_entry` as its verified absolute `peda.py` path and `binary` as the reviewed x86 executable in an approved fixture. Load it explicitly for this session rather than appending source-provided paths to global `.gdbinit`:

~~~bash
gdb -q -nx -iex 'set auto-load off' -x "$peda_entry" --args "$binary"
~~~

GDB's script-extension setting must recognize `.py` as Python. Import failure or an unavailable `peda` command is a tool/build gap, not a target finding. Explicit extension loading executes trusted host-side Python despite automatic script loading being disabled. PEDA changes settings/hooks, so select intended process/ASLR/signal behavior after it loads:

~~~text
peda help
set history save off
set startup-with-shell off
set disable-randomization off
show follow-fork-mode
info functions
break main
run
peda context all 8
disassemble /r main
~~~

Use symbols/addresses from this build. If main is unavailable, `starti` establishes a real instruction stop; initialization may run before a main breakpoint. PEDA's context requires a live inferior and supports register/code/stack views. `stepi` advances one instruction; `nexti` can run a whole call. Keep the chosen input and stops together rather than repeatedly restarting with different layouts.

At a selected **call instruction**, `peda dumpargs 2` can display two inferred arguments. This relies on architecture/calling conventions and heuristics, not debug types. Verify addresses/bytes with `info registers`, `x/16i $pc`, `x/32bx address` and, only for a confirmed string, `x/s address`, substituting actual addresses. A stack string can be an input, constant or stale memory; follow the comparison operands, return value and conditional branch before calling it an accepted password. Avoid debugger expressions that call functions just to inspect values.

For a library function, `break function_name`, the stop's module and `info sharedlibrary` help distinguish the PLT stub from the implementation. Resolution, invocation and effective identity are different claims. A copied program can resolve different libraries and lacks the original launch's mode/ownership context; ptracing can suppress setuid effects. Terminate the owned inferior when finished and retain the relevant state/bytes, without publishing recovered secrets.

Use [PEDA's command guide](https://github.com/longld/peda) and [context/argument implementation](https://github.com/longld/peda/blob/master/peda.py) for this extension's supported commands; [GDB Python script loading](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Python-Commands.html) explains explicit loading.
