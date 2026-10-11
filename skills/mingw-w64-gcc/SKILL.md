---
name: mingw-w64-gcc
description: Cross-compile a reviewed Windows C++ utility from Linux with a MinGW-w64 GCC driver. Use for target-machine, Windows entrypoint, import-library and produced-artifact discrepancies.
---

# Build for the selected Windows target

Read this entire SKILL.md before acting. Require a reviewed local source/build contract, the intended Windows architecture and an existing matching compiler. Compilation may invoke build helpers; use the trusted project and a fresh output path. Finish with compiler identity, command/status, significant diagnostics and the actual artifact; a build does not establish successful Windows execution.

Define `cxx` as the selected MinGW-w64 C++ driver, commonly named `x86_64-w64-mingw32-g++` for an x86-64 Windows target. Distribution variants may append a threading-model suffix; resolve the actual executable rather than assuming the unsuffixed alias or an installation path.

~~~bash
"$cxx" --version
"$cxx" -dumpmachine
"$cxx" -print-sysroot
~~~

The target machine describes generated code, not the Linux host running the compiler. An empty sysroot print can be valid for that configured compiler; inspect its search paths when headers/libraries are missing. Do not substitute native Linux g++ merely because both accept a .cpp file.

Define `source` as the reviewed C++ file and `output` as a new absolute .exe path. For an ordinary console program whose selected build requires no additional library or Unicode entrypoint:

~~~bash
"$cxx" -Wall -Wextra -Og -g "$source" -o "$output"
~~~

Check exit status immediately and retain warnings. A pre-existing output surviving a failed link is not the new build, which is why the path must be fresh. Missing Windows headers, C++ compilation errors and undefined references are different stages; diagnose the selected source/target dependencies before changing flags.

When the actual project uses Unicode-capable startup, `-municode` predefines UNICODE and selects that startup code; match its entrypoint rather than applying the flag to every program. It does not turn every narrow literal or runtime data stream into Unicode. Console and GUI subsystem selection is separate: -mconsole is the Windows-target default, while -mwindows selects GUI startup/subsystem behavior.

Add only the target import libraries required by the reviewed API calls, after their referencing objects/source. For example, -lsecur32 selects that Windows import library when the source actually requires its APIs; it does not grant token privileges. An undefined reference may be a missing library, incorrect calling convention or entrypoint mismatch. Linux libraries cannot satisfy a Windows-target link simply because their names resemble the dependency.

Identify the produced artifact's architecture/PE subsystem and runtime DLL requirements with the available trusted inspection tools. Record its digest alongside the selected source revision and build options when transferring it. A downloaded executable with a different filename has no proven relationship to this output. Windows loader/runtime testing is a separate selected task; absence of a Windows fixture leaves execution unverified. Do not launch a utility to determine whether its source or behavior is safe.

See [Windows-target options](https://gcc.gnu.org/onlinedocs/gcc/Cygwin-and-MinGW-Options.html), [target/sysroot queries](https://gcc.gnu.org/onlinedocs/gcc/Developer-Options.html) and [link options](https://gcc.gnu.org/onlinedocs/gcc/Link-Options.html).
