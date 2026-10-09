---
name: impacket-secretsdump
description: Parse existing Windows SAM/SYSTEM or NTDS snapshots, or perform a selected-account AD replication audit with Impacket secretsdump. Use to distinguish offline evidence, current credentials and incomplete results.
---

# Impacket secretsdump

## Existing local hives

Use SAM and SYSTEM hive copies from the same Windows system and acquisition. A `.reg` text export is not a raw hive. Preserve the originals and acquisition identity; a downloaded filename alone does not establish that the pair matches.

Check `impacket-secretsdump -h`; upstream installations may provide `secretsdump.py`. Define `sam` and `system_hive` as absolute input paths, and `output_prefix` as a new absolute prefix in a private directory:

~~~bash
umask 077
impacket-secretsdump -sam "$sam" -system "$system_hive" -outputfile "$output_prefix" LOCAL
~~~

The literal `LOCAL` selects file parsing. Replacing it with a hostname changes the operation to a remote workflow. SYSTEM supplies the boot key used for SAM decryption. The reviewed implementation writes extracted SAM records to `${output_prefix}.sam`; console output also contains diagnostics, so do not use an unfiltered console transcript as the hash file.

Typical records have `username:RID:LM:NT:::` fields. Keep the username/RID mapping. The fourth field is the NT hash; the LM field may contain a placeholder and is not interchangeable. These are local SAM account records, not NetNTLM challenge/response captures, plaintext passwords or a domain directory dump.

Before reporting success, inspect extraction errors and the new `.sam` file. Caught errors can leave partial results without a failing exit code. On failure, check binary transfer completeness, hive identity/pairing and version support before concluding the source contains no accounts. A recovered hash does not establish the account's enabled state or present network access.

## Selected-account replication audit

For an already acquired **NTDS database snapshot**, use the separate [offline NTDS procedure](references/offline-ntds.md). Its file inputs and account-selection limits differ from both SAM parsing and live replication below.

For an explicitly scoped AD credential/replication audit, define `domain` and `user` as the known requesting identity, `dc_host` as the intended DC, `subject` as the selected directory account and `remote_prefix` as a new private output prefix. Enter the known password at the prompt:

~~~bash
umask 077
impacket-secretsdump "$domain/$user@$dc_host" -just-dc-user "$subject" -just-dc-ntlm -outputfile "$remote_prefix"
~~~

This makes remote DRSUAPI replication requests and requires the applicable directory replication rights. It is not local hive parsing and does not require pretending the requesting user is a DC computer account. `-just-dc-user` selects one account and implies `-just-dc`; bare `-just-dc` has no such account limit. `-just-dc-ntlm` limits material to NTLM records. The selector does not support VSS mode.

Inspect errors and `${remote_prefix}.ntds` before reporting extraction. For an ambiguous account name, use the verified NetBIOS domain-qualified selector, not an assumed DNS-domain prefix. A permission failure is not evidence that no directory secrets exist; do not broaden the dump or switch acquisition method automatically. Protect the output as credential material and retain the requested account mapping.

Documentation reviewed 2026-10-09; Linux execution untested. Cases: Acute pp. 15–16; Administrator p. 10. Sources: [secretsdump CLI](https://github.com/fortra/impacket/blob/master/examples/secretsdump.py), [SAM/NTDS implementations](https://github.com/fortra/impacket/blob/master/impacket/examples/secretsdump.py).
