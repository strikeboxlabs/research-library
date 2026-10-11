---
name: qpdf
description: List, extract or package selected owned PDF attachments with qpdf. Use when embedded-file keys, binary output or recovered-document warnings make the result uncertain.
---

# Work with selected PDF attachments

Read this entire SKILL.md before acting. Require installed qpdf, an authorized PDF working copy and selected attachment/output scope; no conditional resources are required. Use ordinary filesystem permissions and fresh private outputs. Finish with the observed attachment key, output identity and status/diagnostics; missing passwords, unreadable inputs or incomplete output remain unresolved.

Check `qpdf --version` and `qpdf --help=attachments`. Define `pdf` as the absolute working-copy path:

~~~bash
qpdf "$pdf" --list-attachments --verbose
status=$?
~~~

Read the keys rather than guessing from displayed filenames: those can differ. Listing embedded files does not establish their provenance or safe contents, and visible document pages need not show an attachment. Preserve stderr and the final status: 0 means no detected errors/warnings, 2 errors, and 3 warnings without errors. Do not hide warnings to force a clean completion claim.

For one observed `attachment_key`, define `attachment_out` as a fresh private file:

~~~bash
umask 077
(set -C; qpdf "$pdf" "--show-attachment=$attachment_key" > "$attachment_out")
status=$?
~~~

This writes binary bytes to stdout; do not combine other inspection output into that file. A failed command can leave an empty/partial output. Retain its size/digest and diagnostics before accepting or consuming it. Treat decoded contents as data; do not execute an attachment or derive its destination from an embedded filename.

To package a selected owned regular `attachment_file` into a separate fresh `output_pdf`:

~~~bash
test ! -e "$output_pdf" && test ! -L "$output_pdf" &&
  qpdf "$pdf" --add-attachment "$attachment_file" -- "$output_pdf"
status=$?
~~~

Check success, list the output's attachments, then extract the selected key separately and compare its bytes with the source when transfer integrity is the task. The terminating `--` closes attachment options. Output-path checks are not protection against concurrent writers. Keep the original unchanged and diagnose unsupported options or password requirements through the installed help. Adding an attachment copies readable bytes into a new document; it does not confer permission to read other files.

See [qpdf attachment operations and status](https://qpdf.readthedocs.io/en/stable/cli.html#embedded-files-attachments).
