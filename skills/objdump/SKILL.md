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

`-T` shows dynamic symbols; `-R` shows dynamic relocations. A decompiler label such as an **illustrative** `sub_1ff0` may represent a linkage stub rather than application logic. Follow the actual referenced relocation/import and inspect caller arguments and return-value handling. A grep of one address loses this relationship. Static binaries or unsupported formats may need a different symbol/import view; an absent table does not prove an absent capability.

Interpret the identified API using the target OS. For example, OpenBSD `unveil(path, "r")` restricts filesystem visibility; it does not grant permission to every file beneath that path. Other calls, more specific rules, existing descriptors, process credentials and application checks affect the conclusion. A found import is not proof the restriction was successfully installed at runtime. See [OpenBSD unveil](https://man.openbsd.org/unveil.2) for a BSD artifact; do not impose those semantics on a Linux syscall merely because the CPU matches.

See [GNU objdump options and interpretation](https://sourceware.org/binutils/docs/binutils/objdump.html).
