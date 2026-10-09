---
name: readelf
description: Inspect ELF headers, load segments, symbols and section bytes with GNU readelf. Use when file offsets, virtual addresses, PIE relocation or zero-filled data are being confused.
---

# Establish the ELF layout

Define `binary` as the existing ELF artifact copy:

~~~bash
readelf --version
readelf -W -h -l -S "$binary"
~~~

Read the class, byte order, machine and object type together. An ELF header is not a promise that the file can execute on this Linux host: a foreign OS ABI, interpreter or dependency can still differ. `ET_DYN` can describe a shared object or a position-independent executable; inspect program headers/interpreter information rather than treating that field alone as a complete classification.

Sections describe file organization; program headers describe loadable segments. For an address inside a file-backed `PT_LOAD` range, map the linked virtual address using that segment's `p_offset + (address - p_vaddr)`. Check the range against `p_filesz`, not only `p_memsz`: extra in-memory bytes can be zero-filled and have no corresponding file content. A relocated runtime address needs its load bias removed first.

For a named section observed in the table, define `section` and inspect its bytes:

~~~bash
readelf -W -x "$section" "$binary"
readelf -W -r "$binary"
~~~

The hex dump is on-disk section content; `-x` does not apply relocations. It does not show bytes that the running program later writes there. In Attended, a static `.data` address was followed by a GDB memory check after input processing; those are two distinct pieces of evidence. Do not transfer that fixed address to a rebuilt or relocated program.

Use `readelf -W -s "$binary"` for available symbols and `--dyn-syms` for dynamic symbols. Stripping can remove one symbol table while imports/dynamic symbols remain; absence of a local symbol does not mean absence of the behavior. `-W` avoids truncated/wrapped table fields that can break simple parsing.

Finish with artifact identity, relevant segment/section and the address space being described. Keep claims about runtime contents or permissions separate from file metadata.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Attended p. 24, adapted from OpenBSD. Sources: [GNU readelf](https://sourceware.org/binutils/docs/binutils/readelf.html), [ELF program headers](https://gabi.xinuos.com/elf/07-pheader.html).
