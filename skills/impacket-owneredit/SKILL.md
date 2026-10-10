---
name: impacket-owneredit
description: Read or change the owner SID of a selected Active Directory object with Impacket owneredit from Linux. Use to verify ownership prerequisites, distinguish owner changes from DACL changes and restore a specifically authorized temporary change.
---

# Read, change and verify one owner SID

Read this entire file before acting. Resolve the target and capture its original owner before a write. Finish with before/after owner SIDs and any unresolved restoration; a zero exit status alone is insufficient.

Use the installed `impacket-owneredit` wrapper, or its verified Python script invocation. Check `-h`. Define `identity` as `domain.example/user`, `dc_fqdn`, `dc_ip` and `target_dn`. With an appropriate `KRB5CCNAME` cache:

~~~bash
impacket-owneredit -k -no-pass -use-ldaps -dc-host "$dc_fqdn" -dc-ip "$dc_ip" \
  -target-dn "$target_dn" -action read "$identity"
~~~

Retain the resolved object and original owner SID. The tool reads the owner portion of the security descriptor; this is not a complete DACL backup. A not-found diagnostic is a failed lookup even if that build exits zero. Verify realm, object DN and connected DC before interpreting it as absence.

For a selected authorized change, set `new_owner_sid` and use the same target/connection:

~~~bash
impacket-owneredit -k -no-pass -use-ldaps -dc-host "$dc_fqdn" -dc-ip "$dc_ip" \
  -target-dn "$target_dn" -new-owner-sid "$new_owner_sid" -action write "$identity"
~~~

Repeat the read and compare exact SIDs. A name can be renamed or ambiguous, while the SID identifies the principal. Ownership and DACL rights are separate state; changing one is not evidence the other has changed.

For a temporary change, restore with another `-action write -new-owner-sid "$original_owner_sid"`, then read back. There is no owneredit backup-file restore workflow to assume. Permission to take ownership as yourself does not necessarily permit returning ownership to an arbitrary principal; arrange the needed administrator path first. Following a timeout, inspect the current owner before retrying or restoring so concurrent legitimate changes are not overwritten.

The [upstream parser and owner handling](https://github.com/fortra/impacket/blob/master/examples/owneredit.py) distinguish `-target`, `-target-sid`, `-target-dn` and the corresponding new-owner selectors. Use one unambiguous selector for each.
