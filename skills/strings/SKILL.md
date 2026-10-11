---
name: strings
description: Triage binary files with GNU strings while retaining offsets and checking alternate encodings. Use when paths, error messages or UTF-16 text guide subsequent binary analysis.
---

# GNU strings binary triage

Read this entire SKILL.md before acting. Select the actual artifact and encoding/offset options, preserve its source identity, and finish with the needed text/context and supported conclusion. For database/cache ownership, the structured-record step below is required before assigning an extracted verifier to an account; text adjacency alone is insufficient.

Check `strings --version`; GNU binutils flags are not identical to Windows Sysinternals `strings.exe`. Define `binary` as an absolute path to the artifact copy, and `ascii_output`/`wide_output` as fresh private files:

~~~bash
umask 077
strings -a -n 6 -t x "$binary" >"$ascii_output"
strings -a -n 6 -t x -e l "$binary" >"$wide_output"
~~~

`-a` scans the whole file rather than depending on build-specific section defaults. `-n` sets the minimum character run, and `-t x` emits **hexadecimal file offsets**. `-e l` uses lowercase letter l for 16-bit little-endian text; it is not digit one. This second pass often matters for Windows binaries. Keep the outputs separate so encoding and offsets remain attributable.

Search the outputs for an observed error message, path component or configuration key, then examine nearby strings and the corresponding region in a format-aware tool. Use `-t x` explicitly rather than ambiguous cross-implementation `-o`. File offsets are not automatically PE RVAs or runtime virtual addresses; map sections/load addresses before setting a debugger breakpoint.

Embedded library names, C++ namespace text or managed-runtime markers are leads, not proof of the source language or an executed code path. A string naming a DLL does not establish that it is loaded, from which directory, or under which identity. Confirm those claims through imports, disassembly/decompilation or observed file access as appropriate.

No match can mean the wrong encoding/minimum length, compression, encryption, runtime construction or an incomplete artifact. Lower the minimum or choose another encoding based on evidence; do not conclude the application lacks a capability solely from absent strings. Preserve the original file/hash and record the exact extraction options. Running `strings` does not require executing the artifact.

Select one acquired crash artifact instead of a wildcard over every report. An Apport `.crash` report can contain readable metadata plus encoded/compressed binary fields; strings on that report does not decode a core dump or reconstruct complete source. Correlate its executable, process/time and field identity before attributing a command string. Use the format's parser for the selected binary field when required; preserve the report. A printable command line can be observed data without proof every command ran. See [Apport report encoding](https://github.com/canonical/apport/blob/main/problem_report.py).

For a database or cache, text extraction does not preserve logical records. `sort -u` destroys original order and repetition, and `head` limits the view; neither identifies the account associated with a password-like string. Even adjacent file offsets can belong to stale/deleted pages or unrelated records. Use a format-aware reader on a consistent working copy to recover the DN/row and named attribute before assigning ownership or choosing a password-hash mode. An SSSD cache is an LDB database; a structured `ldbsearch` query can retain that association, whereas `strings` is only a lead.

Resolve encoding/offset options with the [GNU binutils strings manual](https://sourceware.org/binutils/docs/binutils/strings.html).
