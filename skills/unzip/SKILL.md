---
name: unzip
description: Inspect ZIP/JAR member names and integrity, then recover selected files or packaged Spring Boot settings with Info-ZIP UnZip on Linux. Use to distinguish stored names, platform-dependent extraction paths, CRC failures and skipped or partial output.
---

# Inspect the archive before choosing an extraction

Read this entire SKILL.md before acting; reuse complete current context. Check names, size limits and status before extracting selected members. For a Spring Boot application archive, read [packaged configuration](references/spring-boot-config.md) fully before attributing its settings to a running service. Finish with selected bytes, source member and any integrity or coverage limitation.

Use `unzip -v` and `unzip -hh` to identify the implementation, compiled features and environment defaults. BusyBox and other similarly named tools can differ. Info-ZIP's `UNZIP`, `UNZIPOPT`, `ZIPINFO` and `ZIPINFOOPT` variables can inject options; account for them when a command's behavior differs from its written flags. Define `archive` as an absolute path to the preserved ZIP working copy.

~~~bash
unzip -Z -l "$archive"
unzip -Z -1 "$archive"
~~~

`-Z` must be first and switches to ZipInfo options. The long listing exposes member attributes and compressed/uncompressed sizes; `-1` lists names. Inspect unexpected sizes, symlinks, duplicate names and paths before expanding data. Names can contain whitespace, newlines or terminal controls, and display/encoding transformations can obscure them; a displayed line is not always one member or its exact original byte representation. Use a ZIP metadata parser with escaped strings if exact names matter, and preserve the original archive.

A member displayed as `C:\data\report.txt` is not evidence that Linux wrote to a Windows drive. Rooted paths, backslashes, case collisions and parent components are interpreted by the eventual extractor and destination OS. A successful local extraction does not validate another application's custom extraction code. If reviewing that application, compare the recorded member name to its path construction and containment checks.

# Distinguish integrity from a safe destination

After checking the size budget, test the contents without writing member files:

~~~bash
unzip -t "$archive"
~~~

This decompresses entries and checks their stored CRCs; it still consumes resources. A clean result establishes that the tested data matched those checks, not authenticity, safe paths, benign contents or application acceptance. Inspect the status and messages. Unsupported compression/encryption, missing volumes and password failures mean incomplete coverage, not necessarily damaged bytes. A CRC failure requires a fresh source or explicit partial-recovery decision; do not treat the output as verified.

# Recover selected reviewed members

For an inspected archive with ordinary relative paths and bounded contents, define `member` as the exact reviewed member name and `destination` as a new directory under a private working parent:

~~~bash
mkdir -- "$destination" && unzip -n "$archive" "$member" -d "$destination"
~~~

Quoting prevents shell expansion, but UnZip still interprets wildcard characters in member selectors. Verify the matched names; names containing pattern characters need this implementation's escaping rules. `-n` skips existing files without asking: that is not proof that the directory matches the archive, especially with duplicate/colliding names. A new empty directory reduces ambiguity; check status, extracted paths and content before using the result. Interrupted or failed extraction can leave partial files.

Do not use `-:` to resolve path warnings: it permits parent-directory traversal. `-d` selects a destination but is not a sandbox, and `-j` removes path components and can create collisions. Avoid `-a` when preserving bytes; it converts text. `-o` permits replacement and changes the recovery task.

For one reviewed regular member, `unzip -p "$archive" "$member" > "$output"` writes its data to a chosen fresh file without recreating the archive path. Multiple matches or duplicate names can concatenate data; check the listing and status, and do not consume partial output after an error. This approach still decompresses untrusted data and is not a general archive-security boundary. Use the installed extended help and [Info-ZIP documentation](https://infozip.sourceforge.net/UnZip.html) for format/build differences.
