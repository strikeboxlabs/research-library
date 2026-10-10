# Change the next instruction in a controlled reproduction

Use the entrypoint's live-debugging procedure with a matching, owned or explicitly authorized executable. This branch changes execution; it does not describe the program's ordinary successful input. A symbol table can expose `main`/`winner` without source debug information. Starting, stepping and continuing execute specimen code.

After stopping in the relevant application path, use actual symbols and runtime addresses from this persistent session:

~~~text
info functions
disassemble /r main
disassemble /r play
info registers pc sp
x/8i $pc
~~~

The function names are **illustrative**. Follow the real call/branch rather than assuming a `lea` of a symbol calls it. PIE/ASLR means a writeup's address is not your runtime address. Determine arguments, stack alignment, return destination and prior initialization before choosing a different instruction. A hidden success routine that only prints and exits is different from one requiring a prepared frame or valid pointers.

For an expressly selected compatible destination, define GDB's convenience variable `$destination` from its actual runtime symbol/address. For example, `set $destination = &winner` only applies if that function symbol exists. Record the old state, change the PC, inspect it, then continue deliberately:

~~~text
set $original_pc = $pc
set $pc = $destination
x/i $pc
continue
~~~

On x86-64 `$rip` names the instruction-pointer register; RIP is not a "return instruction pointer" or proof a saved return address changed. Setting it changes the next instruction, without creating a normal function-call frame. `jump *address` resumes immediately and does not repair arguments/stack; some architectures have auxiliary PC state that a raw assignment also leaves unchanged. Prefer a reviewed instruction-level destination and inspect the result, rather than treating any function entry as interchangeable.

A printed success marker after this intervention establishes that this modified execution reached the effect. It does not establish a normal-input solution, memory corruption, a durable exploit or privilege escalation. A crash after printing may result from the unprepared return frame; preserve both observations. The old PC is not a whole-process snapshot: restoring it after side effects does not undo execution. Restart the owned fixture with its original input when a clean comparison is needed.

See [GDB changing execution](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Jumping.html) and [register inspection](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Registers.html).
