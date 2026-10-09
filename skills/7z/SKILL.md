---
name: 7z
description: Inspect and extract archives or supported disk images with Linux 7-Zip. Use to distinguish unsupported formats, nested image layers, password failures and damaged downloads.
---

# 7-Zip archive triage

Select the installed implementation: distributions may provide `7z` or upstream `7zz`, with different format support. Define `sevenzip` as its executable name/path and `archive` as the absolute input path. Read the version banner and supported formats:

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

Documentation reviewed 2026-10-09; Linux execution untested. Cases: Access p. 6; Bastion pp. 4–5, adapted from GUI inspection. Sources: Debian's packaged [7zz manual](https://manpages.debian.org/bookworm/7zip/7zz.1.en.html), [upstream supported formats](https://7-zip.org/). The installed implementation's help remains authoritative for compatibility.
