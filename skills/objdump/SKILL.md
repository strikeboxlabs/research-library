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

See [GNU objdump options and interpretation](https://sourceware.org/binutils/docs/binutils/objdump.html).
