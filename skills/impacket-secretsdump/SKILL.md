---
name: impacket-secretsdump
description: Parse existing Windows SAM/SYSTEM, SECURITY or NTDS snapshots, perform approved remote member-host acquisition or a selected-account AD replication audit with Impacket secretsdump. Use to distinguish offline evidence, current credentials and incomplete results.
---

# Impacket secretsdump

Read this entire SKILL.md before acting. Select offline inputs, a scoped replication query or the remote acquisition branch; retain store/account mapping, extraction status and actual artifacts. Read [offline NTDS](references/offline-ntds.md) for that snapshot task or [remote SAM acquisition](references/remote-sam.md) before live acquisition. Missing rights, partial output or unavailable inputs remain unresolved.

## Existing local hives

Use SAM and SYSTEM hive copies from the same Windows system and acquisition. A `.reg` text export is not a raw hive. Preserve the originals and acquisition identity; a downloaded filename alone does not establish that the pair matches.

Check `impacket-secretsdump -h`; upstream installations may provide `secretsdump.py`. Define `sam` and `system_hive` as absolute input paths, and `output_prefix` as a new absolute prefix in a private directory:

~~~bash
umask 077
impacket-secretsdump -sam "$sam" -system "$system_hive" -outputfile "$output_prefix" LOCAL
~~~

The literal `LOCAL` selects file parsing. Replacing it with a hostname changes the operation to a remote workflow. SYSTEM supplies the boot key used for SAM decryption. The reviewed implementation writes extracted SAM records to `${output_prefix}.sam`; console output also contains diagnostics, so do not use an unfiltered console transcript as the hash file.

Typical records have `username:RID:LM:NT:::` fields. Keep the username/RID mapping. The fourth field is the NT hash; the LM field may contain a placeholder and is not interchangeable. These are local SAM account records, not NetNTLM challenge/response captures, plaintext passwords or a domain directory dump.

A SAM `Administrator` record and an NTDS domain `Administrator` record are not the same identity merely because names or RIDs match. Preserve the source store and machine/domain with each record. Extraction decrypts stored credential material; it does not mean a password was cracked. A later login failure alone cannot identify why that credential was rejected.

Before reporting success, inspect extraction errors and the new `.sam` file. Caught errors can leave partial results without a failing exit code. On failure, check binary transfer completeness, hive identity/pairing and version support before concluding the source contains no accounts. A recovered hash does not establish the account's enabled state or present network access.

## Existing SECURITY hive

For a separate task examining cached domain logons and LSA secrets, define `security_hive` as the raw SECURITY hive from the same machine/acquisition as `system_hive`, and `security_prefix` as a fresh private output prefix:

~~~bash
umask 077
impacket-secretsdump -security "$security_hive" -system "$system_hive" -outputfile "$security_prefix" LOCAL
~~~

This leaves SAM and NTDS out of the requested inputs. Inspect both diagnostics and emitted files: the implementation writes `.cached` and `.secrets` only when corresponding items were recovered. A missing file may therefore mean no extracted items or a failed stage; check the error context before deciding.

Cached domain logon verifiers, including `$DCC2$` records, are not raw NT hashes. LSA results can include machine-account or service secrets and DPAPI key material; retain their labels instead of treating every value as a user's login password. **Illustrative:** a `.cached` record labelled for a domain user and a `.secrets` entry labelled `DPAPI_SYSTEM` establish different artifact types, not two interchangeable authentication values. Keep the source machine and snapshot date with each.

Use the [CLI and output implementation](https://github.com/fortra/impacket/blob/master/examples/secretsdump.py) to check release-specific flags; do not add remote acquisition options to repair a local parsing error.

## Selected-account replication audit

For an already acquired **NTDS database snapshot**, use the separate [offline NTDS procedure](references/offline-ntds.md). Its file inputs and account-selection limits differ from both SAM parsing and live replication below.

For an explicitly scoped AD credential/replication audit, define `domain` and `user` as the known requesting identity, `dc_host` as the intended DC, `subject` as the selected directory account and `remote_prefix` as a new private output prefix. Enter the known password at the prompt:

~~~bash
umask 077
impacket-secretsdump "$domain/$user@$dc_host" -just-dc-user "$subject" -just-dc-ntlm -outputfile "$remote_prefix"
~~~

This makes remote DRSUAPI replication requests and requires the applicable directory replication rights. It is not local hive parsing and does not require pretending the requesting user is a DC computer account. `-just-dc-user` selects one account and implies `-just-dc`; bare `-just-dc` has no such account limit. `-just-dc-ntlm` limits material to NTLM records. The selector does not support VSS mode.

Inspect errors and `${remote_prefix}.ntds` before reporting extraction. For an ambiguous account name, use the verified NetBIOS domain-qualified selector, not an assumed DNS-domain prefix. A permission failure is not evidence that no directory secrets exist; do not broaden the dump or switch acquisition method automatically. Protect the output as credential material and retain the requested account mapping.
