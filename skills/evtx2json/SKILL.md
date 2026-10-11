---
name: evtx2json
description: Convert one acquired Windows EVTX log into selected, normalized JSON records with Silv3rHorn evtx2json on Linux; retain original records, parser diagnostics and field mappings when investigating logon events.
---

# Export selected EVTX records

Read this entire SKILL.md before acting; reuse complete current context. Require the installed Silv3rHorn implementation, its Python dependencies/resources and one acquired EVTX copy. Confirm the installed help and platform-specific resource paths below before conversion. Finish with original identity, selected channel, exported record coverage and unresolved parsing/translation gaps; this export is not a complete raw-event copy.

Define `python` as the verified interpreter, `tool_dir` as this implementation's installed directory and `converter` as its absolute evtx2json.py path. Do not assume another identically named converter has these options:

~~~bash
"$python" "$converter" --help
~~~

Define `evtx` as the absolute acquired input and `out_dir` as a fresh private directory. For a Security-channel export retaining duplicates:

~~~bash
umask 077
mkdir -m 700 -- "$out_dir" && (
  cd -- "$tool_dir" || exit
  "$python" "$converter" -f "$evtx" -c sec --nodedup -o "$out_dir" \
    >"$out_dir/stdout.txt" 2>"$out_dir/stderr.txt"
)
status=$?
~~~

Inspect the generated export, converter log, stdout and stderr. Upstream emits separate JSON objects separated by carriage returns, with a .txt suffix. Use a record-stream parser, not a single-document JSON loader. Unsupported events and parse failures can be omitted; found/processed counts need not equal emitted records when deduplication is enabled. A fresh directory prevents accidental append/reuse of timestamp-named outputs.

The upstream script's normal main path lacks a true return, so status 1 can follow a completed export; retain it and assess artifacts/diagnostics separately. Its non-frozen database lookup uses a working-directory-relative path containing a Windows backslash. On Linux, verify the installed implementation's resource-path handling before relying on decoded fields. A missing database, dependency or translation is a precise gap, not evidence of an empty original log. Do not silently change the acquired log or interpret partial output as complete.

The event mapping renames native fields: TargetUserName becomes TargetUsername, for example. Preserve original channel/provider, computer, record ID and UTC event time alongside normalized fields; a viewer's local-time display may differ. For logon analysis, 4625 records a failure and 4624 a successful logon. Compare logon type, workstation/IP, domain and available identifiers before associating nearby events. A password-looking username remains an unverified submitted value; a later successful event does not establish its ownership or validity. Inspect decisive fields in the original record when normalization loses detail.

Consult the [implementation and CLI](https://github.com/Silv3rHorn/evtx2json), [converter source](https://github.com/Silv3rHorn/evtx2json/blob/master/evtx2json.py), [event mappings](https://github.com/Silv3rHorn/evtx2json/blob/master/resources/events.py), and Microsoft definitions of [4625](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4625) and [4624](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4624) for version/schema differences.
