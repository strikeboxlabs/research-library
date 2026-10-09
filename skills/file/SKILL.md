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

For MIME-based routing, use `--mime-type` with the same explicit link handling. `application/octet-stream` or `data` means classification is limited, not that the artifact is empty or unusable. The default classifier stops at a successful test; `-k` can expose additional matches but is not a validator for every embedded object.

A recognizable image prefix can label a mixed-format or malformed file as GIF. Report that as classification, then use the intended image decoder; the label does not prove valid pixels or exclude executable/archive content elsewhere in the bytes.

Do not add `-z` or `-s` indiscriminately: compressed-content inspection can invoke decompressors, while special-file reads can touch devices/FIFOs. Start with the saved ordinary file. Finish by selecting the appropriate parser and checking its result; do not execute an artifact merely to confirm file's guess.

Documentation reviewed 2026-10-09; Linux execution untested. Cases: Bagel p. 8; BigBang pp. 4–7. Sources: [file manual](https://man7.org/linux/man-pages/man1/file.1.html), [.NET portable binaries and native dependencies](https://learn.microsoft.com/en-us/dotnet/core/deploying/), [image-header detection limits](https://www.php.net/manual/en/function.getimagesize.php).
