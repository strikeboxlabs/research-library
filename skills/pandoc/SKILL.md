---
name: pandoc
description: Convert reviewed Markdown to an inspectable LaTeX intermediate with explicit reader extensions and template selection. Use to diagnose document pipeline stages and distinguish conversion from PDF rendering.
---

# Inspect the conversion stage

Read this entire SKILL.md before acting. Require the reviewed Markdown, trusted template/resources and installed converter. Finish with status, diagnostics and inspected intermediate output; rendering a PDF is a separate stage.

Set `input_md`, `template`, `output_tex` and `conversion_log` to absolute paths; outputs must be fresh files in a private working directory. Inspect templates, defaults and filters before use.

~~~bash
pandoc --version
pandoc --list-extensions=markdown
pandoc --from=markdown-raw_attribute --to=latex --standalone \
  --template="$template" --output="$output_tex" "$input_md" \
  >"$conversion_log" 2>&1
conversion_status=$?
~~~

The minus sign disables that reader extension; it does not disable all raw TeX handling. Select extensions from the actual document contract. Check status and inspect the generated TeX before sending it to an engine. A successful conversion does not establish a complete PDF, correct glyphs or successful later stages. Preserve each stage's diagnostics when a wrapper falls back after failure.

For untrusted conversion, use an isolated environment and the installed `--sandbox` option where applicable. Pandoc's sandbox restricts reader/writer IO, not filter execution or the PDF engine. A template or Lua filter remains a separate trust input. Missing template/data resources require resolving that dependency, not dropping the restriction silently.

See the [Pandoc manual](https://pandoc.org/MANUAL.html) for extension, template and sandbox behavior.
