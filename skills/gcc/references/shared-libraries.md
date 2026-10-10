# Build an ABI-matched diagnostic shared library

Use when a selected Linux caller needs a reviewed C shared object. Establish its ELF class/machine, dependency filename/SONAME, exported function signatures and intended return behavior before compiling. A symbol name alone does not disclose the prototype.

Define `source` as the reviewed source, `library` as a fresh output, and `soname` as the caller's observed bare dependency name:

~~~bash
gcc -Wall -Wextra -shared -fPIC -Wl,-soname,"$soname" "$source" -o "$library"
readelf -W -h -d --dyn-syms "$library"
~~~

`-fPIC` produces position-independent object code; `-shared` links a shared object rather than an ordinary executable. SONAME supplies its runtime identity and may control links/cache keys; a differently named file with the wrong SONAME is not necessarily a substitute. Match architecture, exported symbols, symbol versions and dependencies introduced by the build. Do not add `-m32` without the required matching toolchain/libraries.

A controlled marker can return normally from the verified function and print `getuid()`/`geteuid()` via `<unistd.h>`/`<stdio.h>`. It demonstrates a reached call and identity without changing credentials or starting a shell. Keep function parameters/return contract correct so caller behavior is meaningful. Do not copy a snippet using undeclared `setreuid`/`execve`, ignored error returns and NULL argument vectors merely because an old compiler accepted it; Linux's permissive execve NULL-vector behavior is not portable C/process guidance.

Undefined references, relocation errors or implicit-declaration diagnostics require source/link review, not blanket warning suppression. Exported symbols and successful compilation establish an artifact; a separate approved launch establishes that the loader selected it and the intended function ran. A cache update can affect other processes' future launches, and existing running processes may retain their old mapping. Retain the build's significant diagnostics and match its identity to runtime observations.

See [GCC code generation](https://gcc.gnu.org/onlinedocs/gcc/Code-Gen-Options.html), [shared linking](https://gcc.gnu.org/onlinedocs/gcc/Link-Options.html) and [execve API/portability](https://raw.githubusercontent.com/mkerrisk/man-pages/master/man2/execve.2).
