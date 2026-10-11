---
name: wget
description: Retrieve a selected HTTP/HTTPS artifact or approved FTP subtree with GNU Wget. Use when output naming, partial transfers, mirror completeness, page requisites or relocated form/asset origins matter.
---

# Preserve the intended artifact and inspect the response

Read this entire SKILL.md before acting. Define the requested URL and a new output path before downloading. Finish with the transfer result, file identity and any remaining integrity uncertainty; a filename extension alone is not evidence of content type.

For a page captured as an owned template or relocated assets/forms, read [page capture boundaries](references/page-capture.md) fully first.

For an approved FTP directory mirror, read [FTP subtree retrieval](references/ftp-mirror.md) fully first; the single-file command below is not a mirror command.

Confirm GNU Wget with `wget --version`; BusyBox and other implementations have different option sets. A Windows PowerShell `wget` can instead be an alias for Invoke-WebRequest; its `-OutFile` download argument does not establish GNU option semantics. GNU Wget's lowercase `-o` names a log file, whereas uppercase `-O`/`--output-document` names the downloaded content. Use the selected client's contract before interpreting a saved filename. Define `url`, `download_file` and a private `response_log`:

~~~bash
wget --server-response --timeout=20 --tries=2 \
  --output-document="$download_file" "$url" 2> "$response_log"
~~~

These bounds are example task choices. The timeout covers network stages/idle reads, not an absolute total runtime. `--output-document` truncates its destination immediately: use a new path and do not point it at the only valid copy. Inspect the exit status and response log, then check the resulting format/size and an independently supplied digest when available. Redirects, login pages and proxy error documents can produce the wrong bytes under the desired filename.

For an interrupted earlier download, `--continue` can request the remaining bytes. Use it only when the local partial file is known to match the same remote object. Resuming against a replaced object can combine incompatible content; restart into a separate file when identity is uncertain. A completed byte transfer still needs the requested integrity check.

Use a specific URL for a specific artifact. Recursive retrieval or mirroring changes the task and request volume. A certificate error needs trust/name/time diagnosis; disabling certificate verification does not establish that the artifact came from the intended server. Keep authentication cookies, redirect tokens and private response headers out of public reports.

See [GNU Wget download semantics](https://www.gnu.org/software/wget/manual/wget.html) and the [Windows PowerShell alias contract](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-webrequest?view=powershell-5.1). A downloaded program is not automatically an instruction to execute it.
