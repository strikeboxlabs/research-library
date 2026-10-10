---
name: ps2pdf
description: Convert reviewed PostScript to PDF with Ghostscript and diagnose conversion status, file-access failures and template errors. Use when a label/report wrapper misreads output or disables SAFER.
---

# PostScript conversion and failure diagnosis

Inspect `command -v ps2pdf` and the installed wrapper when a service uses a bundled copy. Check the version of the Ghostscript executable that wrapper actually invokes (`gs --version` for the normal PATH installation). PostScript is executable interpreter input: conversion can process file operations as well as drawing instructions. Use reviewed input and an ordinary account in the intended conversion environment.

Define `input_ps` as an existing absolute source path, and `output_pdf` and `conversion_log` as fresh absolute paths in a private working directory:

~~~bash
umask 077
ps2pdf -dSAFER "$input_ps" "$output_pdf" >"$conversion_log" 2>&1
conversion_status=$?
~~~

Options precede filenames. Keep the output explicit to avoid an unintended default destination. The wrapper invokes Ghostscript's `pdfwrite` device in batch mode; this writes a PDF rather than sending a print job. A nonzero status is a conversion failure even if a partial PDF exists. Empty stdout is normal for the quiet wrapper, and nonempty diagnostics alone do not prove failure. Retain the exit status and inspect the result with a PDF reader, including page count, content and layout.

| Result | Next check |
|---|---|
| File-access error such as `invalidfileaccess` | Inspect the named operand, process identity, OS permissions and Ghostscript access policy. Distinguish an intended resource from an unexpected file operation. |
| `undefined`, `syntaxerror` or `typecheck` | Inspect the generated PostScript around the reported operator and operand stack. A faulty text substitution can become program syntax; rerunning under sudo is not a repair. |
| Successful conversion, wrong label or page geometry | Compare source/template data and page settings, then inspect the rendered PDF. A generated artifact alone does not prove the database returned the intended row. |

Ghostscript 9.50 and later enables SAFER by default; explicit `-dSAFER` states the intended mode. `-dNOSAFER`/`-dDELAYSAFER` disables those interpreter access controls until re-enabled, while OS permissions still apply. Do not use it as a generic conversion fix. For a legitimate additional resource, consult the installed version's narrowly scoped `--permit-file-read` handling; path spelling matters, including absolute versus relative paths and symlink aliases. SAFER is not a substitute for an updated, appropriately isolated interpreter.

When reviewing a generator, follow values into the final PostScript as well as the subprocess arguments. Quoting a shell argument does not escape PostScript string delimiters. Inspect generated code as text first; converting it is execution. Keep source inspection separate from any privileged wrapper invocation.

Consult the [wrapper implementation](https://github.com/ArtifexSoftware/ghostpdl/blob/master/lib/ps2pdfwr), [Ghostscript access controls](https://ghostscript.readthedocs.io/en/latest/Use.html#dsafer) and [PDF device behavior](https://ghostscript.readthedocs.io/en/latest/VectorDevices.html) for release-specific details.
