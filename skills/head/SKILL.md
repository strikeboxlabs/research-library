---
name: head
description: Preview the beginning of selected local text files with GNU head while retaining file identity and partial-read limits. Use to choose documents for full review or diagnose misleading merged previews.
---

# Preview selected text without claiming full coverage

Read this entire SKILL.md before acting. Require GNU head and the explicit local files to preview. Establish whether the task needs lines or bytes and retain input identity. Finish with candidate files and any read failures; previewing the beginning does not complete a document review.

Check `head --version`. Define `file_a` and `file_b` as selected absolute text-file paths. This first-line preview forces headers even when the selected set later contains just one file:

~~~bash
head -v -n 1 -- "$file_a" "$file_b"
status=$?
~~~

Check `status` and diagnostics: output from one readable file can coexist with a failure for another. Normally headers appear only for multiple files; `-v` always labels them and `-q` suppresses them. Do not use a merged `-q` preview as evidence of which file supplied a line. Filenames/contents can themselves contain newlines; these human-readable headers are not a lossless machine record format.

`-n 1` selects one line, not one character or all relevant text. Empty files produce no content; an initial blank line or PDF form feed can conceal a useful later heading. Review the candidate fully before accepting its contents. An uncontrolled wildcard can include stale/unrelated outputs or remain literal when it matches nothing; select the intended files explicitly.

For byte inspection, `-c` counts bytes and can cut a UTF-8 character. GNU negative counts mean all but the trailing lines/bytes, so use a reviewed nonnegative count for a bounded beginning preview. With no file, head reads stdin; a pipeline can stop its producer early, and head's status does not establish upstream completion. See the [GNU head manual](https://manpages.debian.org/testing/coreutils/head.1.en.html).
