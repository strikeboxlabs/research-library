---
name: asar
description: List an acquired Electron ASAR archive and extract selected source files or a reviewed ordinary archive for static inspection. Use when app.asar hides package metadata, entrypoints or client request code.
---

# Inspect the acquired Electron archive

Read this entire SKILL.md before acting. Require the acquired archive, trusted installed ASAR CLI/runtime and fresh private extraction directory. No conditional resources are required. Finish with archive/member identity, command status and extracted source coverage; extraction does not launch the application or establish server behavior.

Check `asar --version` and `asar --help`. Current `@electron/asar` requires Node 22.12.0 or later; the historical unscoped `asar` package is a different installation identity. Installing either is a separate task. Define `archive` as the absolute acquired file path:

~~~bash
asar list "$archive"
status=$?
~~~

Read the complete listing and check status. ASAR is an archive, rather than encrypted or necessarily compiled source. Some entries can depend on an adjacent `.asar.unpacked` tree; its absence leaves extraction incomplete.

For one selected ordinary member, define `member` as its archive-relative path and `output_dir` as a new absolute directory:

~~~bash
umask 077
mkdir -- "$output_dir" && (
  cd -- "$output_dir" || exit
  asar extract-file "$archive" "$member"
)
status=$?
~~~

This CLI writes the member's basename into the current directory, not its entire archived path. Use a fresh directory for each member when basenames collide. Require success and inspect the new ordinary file before reading it as text.

For a known ordinary archive with complete entry paths and link metadata reviewed for confinement to the destination, use a fresh `output_dir` for whole extraction:

~~~bash
asar extract "$archive" "$output_dir"
status=$?
~~~

Unknown external links/path escapes or missing unpacked content leave that whole-archive task unresolved; a name listing alone does not validate those properties. Inspect package.json's main field, then its selected entrypoint and referenced client code as text. A bundled endpoint or credential literal is historical source evidence, not a verified current server identity or authorization. Preserve needed redacted findings and coverage gaps. Do not execute extracted scripts to read them.

See [ASAR usage and format](https://github.com/electron/asar) and [CLI output behavior](https://github.com/electron/asar/blob/main/bin/asar.mjs).
