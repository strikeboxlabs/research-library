---
name: samdump2
description: Extract offline local-account hash records from matching legacy Windows SYSTEM and SAM hives. Use to distinguish extraction, unsupported hive encryption and misleading empty-password output.
---

# Offline SAM extraction

Use existing hive copies from the same Windows installation and coherent acquisition. `samdump2` derives the boot key from SYSTEM and reads local-account records from SAM; it does not crack passwords or read Active Directory's NTDS database. Inspect `samdump2 -h` and the package version before choosing it.

The reviewed 3.0.0 implementation uses legacy RC4/DES processing without modern AES SAM handling. Do not infer compatibility merely from two files being named SYSTEM and SAM. For newer or unknown hive formats, choose a parser with demonstrated support for that format, such as a verified Impacket secretsdump build.

Define `system_hive` and `sam_hive` as existing absolute paths, and `records` as a fresh private output. The argument order matters:

~~~bash
umask 077
samdump2 -o "$records" "$system_hive" "$sam_hive"
~~~

Check diagnostics and inspect whether complete account records were written. Preserve username, RID and both hash fields in the original output. The layout is `username:RID:LM:NT:::`; the NT field is distinct from an LM hash or captured NetNTLM challenge/response. This implementation can prefix disabled accounts with `*disabled*`; retain that acquisition-time state in the account mapping if preparing a separate cracker input.

An emitted empty-password NT value is not sufficient evidence that the account has an empty password: the reviewed source substitutes that value when the NT field's size is not the expected legacy size. An unsupported modern record can therefore look plausible. Resolve format support, acquisition completeness and parser diagnostics before interpreting values or starting an offline check.

Keep extracted records local and private; the source writeup's upload to an online cracking service is unnecessary. A recovered candidate also does not establish current account state or authorize a login attempt. Finish with hive identities, parser version, supported format, record count and any unresolved extraction limitation.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Bastion pp. 4–5. Sources: [packaged manual](https://manpages.debian.org/trixie/samdump2/samdump2.1.en.html), [3.0.0 extraction and fallback behavior](https://sources.debian.org/src/samdump2/3.0.0-8/samdump2.c/).
