---
name: file
description: Classify downloaded or recovered artifacts with file while distinguishing format hints from integrity and runtime compatibility. Use especially when a managed .NET assembly is labelled PE32 or a failed transfer looks executable.
---

# Treat the label as a format finding

Check `file --version`, including the magic database location. Identify the exact captured artifact and preserve its origin, size and checksum. A download named `.dll` might contain an HTTP error page; an executable-looking header does not establish that the full transfer completed.

Define `artifact` as the existing working-copy path:

~~~bash
file -E -h -- "$artifact"
~~~

`-h` inspects a symbolic link itself. Use `-L` deliberately when the intended input is its target; the default can change with `POSIXLY_CORRECT`. `-E` makes filesystem errors fail instead of merely printing diagnostics with an otherwise successful exit. Retain stderr and the reported type; a zero status is not an integrity check.

`PE32 ... Mono/.Net assembly, for MS Windows` describes recognizable container/metadata conventions. It does **not** prove a managed assembly is Windows-only or requires a 32-bit Linux runtime. Determine the managed target framework, platform flags, native dependencies and application APIs with a suitable assembly reader. Bagel's .NET 6 DLL was hosted on Linux despite that label. Conversely, not every `.dll` is managed or portable, and a class library need not be runnable as an application.

For an **illustrative** `ELF 64-bit LSB ... x86-64 ... interpreter /lib64/ld-linux-x86-64.so.2` result, class, byte order, machine and loader are separate facts. If a narrative calls that artifact 32-bit, resolve the disagreement against the actual file headers before selecting a debugger/runtime:

~~~bash
readelf -W -h -l "$artifact"
~~~

Read `Class`, `Data`, `Machine` and the requested interpreter together. A file recovered from a Windows host can still be a Linux ELF; its storage host does not choose its format. A GNU/Linux ABI note is not the running host's kernel version. `not stripped` does not promise complete source-level debug information. Inspect symbol/debug sections before choosing source-level debugging. See the [ELF classifier](https://github.com/file/file/blob/master/src/readelf.c) and [GNU readelf options](https://sourceware.org/binutils/docs/binutils/readelf.html).

For MIME-based routing, use `--mime-type` with the same explicit link handling. `application/octet-stream` or `data` means classification is limited, not that the artifact is empty or unusable. The default classifier stops at a successful test; `-k` can expose additional matches but is not a validator for every embedded object.

A recognizable image prefix can label a mixed-format or malformed file as GIF. Report that as classification, then use the intended image decoder; the label does not prove valid pixels or exclude executable/archive content elsewhere in the bytes.

Do not add `-z` or `-s` indiscriminately: compressed-content inspection can invoke decompressors, while special-file reads can touch devices/FIFOs. Start with the saved ordinary file. Finish by selecting the appropriate parser and checking its result; do not execute an artifact merely to confirm file's guess.
