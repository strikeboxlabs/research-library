---
name: pdftotext
description: Extract text from an acquired PDF with Poppler pdftotext and retain page, layout and failure limits. Use for document review when empty or plausible text does not establish complete visual coverage.
---

# Extract and assess PDF text

Read this entire SKILL.md before acting. Require the installed Poppler utility, the selected local PDF and fresh private text/diagnostic paths. Choose whole-document or an explicit physical-page range before extracting. Finish with extraction status, the chosen page scope and unresolved visual/text gaps; a missing tool or unreadable input is a prerequisite gap.

Check `pdftotext -v` and `pdftotext -h`. Define `pdf` as the absolute input, `text` as a fresh text path and `log` as a separate fresh diagnostic path:

~~~bash
umask 077
(set -o noclobber; pdftotext -enc UTF-8 -eol unix "$pdf" - > "$text" 2> "$log")
status=$?
~~~

The final `-` sends text to stdout. Without a text-file argument the utility derives an output filename; explicit capture avoids silently replacing that default file. Check `status` and diagnostics before using the text; failure can leave a partial file. Preserve the original PDF.

The default attempts reading order. If columns or aligned tables become misleading, repeat into a fresh file with `-layout` and compare the relevant rendered pages. Neither mode guarantees correct structure. `-raw` follows content-stream order and is not a general reading-order repair. `-f` and `-l` select first/last physical pages; record that scope instead of claiming full-document coverage.

Page breaks normally include form feeds. `-nopgbrk` removes them and loses that boundary signal. PDF text extraction does not perform OCR: screenshots, scans or unusable font encodings can leave empty or misleading output while the process succeeds. A first-line preview finds candidates; it does not review all pages. Render and inspect evidence whose meaning depends on layout, imagery or missing text.

For this Poppler interface, status 1 concerns opening the PDF, 2 opening output, 3 permissions and 99 other errors. Resolve the actual diagnostic rather than treating every empty output as a scanned file or suppressing messages with `-q`. An extraction success establishes parsed text, not authenticity or complete content. Consult the [packaged upstream pdftotext manual](https://manpages.debian.org/testing/poppler-utils/pdftotext.1.en.html) for the installed options.
