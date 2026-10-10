---
name: ldd
description: Resolve shared-library dependencies of trusted Linux ELF programs with ldd. Use to diagnose missing libraries, unexpected resolved paths and the limits of dependency traces for privileged launches.
---

# Trace a trusted program's dependencies

Read this entire SKILL.md before acting. Establish that the executable, interpreter and candidate libraries are trusted for loader-based inspection. Finish with the exact artifact, host/launch context and resolved or missing dependency; a trace does not prove that a function ran or that a privileged launch uses the same mapping.

For untrusted artifacts, use static `readelf -W -d "$binary"` or `objdump -p "$binary"` instead. They show direct dependency names without resolving the whole tree. Some ldd implementations/interpreters can execute the program; even ordinary tracing involves the loader and dependencies. Do not run it as root just to inspect a suspect executable.

Define `binary` as the selected trusted absolute ELF path and `report` as a fresh output file:

~~~bash
ldd --version
ldd "$binary" > "$report" 2>&1
~~~

Check status and the full report. **Illustrative** distinctions:

~~~text
libexample.so => /srv/approved-libs/libexample.so (0x00007f0000000000)
libother.so => not found
~~~

The first identifies this trace's chosen object; the address is session-specific. The second is unresolved, not proof that the library is absent from the entire host. Check ELF architecture/interpreter, direct NEEDED names, RPATH/RUNPATH, relevant environment and cache. A library copied onto disk need not be indexed or compatible. `not a dynamic executable` can reflect a static binary, incompatible format or tracing failure; inspect the artifact rather than treating it as a complete library inventory.

`ldd -v "$binary"` adds version requirements. `-r` performs data/function relocations and reports missing symbols; select it only when that loader activity is intended. Resolving a library with the right filename does not establish its ABI or symbol versions match.

For set-user-ID/capability programs, an ordinary user's ldd trace is not an actual privileged execution. The loader's secure mode can ignore `LD_LIBRARY_PATH` and other variables; tracing, a copied binary, a debugger and a direct launch can differ. Capture actual launch evidence when the task concerns privilege or a called function. If a cached path changes, compare the same executable and environment before/after, then separately establish what the approved normal launch does.

See the [ldd manual and execution caveat](https://manpages.debian.org/bookworm/manpages/ldd.1.en.html) and [loader search/secure-mode rules](https://manpages.debian.org/bookworm/manpages/ld.so.8.en.html).
