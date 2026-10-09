---
name: searchsploit
description: Search the local Exploit-DB catalogue and inspect candidate source without executing it. Use when a product/version match needs validation or copied exploit paths and update behavior are unclear.
---

# SearchSploit candidate review

Check `searchsploit -h` and the installed catalogue/package location. This searches a local index; results depend on its age and configured data paths. No match does not establish that a product has no vulnerabilities.

Define `product` and `version` from observed service evidence, keeping banner uncertainty visible:

~~~bash
searchsploit -t "$product" "$version"
~~~

Default terms are combined with AND, order is flexible, and version-range matching can expand results. `-t` searches titles rather than also matching file paths. `-s` makes version matching strict; `-e` means an exact ordered title match, not stronger vulnerability verification. Broad product-only searches can help when exact version text misses a range, but increase review work.

Choose `edb_id` from an actual result:

~~~bash
searchsploit -p "$edb_id"
searchsploit -x "$edb_id"
~~~

`-p` displays the local path and may copy it to the clipboard; `-x` opens the source using the configured pager. Inspect title, affected versions/platform, prerequisites, references and code behavior. A title match is a candidate, not evidence that the specific service is exploitable. Confirm vendor advisories and package backports where relevant.

If a working copy is needed, move into a new case directory before `searchsploit -m "$edb_id"`. This copies the source; it does not validate or run it. Read defaults, network destinations, file writes, dependencies and cleanup before any separate decision to execute. Do not pipe a discovered path directly into Python or a shell.

`--nmap scan.xml` correlates service/version output with the catalogue, not live exploitability. `-u` updates the catalogue/package and can invoke package-manager or Git actions; do not mix it into a supposedly read-only search. Record the EDB ID, catalogue date/version when known, matched evidence and unmet conditions.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Ambassador p. 4. Source: [official SearchSploit manual](https://www.exploit-db.com/searchsploit).
