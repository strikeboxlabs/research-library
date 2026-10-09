---
name: 7z
description: Inspect and extract archives with Linux 7-Zip, including AES-encrypted ZIP files that another extractor rejects. Use to distinguish unsupported methods, password failures and damaged downloads.
---

# 7-Zip archive triage

Select the installed implementation: distributions may provide `7z` or upstream `7zz`, with different format support. Define `sevenzip` as its executable name/path and `archive` as the absolute input path. Read the version banner and supported formats:

~~~bash
"$sevenzip" i
"$sevenzip" l -slt "$archive"
~~~

Check the reported archive type, compression/encryption methods, member paths and unpacked sizes. A ZIP extension does not guarantee that every extractor supports its encryption. `unzip` reporting an unsupported method is not proof of a bad password.

Test integrity before extracting. For encrypted content, provide the known password at the interactive prompt rather than embedding it in a command line:

~~~bash
"$sevenzip" t "$archive"
~~~

Only after a successful test, define `destination` as a new extraction directory under the investigation workspace:

~~~bash
mkdir -m 700 "$destination" && "$sevenzip" x "$archive" -o"$destination"
~~~

`x` preserves member directories; `e` flattens them and can create name collisions. The output path is attached to `-o`. Inspect unexpected paths, links and very large expansion before extraction; use an unprivileged workspace. Avoid blanket overwrite switches when reviewing evidence.

Retain the test/extraction status and error text. Password errors and corruption can present similarly; verify the source transfer, archive parts and supported method before retrying credentials. A successful extraction establishes readable files, not trustworthy contents.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Access PDF p. 6. Maintenance source: Debian's packaged [7zz manual](https://manpages.debian.org/bookworm/7zip/7zz.1.en.html), commands and switches; the installed implementation's help remains authoritative for compatibility.
