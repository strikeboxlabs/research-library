---
name: objdump
description: Inspect object-file headers and bounded disassembly with GNU objdump. Use when raw bytes are mistaken for instructions, source lines are missing or addresses and instruction boundaries need interpretation.
---

# Read the right representation

Read this entire SKILL.md before acting; reuse complete current context. Establish the artifact format and address space, select headers/bytes/disassembly below, and retain the bounded output supporting the requested conclusion. Missing symbols or static-only evidence must remain explicit; this procedure does not establish runtime reachability.

Define `binary` as an existing artifact copy. Establish the object format and architecture before selecting disassembler options:

~~~bash
objdump --version
objdump -f -h "$binary"
~~~

An unsupported format/architecture may require the matching cross-binutils build. Do not force x86 decoding merely because the analysis workstation is x86. Linux tooling can inspect some foreign ELF files without being able to execute them.

The case of the option changes its meaning:

| Option | What it shows |
|---|---|
| `-s` | Section contents as bytes; not instruction disassembly. |
| `-d` | Disassembly of sections expected to contain code. |
| `-D` | Broader disassembly, including data that may decode into plausible but irrelevant instructions. |
| `-S` | Disassembly with source interleaving when matching debug/source information is available. |

For a known symbol, define `symbol` as its actual name:

~~~bash
objdump -d -C --disassemble="$symbol" "$binary"
~~~

For a stripped artifact, use observed **object virtual addresses** `start` and `stop` to bound output:

~~~bash
objdump -d --start-address="$start" --stop-address="$stop" "$binary"
~~~

These are not raw file offsets. Relocation and load bias can make live addresses differ. On x86, explicitly select `-M intel` if needed and keep that choice with the report; AT&T and Intel operand ordering differ. A missing source line in `-S` output does not prove the instruction has no source-level origin.

Check actual instruction bytes, boundaries, operand widths and following instructions. A mnemonic found by grep may hide extra register writes, memory accesses or a return's stack effects. Disassembling from another byte offset can produce a different instruction stream; static output does not prove that execution reaches it. Use matching debugger state for runtime claims and the target OS/architecture ABI for syscall meanings, not a table selected only by CPU family.

## Identify an imported call behind a decompiler label

For a dynamic ELF artifact, compare symbol names and dynamic relocations with the call site and PLT stub:

~~~bash
objdump -T -R "$binary"
objdump -d --start-address="$start" --stop-address="$stop" "$binary"
~~~

`-T` shows dynamic symbols; `-R` shows dynamic relocations. A decompiler label such as an **illustrative** `sub_1ff0` may represent a linkage stub rather than application logic. Follow the actual referenced relocation/import and inspect caller arguments and return-value handling. A PLT address, its associated GOT storage address and the function address currently stored there are different objects; static relocation output alone does not establish the loaded implementation. A grep of one address loses this relationship. Static binaries or unsupported formats may need a different symbol/import view; an absent table does not prove an absent capability.

Distinguish a normal function call through `write@plt` from a kernel `syscall` instruction before applying argument rules. For ordinary integer/pointer arguments on the x86-64 System V ABI, the first registers are RDI, RSI, RDX, RCX, R8 and R9; Linux's x86-64 kernel interface uses R10 for the fourth instead of RCX. Other types, architectures and ABIs need their own rules. Follow the complete function prototype: a length argument is not optional because a screenshot omits its register setup, and a previously held register value is not proof of the intended count. Preserve caller data flow and actual return handling before describing an operation. See the [AMD64 ABI, function calling and Linux kernel interface](https://refspecs.linuxbase.org/elf/x86_64-abi-0.99.pdf).

Interpret the identified API using the target OS. For example, OpenBSD `unveil(path, "r")` restricts filesystem visibility; it does not grant permission to every file beneath that path. Other calls, more specific rules, existing descriptors, process credentials and application checks affect the conclusion. A found import is not proof the restriction was successfully installed at runtime. See [OpenBSD unveil](https://man.openbsd.org/unveil.2) for a BSD artifact; do not impose those semantics on a Linux syscall merely because the CPU matches.

An imported OpenBSD `auth_userokay` is an authentication lead, not the helper's complete policy. Its API takes name, style, type and password; zero means failure and nonzero means success. That is distinct from the helper executable's exit status, which may invert the API result. Inspect caller arguments and return/exit handling before interpreting a PHP `system` status. The imported name alone does not establish a vulnerable revision, selected authentication style or successful login. See [OpenBSD authentication API](https://man.openbsd.org/authenticate.3).

See [GNU objdump options and interpretation](https://sourceware.org/binutils/docs/binutils/objdump.html).
