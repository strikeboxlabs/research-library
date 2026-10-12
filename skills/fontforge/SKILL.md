---
name: fontforge
description: Read metadata from a selected trusted local font with FontForge's Python interface. Use when a processing pipeline confuses successful parsing, font names and full font validation, or a CLI build differs from system Python.
---

# Inspect one trusted font

Read this entire SKILL.md before acting. Require a trusted FontForge installation with Python support and trusted startup scripts/plugins, one known ordinary TTF/OTF file, and permission to parse it. No conditional resources are required. Finish with the selected input, build, metadata, diagnostics and process status; an unavailable parser or unknown input provenance leaves the check incomplete.

Define `fontforge_bin` as the verified executable and inspect its build and CLI options:

~~~bash
"$fontforge_bin" -version
"$fontforge_bin" -usage
~~~

FontForge embeds Python; a separate system Python lacking its extension does not prove that the CLI lacks scripting support. `-lang=py` selects Python rather than FontForge's native script language. Startup code is executable; a metadata task does not make an unknown installation or hostile font safe. Use ordinary privilege and a reviewed input copy, excluding archives, suspect uploads and font collections from this procedure.

Define `font_file` as that copy's absolute path, and `report`/`diagnostics` as fresh private files. Pass the filename as an argument instead of inserting it into Python source:

~~~bash
umask 077
timeout --kill-after=5s 30s "$fontforge_bin" -lang=py -c '
import json
import sys
import fontforge
font = fontforge.open(sys.argv[1])
try:
    print(json.dumps({"familyname": font.familyname, "fontname": font.fontname}))
finally:
    font.close()
' "$font_file" >"$report" 2>"$diagnostics"
parse_status=$?
printf 'parse_status=%s\n' "$parse_status"
~~~

Require zero status, the expected JSON fields and inspected diagnostics. GNU timeout normally reports 124 when the time limit expires; retain partial output as incomplete. A timeout limits duration, not parser privilege or all resource use. Resolve a missing module/build or input-format error before retrying; do not add sudo or run an archive to diagnose it.

`familyname` and `fontname` are PostScript naming metadata, not a verified style classification or publisher identity. Opening successfully does not validate every table, glyph, rendering behavior or security property. This snippet closes the object without saving/generating a font. In a pipeline review, distinguish parser status from the wrapper's labels and later moves: moving an input to a processed directory can occur even after a failed parse.

References: [CLI options](https://fontforge.org/docs/techref/cliargs.html), [Python integration](https://fontforge.org/docs/scripting/python.html), [font properties and methods](https://fontforge.org/docs/scripting/python/fontforge.html).
