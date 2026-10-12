---
name: gs
description: Convert reviewed PostScript to PDF with the Ghostscript CLI and explicit device and access policy. Use to diagnose a final rendering stage while preserving interpreter errors and visual evidence.
---

# Run the selected Ghostscript conversion

Read this entire SKILL.md before acting. Require reviewed PostScript/resources, a trusted Ghostscript environment and fresh private outputs. Finish with status, diagnostics and inspected PDF content; an artifact alone does not establish successful conversion.

Set `input_ps` to the absolute input path, and `output_pdf` and `conversion_log` to fresh absolute file paths. Inspect `GS_OPTIONS` and resource search settings first; they can add arguments or inputs. Use the normal build identity.

~~~bash
gs --version
gs --help
gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=pdfwrite \
  -sOutputFile="$output_pdf" -f "$input_ps" >"$conversion_log" 2>&1
conversion_status=$?
~~~

`pdfwrite` produces PDF; this invocation does not select a printer. Retain status even when output exists. Diagnose `invalidfileaccess` using the named resource, OS permissions and interpreter policy; syntax/type errors instead require inspecting the generated PostScript. Do not disable SAFER to conceal a failure.

SAFER is enabled by default from Ghostscript 9.50, but its implementation varies with version. It is not an OS sandbox. For a legitimate additional resource, consult the exact version's narrow file-permission options; relative paths and symlink spellings matter.

Inspect page count, layout and glyphs in the new PDF. Preserve the earlier stage's error when a wrapper retries through Ghostscript; later success does not retroactively validate that stage.

See [Ghostscript usage and access controls](https://ghostscript.readthedocs.io/en/latest/Use.html).
