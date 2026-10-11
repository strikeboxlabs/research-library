---
name: exiftool
description: Inspect image, document and media metadata with ExifTool while retaining tag groups and source-file identity. Use for creator, software, codec and timestamp leads in downloaded artifacts.
---

# ExifTool metadata inspection

Read this entire SKILL.md before acting. Require the installed ExifTool, selected original artifact and fresh private report path. Use the read-only inspection below, retaining source identity and relevant tag groups. Finish with reported fields, parser/status gaps and the supported interpretation; missing input/tool is not a successful metadata review.

Inspect the original downloaded bytes; screenshots and re-exported documents may have different metadata. Define `artifact` as an absolute file path and `report` as a fresh JSON path.

~~~bash
exiftool -ver
exiftool -a -G1 -s "$artifact"
(set -o noclobber; exiftool -j -G1:4 "$artifact" > "$report")
status=$?
~~~

Check each command's status and diagnostics; a report may contain partial results or error fields. The first inspection displays duplicate tags and their groups. The JSON uses group and instance identifiers to avoid suppressing identically named tags. Keep `SourceFile` when combining results from several files. The commands read metadata; tag assignments such as `-Author=...` and `-json=...` switch to writing.

Check `Author`, `Artist`, `Creator`, `Description` and software fields as available. Names may be in different tags; grepping only the printed label `Author` loses evidence. JSON values may be arrays, and names may contain spaces or punctuation, so avoid fixed-column `cut` pipelines.

Treat a creator name or hostname as a lead, not proof of an account or device. A timestamp may describe editing, export or the local filesystem; retain its tag/group and timezone context. A missing field means it was not reported, not that the original never contained it. Investigate parser warnings, unsupported formats and truncated downloads before claiming a clean result.

For media, retain container, codec/tag and software fields separately. AVI's `FMP4` tag maps to MPEG-4 in [FFmpeg's RIFF table](https://github.com/FFmpeg/FFmpeg/blob/master/libavformat/riff.c); that tag alone does not establish the producing server's software version, invocation or vulnerability status. An output filename ending `.avi` or a conversion-success page is weaker than parsing the actual returned bytes.

Use the [upstream application manual](https://github.com/exiftool/exiftool/blob/master/html/exiftool_pod.html) to resolve reading, JSON and group options.
