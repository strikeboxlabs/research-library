# Existing NTDS snapshot

Use `ntds.dit` and the SYSTEM hive from the same DC/acquisition. Define `ntds`, `system_hive` and a new private `output_prefix` as absolute paths. Check the installed help, then parse local copies:

~~~bash
umask 077
impacket-secretsdump -system "$system_hive" -ntds "$ntds" -just-dc-ntlm -outputfile "$output_prefix" LOCAL
~~~

This makes no live replication request. SYSTEM supplies the boot key; a SECURITY hive is not required for this NTDS-only operation. It serves different LSA-secret extraction tasks. `-just-dc-ntlm` limits extracted material, not the account count. The reviewed CLI rejects `-just-dc-user` in LOCAL mode; do not promise one-account extraction from this command.

Inspect diagnostics and `${output_prefix}.ntds`; errors can leave partial results. Preserve `domain/account:RID:LM:NT:::` identity mapping and snapshot date. Old hashes and usernames do not establish current passwords, account state or login access. Do not automatically attempt every extracted credential against a live service.

ESE/database errors call for checking matching acquisition, file completeness and format support. Preserve originals; do not modify/repair the evidence database in place. Record which records were actually recovered and any failures.

Documentation reviewed 2026-10-09; Linux execution untested. Case: APT pp. 7â€“9. Sources: [CLI and LOCAL restrictions](https://github.com/fortra/impacket/blob/master/examples/secretsdump.py), [NTDS parser](https://github.com/fortra/impacket/blob/master/impacket/examples/secretsdump.py).
