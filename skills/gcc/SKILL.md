---
name: gcc
description: Compile a selected C utility with GCC and distinguish preprocessing, compilation, linking and runtime compatibility failures. Use when building an existing tool or a diagnostic fixture with the Linux image's available compiler.
---

# Diagnose the build stage before changing flags

Read this entire file before acting. Identify the reviewed source, target architecture and required libraries. Finish with the build command, diagnostics and artifact identity; successful compilation does not establish that running the program is appropriate or correct.

Define `source` as the intended C file and `output` as a new output path. For a debuggable build:

~~~bash
gcc -Wall -Wextra -Og -g "$source" -o "$output"
~~~

`-g` supplies debug information; optimization still affects variable visibility and stepping. Do not remove warnings or disable protections reflexively to get a historical program to build. Compiler errors may expose obsolete APIs or actual defects that need source review.

Separate stages when the error is unclear:

~~~bash
gcc -E "$source" -o "$preprocessed"
gcc -Wall -Wextra -c "$source" -o "$object"
gcc "$object" -o "$output"
~~~

Define the additional paths first. `-E` stops after preprocessing, `-c` produces an object without linking, and the last command links it. A missing header points to include paths/development headers; an undefined reference points to definitions, libraries or link order. Libraries generally belong after the objects that reference them, for example `gcc "$object" -lm -o "$output"` when the source needs the math library. Use `g++` for C++ linking rather than assuming `gcc` adds its runtime libraries.

If a produced binary fails to start, inspect its architecture, requested loader and shared-library requirements. `-m32` requires a working 32-bit toolchain/libraries; a 64-bit kernel alone is insufficient. A binary compiled against newer libc interfaces may not run on an older destination even with the same CPU architecture. Use the controlled image's intended toolchain rather than a guessed compatibility flag.

Compilation and execution are separate task steps. Preserve the source revision and significant build flags with the resulting binary when the investigation depends on reproducing behavior. The compiler can establish a build artifact; it cannot establish that a race, protocol action or privileged operation in that program succeeds.

See [GCC stages](https://gcc.gnu.org/onlinedocs/gcc/Overall-Options.html), [link options](https://gcc.gnu.org/onlinedocs/gcc/Link-Options.html) and [debugging options](https://gcc.gnu.org/onlinedocs/gcc/Debugging-Options.html).
