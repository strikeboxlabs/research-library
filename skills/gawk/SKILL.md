---
name: gawk
description: Remove exact duplicate text lines in one owned file with GNU awk's inplace extension while retaining first-seen order and a separate original backup.
---

# Rewrite one text file with GNU awk

Read this entire SKILL.md before acting. Require one owned ordinary regular text file, a stable original and a fresh backup suffix. Confirm GNU awk and its trusted installed inplace extension; this is not a portable awk option. Finish with rewrite status, preserved original and the actual resulting line semantics.

Define `input` as the absolute file path. Check it is not a symbolic link and that `${input}.bak` is absent before the selected rewrite:

~~~bash
gawk --version
gawk -i inplace -v inplace::suffix=.bak '!seen[$0]++' "$input"
status=$?
~~~

This keeps the first occurrence of each exact whole line without sorting. Supply only one file: the associative array otherwise persists across files. Default output record handling can normalize the final newline; do not use this for binary preservation or a format whose logical records span lines.

`-i` loads an AWK include; the inplace implementation also needs its installed native extension. Current GNU awk uses `inplace::suffix`; older installations may document `INPLACE_SUFFIX`. Select the matching manual rather than assuming any awk supports either interface.

The extension replaces the file through a temporary file, breaking links. It attempts to preserve owner/mode but does not copy ACLs. A fatal error preserves the original; an unhandled signal may leave a temporary file. Check status and resulting content against the retained backup before accepting the transformation or choosing recovery. Do not overwrite the backup to retry.

See [GNU awk inplace behavior](https://www.gnu.org/software/gawk/manual/html_node/Extension-Sample-Inplace.html).
