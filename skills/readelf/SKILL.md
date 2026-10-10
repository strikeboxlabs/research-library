---
name: readelf
description: Inspect ELF headers, load segments, symbols and section bytes with GNU readelf. Use when file offsets, virtual addresses, PIE relocation, shared-library metadata or zero-filled data are being confused.
---

# Establish the ELF layout

Read this entire SKILL.md before acting. Use an acquired ELF copy, establish its header/layout, then select section/address analysis or dynamic-library metadata below. Finish with artifact identity, the exact field/bytes and the address space described; missing bytes or runtime context must remain unresolved.

Define `binary` as the existing ELF artifact copy:

~~~bash
readelf --version
readelf -W -h -l -S "$binary"
~~~

Read the class, byte order, machine and object type together. An ELF header is not a promise that the file can execute on this Linux host: a foreign OS ABI, interpreter or dependency can still differ. `ET_DYN` can describe a shared object or a position-independent executable; inspect program headers/interpreter information rather than treating that field alone as a complete classification.

If tables or sections extend beyond EOF, preserve the truncated artifact and check acquisition length/encoding against its source. Appending NUL bytes can silence a bounds error without recovering the missing contents. A parser accepting a padded file does not establish an intact library or trustworthy offsets/symbols; obtain the exact bytes or keep the finding inconclusive.

Sections describe file organization; program headers describe loadable segments. For an address inside a file-backed `PT_LOAD` range, map the linked virtual address using that segment's `p_offset + (address - p_vaddr)`. Check the range against `p_filesz`, not only `p_memsz`: extra in-memory bytes can be zero-filled and have no corresponding file content. A relocated runtime address needs its load bias removed first.

For a named section observed in the table, define `section` and inspect its bytes:

~~~bash
readelf -W -x "$section" "$binary"
readelf -W -r "$binary"
~~~

The hex dump is on-disk section content; `-x` does not apply relocations. It does not show bytes that the running program later writes there. A static `.data` address and a debugger memory check after input processing are distinct pieces of evidence. Do not transfer that fixed address to a rebuilt or relocated program.

## Inspect shared-library metadata without loading it

~~~bash
readelf -W -d "$binary"
readelf -W --dyn-syms "$binary"
~~~

`NEEDED` entries name direct dependencies, not the complete resolved runtime library set. Search paths, loader configuration and preloads can affect what is loaded; an entry in an acquired `/etc/ld.so.preload` does not appear automatically in this artifact's `NEEDED` list. Correlate that configuration with the relevant host and execution context. Use static inspection on suspect copies: `ldd` is unsafe for untrusted executables because some implementations/cases may execute code.

In the symbol table, `UND` indicates an undefined symbol; a defined/exported `read` is different from an import. Neither proves invocation, an effective interposer, a kernel syscall hook or a successful privilege change. Continue into the relevant implementation or already captured runtime evidence before making those claims.

Use `readelf -W -s "$binary"` for other available symbols. Stripping can remove one table while dynamic symbols remain; absence of a local symbol does not establish absence of behavior. `-W` avoids wrapped/truncated table fields. See [loader rules](https://man7.org/linux/man-pages/man8/ld.so.8.html) and [ldd's execution warning](https://man7.org/linux/man-pages/man1/ldd.1.html) when deciding what static metadata can establish.

Finish with artifact identity, relevant segment/section and the address space being described. Keep claims about runtime contents or permissions separate from file metadata.

Consult the option and format references: [GNU readelf](https://sourceware.org/binutils/docs/binutils/readelf.html), [ELF program headers](https://gabi.xinuos.com/elf/07-pheader.html).
