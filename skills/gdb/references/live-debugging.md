# Controlled live instruction and memory inspection

Use a matching executable in a Linux fixture where running it is part of the task. Inspecting an OpenBSD binary from Linux does not make it a Linux executable. Starting or continuing a live process executes its code; this procedure is separate from offline core inspection.

Define `binary` as the fixture's absolute executable path and `sample_arg` as one controlled text argument. Omit that argument if the fixture needs none; binary data containing NUL bytes cannot be passed as an ordinary argument.

~~~bash
gdb -q -nx -iex 'set auto-load off' --args "$binary" "$sample_arg"
~~~

In the persistent GDB session, configure and stop at the first instruction:

~~~text
set startup-with-shell off
set disable-randomization off
show args
starti
info files
info registers
x/12i $pc
~~~

Disabling the startup shell avoids shell expansion of the inferior's arguments. With that setting, shell-style redirection in `run` arguments will not provide stdin. `set disable-randomization off` preserves the host's normal ASLR behavior; on supported Linux targets GDB otherwise normally disables randomization. Record that choice because debugger and ordinary launches can have different layouts.

Select an actual symbol with `break function_name`, or an observed **runtime** address with `break *address`, then `continue` only to the intended stop. Substitute names/addresses from this build and session. `start` stops around `main`; initialization code can already have run. A fixed linked address from a writeup may require relocation and is not a reusable runtime breakpoint.

At a stop, use `disassemble /r` for the current function's instruction bytes and `info registers` for state. Inspect a selected readable address with `x/32bx address` before and after the relevant operation. `x/s address` assumes a string and is unsuitable for proving exact binary length or NUL-containing content. `stepi` advances one instruction; `nexti` can run an entire call before stopping. Inspect register widths and all instructions, not just the desired mnemonic.

Keep both observations tied to the same input, stop location and address mapping. Unreadable memory may mean the wrong address, lifetime or mapping; missing symbols require address-level reasoning, not invented variable names. Avoid debugger expressions that call target functions merely to inspect state. Finish by recording the observed change and terminating the owned fixture; this does not establish behavior for another build or launch environment.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Attended pp. 20–25, adapted from OpenBSD. Sources: [starting](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Starting.html), [machine code](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Machine-Code.html), [memory](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Memory.html), [registers](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Registers.html).
