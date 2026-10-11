---
name: 7z
description: Inspect/extract archives or supported disk images and diagnose 7-Zip backup filename/listfile parsing. Use for format, integrity, password, wildcard and symlink-related discrepancies.
---

# 7-Zip archive triage

Read this entire SKILL.md before acting; reuse complete current context. Select the installed implementation and requested archive task, retain its status/listing and distinguish readable output from a complete valid backup. For backup creation, @listfile arguments or symlink-related diagnostics, read [backup argument parsing](references/backup-arguments.md) fully before that procedure. Keep it unloaded for ordinary archive extraction.

Select the installed implementation: distributions may provide legacy p7zip `7za`/`7z` or upstream `7zz`, with different format support. Define `sevenzip` as its executable name/path and `archive` as the absolute input path. Read the version banner and supported formats:

~~~bash
"$sevenzip" i
"$sevenzip" l -slt "$archive"
~~~

Check the reported archive type, compression/encryption methods, member paths and unpacked sizes. A ZIP extension does not guarantee that every extractor supports its encryption. `unzip` reporting an unsupported method is not proof of a bad password.

For formats with an integrity test, test before extracting. This can read the full input; account for a large image's I/O cost. For encrypted content, provide the known password at the interactive prompt rather than embedding it in a command line:

~~~bash
"$sevenzip" t "$archive"
~~~

After reviewing the listing and any test result, define `destination` as a new extraction directory under the investigation workspace:

~~~bash
mkdir -m 700 "$destination" && "$sevenzip" x "$archive" -o"$destination"
~~~

`x` preserves member directories; `e` flattens them and can create name collisions. The output path is attached to `-o`. Inspect unexpected paths, links and very large expansion before extraction; use an unprivileged workspace. Avoid blanket overwrite switches when reviewing evidence.

For VHD/VHDX, a supported outer container may expose a partition image rather than filesystem files. List each observed layer; do not assume the image is raw NTFS or requires Windows to inspect. When the listing exposes the desired file, add its exact member path to `x` to extract only that member. If another image layer must be extracted first, budget its expanded size and inspect it separately. A readable container is not filesystem consistency or a complete backup; parent/differencing disks and unsupported inner formats can limit recovery. Extracting registry hives should preserve their common acquisition context.

Retain the test/extraction status and error text. Password errors and corruption can present similarly; verify the source transfer, archive parts and supported method before retrying credentials. A successful extraction establishes readable files, not trustworthy contents.

When a spreadsheet receives a ZIP label but extraction reports a header error, retain the original and distinguish a readable directory from valid member data. A recovered or edited candidate must pass `"$sevenzip" t "$archive"` and the intended document parser before calling the recovery complete. A changed `file` label alone is insufficient. Header repair depends on the actual container format and intact remaining structures; the [upstream 7z recovery procedure](https://7-zip.org/recover.html) concerns 7z headers and must not be copied onto a ZIP file.

Resolve implementation differences with the installed help, Debian's packaged [7zz manual](https://manpages.debian.org/bookworm/7zip/7zz.1.en.html) and [upstream supported formats](https://7-zip.org/).
