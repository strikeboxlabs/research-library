---
name: latex
description: Build a reviewed LaTeX document for a DVI-based workflow and interpret the selected engine's log and intermediate output. Use when a pipeline deliberately requires DVI before PostScript conversion.
---

# Produce the intended DVI intermediate

Read this entire SKILL.md before acting. Require reviewed TeX/resources, the installed latex format and a deliberate DVI output requirement. Complete with status, log and the newly produced DVI; later conversion stages need their own results.

Set `source_dir` to the trusted project directory, `input_tex` to its absolute main file, `output_dir` to an existing fresh private directory and `console_log` to a fresh absolute path. Use the normal build identity.

~~~bash
latex --version
latex --help
(cd "$source_dir" && latex -no-shell-escape -interaction=nonstopmode \
  -halt-on-error -file-line-error -output-directory="$output_dir" "$input_tex") \
  >"$console_log" 2>&1
compile_status=$?
~~~

Confirm the selected implementation and actual output format in its log. DVI generation is distinct from PDF generation. A failed earlier PDF engine does not prove this route will work or render equivalently. Check class/package availability, driver-specific graphics and glyph support before selecting a fallback. Keep every stage's status and fresh artifact associated with the same input.

TeX processes macros and reads resources even with shell escape disabled. Review source/configuration and constrain the build environment for untrusted input. An output directory is not a filesystem sandbox. Missing prerequisites remain explicit; do not fetch or install arbitrary packages to suppress an unexplained error.

See the [TeX implementation options](https://raw.githubusercontent.com/TeX-Live/texlive-source/trunk/texk/web2c/man/tex.man) and [Web2c manual](https://www.tug.org/texinfohtml/web2c.html).
