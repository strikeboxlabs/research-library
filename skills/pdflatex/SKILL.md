---
name: pdflatex
description: Compile a reviewed LaTeX document to PDF and diagnose engine, package, glyph and output failures. Use when a rendering wrapper reports success despite a failed TeX stage.
---

# Compile and inspect the selected document

Read this entire SKILL.md before acting. Require trusted TeX input, its reviewed resources and an installed LaTeX format. Complete with exit status, the engine log and an inspected fresh PDF; a partial file is not completion.

Use an ordinary account in the intended build environment. Set `source_dir` to the reviewed project directory, `input_tex` to its absolute main file, `output_dir` to an existing fresh private build directory and `console_log` to a fresh absolute log path.

~~~bash
pdflatex --version
pdflatex --help
(cd "$source_dir" && pdflatex -no-shell-escape -interaction=nonstopmode \
  -halt-on-error -file-line-error -output-directory="$output_dir" "$input_tex") \
  >"$console_log" 2>&1
compile_status=$?
~~~

Check the first substantive error in the log. Distinguish missing classes/packages, unsupported Unicode and malformed source. PDF mode supports graphics such as PDF, PNG and JPEG; EPS needs a deliberate conversion path. Do not switch engines automatically merely to hide the first failure.

Rerun only when cross-reference diagnostics require it. Inspect page count, missing glyphs, clipping and references in the new PDF. A wrapper's final status cannot replace this engine's result.

Disabling shell escape does not prevent TeX file reads or provide OS isolation. Keep untrusted documents in a separately constrained build environment. Output-directory selection also affects input lookup; reuse can introduce stale auxiliary files.

References: [pdfTeX mode and graphics](https://raw.githubusercontent.com/TeX-Live/texlive-source/trunk/texk/web2c/man/pdftex.man), [TeX options](https://raw.githubusercontent.com/TeX-Live/texlive-source/trunk/texk/web2c/man/tex.man).
