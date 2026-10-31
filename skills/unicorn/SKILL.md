---
name: "unicorn"
description: "Emulate machine code stubs and shellcode with the Unicorn CPU-emulation library from Python for analysis without execution on the host. Use to trace unpacking stubs, hash loops and architecture-specific code safely."
---

# Unicorn CPU emulation

Installed invocation: `/usr/bin/python3` with the `unicorn` module (Kali package python3-unicorn 2.1.4; `import unicorn`).

Read this entire SKILL.md before acting. Require the code bytes, target architecture and the observation to make (register trace, memory writes, iteration count). Finish with the emulation result and the emulation boundaries chosen.

~~~python
import unicorn
mu = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_64)
mu.mem_map(0x1000, 0x1000)
mu.mem_write(0x1000, code_bytes)
mu.emu_start(0x1000, 0x1000 + len(code_bytes))
print(mu.reg_read(unicorn.x86_const.UC_X86_REG_RAX))
~~~

Unicorn executes only the bytes you map — no syscalls, no external libraries — so emulated code fails where it leaves the mapped region; hook interrupts (`mu.hook_add(unicorn.UC_HOOK_INTR, ...)`) and unmapped-memory events to decide stub behavior at those boundaries instead of crashing the emulator. Architecture/mode constants select the CPU; x86-64 and ARM are the common CTF cases.

Emulation is analysis, not execution on the host: it is the safe way to understand a stub, and the results (traced writes, computed addresses) feed the real analysis in the disassembly skills. An emulation that diverges from real hardware usually means an unhandled boundary, not broken code.

References: [project documentation](https://www.unicorn-engine.org/docs/).
