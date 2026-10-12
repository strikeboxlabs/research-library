# Pause a selected guest for GDB

Use the entrypoint's approved kernel/disposable disk and actual boot arguments. Require matching local vmlinux debug symbols, architecture support and a free loopback port. A boot image and its symbol-bearing ELF serve different purposes. Retain kernel build identity and its runtime relocation state.

Add these options to the intended QEMU launch:

~~~text
-gdb tcp:127.0.0.1:1234 -S
~~~

Here -S pauses the CPU until a debugger resumes it. -gdb selects the endpoint; it does not pause by itself. The shorthand -s selects port 1234 without this explicit loopback address, so do not assume the shorthand enforces local-only access. The debug connection has no authentication and controls the guest.

Define `symbols` as the matching absolute ELF and start GDB:

~~~bash
gdb -q -nx -iex 'set auto-load off' "$symbols"
~~~

In that session:

~~~text
target remote 127.0.0.1:1234
info registers
info files
continue
~~~

Confirm connection and target architecture before resuming. Connection refusal needs endpoint/process diagnosis; absent or misleading symbols need build/relocation diagnosis. Do not change kernel mitigation settings to make a mismatched symbol address appear valid. Continuing executes the guest; no boot success exists until the console establishes it. For ordinary guest userspace debugging, running GDB inside the guest is often more suitable than following the entire kernel's CPU state.

When done, account for the debugger and QEMU guest; disconnecting a debugger alone does not shut down the VM. See [QEMU GDB behavior](https://www.qemu.org/docs/master/system/gdb.html).
