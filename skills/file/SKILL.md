---
name: file
description: Classify downloaded or recovered artifacts with file while distinguishing format hints from integrity and runtime compatibility. Use especially when a managed .NET assembly is labelled PE32 or a failed transfer looks executable.
---

# Treat the label as a format finding

Read this entire SKILL.md before acting; reuse complete current context. Classify the preserved file with deliberate link handling, then use the relevant format reader before claiming integrity or runtime compatibility. Finish with the label, corroborating result and any unresolved limitation; a missing or partial input is not a verified artifact.

Check `file --version`, including the magic database location. Identify the exact captured artifact and preserve its origin, size and checksum. A download named `.dll` might contain an HTTP error page; an executable-looking header does not establish that the full transfer completed.

Define `artifact` as the existing working-copy path:

~~~bash
file -E -h -- "$artifact"
~~~

`-h` inspects a symbolic link itself. Use `-L` deliberately when the intended input is its target; the default can change with `POSIXLY_CORRECT`. `-E` makes filesystem errors fail instead of merely printing diagnostics with an otherwise successful exit. Retain stderr and the reported type; a zero status is not an integrity check.

`PE32 ... Mono/.Net assembly, for MS Windows` describes recognizable container/metadata conventions. It does **not** prove a managed assembly is Windows-only or requires a 32-bit Linux runtime. Determine the managed target framework, platform flags, native dependencies and application APIs with a suitable assembly reader. Conversely, not every `.dll` is managed or portable, and a class library need not be runnable as an application.

For an **illustrative** `ELF 64-bit LSB ... x86-64 ... interpreter /lib64/ld-linux-x86-64.so.2` result, class, byte order, machine and loader are separate facts. If a narrative calls that artifact 32-bit, resolve the disagreement against the actual file headers before selecting a debugger/runtime:

~~~bash
readelf -W -h -l "$artifact"
~~~

Read `Class`, `Data`, `Machine` and the requested interpreter together. A file recovered from a Windows host can still be a Linux ELF; its storage host does not choose its format. A GNU/Linux ABI note is not the running host's kernel version. `not stripped` does not promise complete source-level debug information. Inspect symbol/debug sections before choosing source-level debugging. See the [ELF classifier](https://github.com/file/file/blob/master/src/readelf.c) and [GNU readelf options](https://sourceware.org/binutils/docs/binutils/readelf.html).

A `Java archive data (JAR)` label identifies a container signature; it does not establish an intact transfer or parseable Java classes. After checking archive sizes, `unzip -t "$artifact"` checks the ZIP members' stored CRCs. A truncated JAR may still receive a convincing label. Only proceed to a Java decompiler once the container result is understood; CRC success still does not authenticate the archive or prove every method can be reconstructed.

For a `Vim swap file` result, recorded version, user, host, PID and original filename describe the artifact's embedded metadata. They do not authenticate the last editor, prove a crash, identify a current process or establish complete recoverability. Preserve the ordinary file and any matching original for a controlled editor recovery; a filename ending `.swp` alone is weaker evidence than the recognized header.

For MIME-based routing, use `--mime-type` with the same explicit link handling. `application/octet-stream` or `data` means classification is limited, not that the artifact is empty or unusable. The default classifier stops at a successful test; `-k` can expose additional matches but is not a validator for every embedded object.

An OLE/Compound File result on `.msg` can identify an Outlook message container, not an "OLE2 PDF." Use an appropriate message reader to recover its properties, body and attachments. A converted PDF is a derivative: preserve the original and distinguish embedded message dates from conversion timestamps. See Microsoft's [MSG compound-file structure](https://learn.microsoft.com/en-us/openspecs/exchange_server_protocols/ms-oxmsg/cd44ec9f-01bb-4ea3-b335-87cfeb827594).

A recognizable image prefix can label a mixed-format or malformed file as GIF. Report that as classification, then use the intended image decoder; the label does not prove valid pixels or exclude executable/archive content elsewhere in the bytes.

Do not add `-z` or `-s` indiscriminately: compressed-content inspection can invoke decompressors, while special-file reads can touch devices/FIFOs. Start with the saved ordinary file. Finish by selecting the appropriate parser and checking its result; do not execute an artifact merely to confirm file's guess.

Consult the [file manual](https://github.com/file/file/blob/master/doc/file.man) when option defaults or classifier behavior differ.
