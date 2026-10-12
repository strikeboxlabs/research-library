---
name: wkhtmltopdf
description: Render a selected reviewed local web document to PDF with wkhtmltopdf. Use when resource loading, stylesheet context or partial rendering affects a report artifact.
---

# Verify the rendered report

Read this entire SKILL.md before acting. Require the reviewed document/resources and intended renderer environment. No conditional resources are required. Finish with conversion status and visual/content coverage; a created PDF alone is incomplete evidence.

Check `wkhtmltopdf --version` and `--extended-help`; build features can differ. Define `input` as the reviewed absolute document path, `pdf` as a fresh output path and `log` as a fresh diagnostic capture:

~~~bash
wkhtmltopdf --disable-javascript --disable-local-file-access --load-error-handling abort "$input" "$pdf" 2>"$log"
status=$?
~~~

Check status and diagnostics, then render/inspect all requested content for missing tables, assets or clipping. Local asset access can require a specific reviewed `--allow` directory. Disabling JavaScript changes script-dependent output. These options do not prevent all network resource requests or sandbox the renderer.

An XML extension alone does not establish a renderable document: matching stylesheet/resource resolution must exist. If a report relies on XSL or JavaScript, establish that contract rather than accepting a blank or raw-text PDF. Load-media failures can be ignored by default; inspect them even when status is successful. Keep the source and derivative distinct.

Source: [wkhtmltopdf option contract](https://wkhtmltopdf.org/usage/wkhtmltopdf.txt).
