---
name: apport-unpack
description: Unpack one acquired Apport crash report into a private fresh directory. Use when encoded binary fields, partial extraction or process attribution complicate an owned crash diagnosis.
---

# Separate the report from its decoded fields

Read this entire SKILL.md before acting. Require the installed trusted Apport implementation, one authorized report copy and enough private disk/memory for its expanded fields. No conditional files are required. Finish with status, actual field coverage and report/process association; a CoreDump filename alone is insufficient.

Check `apport-unpack --help`. Define `report` as the selected absolute acquired report path and `out` as a fresh absolute directory under a private working parent:

~~~bash
umask 077
sha256sum -- "$report"
mkdir -m 700 -- "$out" && apport-unpack "$report" "$out"
status=$?
~~~

Inspect status and diagnostics before using the output. The destination must be new or empty; choose a new directory after failure rather than merging uncertain fields into an earlier extraction. Failure can leave partial output. A compressed report expands further, and stdin loading can require the whole report in memory; prefer the preserved file for attributable diagnosis.

Inspect the actual emitted field names and selected metadata such as ExecutablePath, Date, Signal and ProcStatus when present. Correlate executable/process/time with independent evidence. The report can omit CoreDump or other fields; a report suffix and zero status do not promise a complete memory snapshot. A textual field and its decoded binary counterpart are separate artifacts.

Preserve the original and hash any selected decoded field before format-aware analysis. Unpacking neither runs the crashed executable nor recreates its privileges. A memory string can be stale or unrelated to the current operation; printable fragments do not establish complete bytes or account ownership. Reports may contain private application data, so retain outputs privately and avoid dumping them into routine logs.

Reference: [Canonical parser and extraction behavior](https://github.com/canonical/apport/blob/main/bin/apport-unpack).
