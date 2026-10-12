---
name: dvips
description: Convert a reviewed DVI intermediate to an explicit PostScript file and diagnose font, resource and page-selection problems. Use when a document pipeline requires a separate DVI-to-PostScript stage.
---

# Convert the selected DVI

Read this entire SKILL.md before acting. Require the reviewed DVI and associated fonts/resources, trusted configuration and a fresh private output destination. Complete with status, diagnostics and checked PostScript output; PDF creation is a later operation.

Set `work_dir` to the reviewed staging directory, `input_dvi` to its ordinary relative DVI filename and `output_ps` and `conversion_log` to fresh relative filenames there. Use names without leading option or command characters. Keep required resources in the approved relative layout.

~~~bash
dvips --version
dvips --help
(cd "$work_dir" && dvips -R2 -o "$output_ps" "$input_dvi") \
  >"$work_dir/$conversion_log" 2>&1
conversion_status=$?
~~~

The explicit output selects a file instead of a configured printer destination. `-R2` restricts shell execution and absolute/parent-relative resource access. A denied required resource calls for reviewing its layout and provenance, not silently weakening that policy. Configuration and fonts can still affect output.

Check status, missing fonts and conversion diagnostics. PostScript is interpreter input; inspect it before the next stage. A page count alone does not establish correct geometry or glyphs. If selecting pages, distinguish TeX page numbers from physical sequence positions: the manual's equals-prefix form selects sequence positions.

See the [Dvips manual](https://tug.ctan.org/systems/doc/dvips/dvips.html) for security levels, configuration and page numbering.
