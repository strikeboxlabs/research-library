---
name: clamscan
description: Scan selected owned files with ClamAV and interpret detections, errors and parser diagnostics. Use when zero infections, an old database or a file-list option is mistaken for a complete safety result.
---

# Preserve scan scope and the actual result

Read this entire SKILL.md before acting. Require a trusted scanner, approved signature database and readable selected artifacts. Establish scope and private outputs first; use the approved isolated analysis context with ordinary file access. Finish with status, detections, errors/skipped files and engine/database coverage.

Define `artifact` as the selected absolute regular-file path and `scan_log` as a fresh private output file:

~~~bash
umask 077
clamscan --version
clamscan -- "$artifact" >"$scan_log" 2>&1
scan_status=$?
printf 'scan status: %s\n' "$scan_status"
~~~

Read the relevant whole report. Status 0 means no virus found, 1 detections, 2 errors. Retain file/signature names, engine/database version/date, counts and warnings. Stale signatures, inaccessible files, limits or unsupported parsers can reduce coverage. Zero infections does not prove safety or parser immunity. Do not automatically remove/move evidence or enable unsigned bytecode signatures.

For a reviewed list of owned inputs, define `file_list` as one absolute path per line; handle newline filenames separately:

~~~bash
clamscan --file-list="$file_list" >"$scan_log" 2>&1
scan_status=$?
~~~

The list supplies filenames to scan; it is not scanned as the artifact itself. Missing-path diagnostics are not completed scans. Recursion/symlink following changes scope and needs explicit selection; do not widen privileges for unrelated files.

For an authorized parser diagnosis, repeat the same bounded scan with `--debug` into a separate private log. Debug output can include parsed content; restrict access and redact reports. Retain recognized format/structure separately from detection verdict. Signature updates and daemon control are separate tasks.

See [clamscan options/status](https://manpages.debian.org/bookworm/clamav/clamscan.1.en.html) and [ClamAV scanning](https://docs.clamav.net/manual/Usage/Scanning.html).
