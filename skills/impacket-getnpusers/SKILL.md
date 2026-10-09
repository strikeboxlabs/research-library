---
name: impacket-getnpusers
description: Use Impacket GetNPUsers to check specified lab accounts for Kerberos preauthentication requirements and save AS-REP material for an offline audit. Use to distinguish account responses from usable ticket caches.
---

# Impacket GetNPUsers

Check the installed executable and `-h`: distributions may name it `impacket-GetNPUsers` or `GetNPUsers.py`. Preserve the reported Impacket version. This procedure checks a supplied account list against one in-scope domain; it does not guess passwords.

Define `domain` as the AD DNS domain, `dc_ip` as its DC address, `users` as a file of selected bare usernames (one per line), and `output` as a fresh artifact file:

~~~bash
umask 077
impacket-GetNPUsers "$domain/" -dc-ip "$dc_ip" -no-pass -usersfile "$users" -format hashcat -outputfile "$output"
~~~

In this mode the supplied list drives requests; it is not a directory-wide account inventory. Keep `-no-pass`: omitting it can enter a different authentication path. Names inferred from document metadata are candidates, not established accounts.

| Result | Interpretation |
|---|---|
| `$krb5asrep$...` output | An AS-REP encrypted reply-part was obtained for offline password testing. Preserve the complete single-line record and encryption type. |
| Preauthentication required / `UF_DONT_REQUIRE_PREAUTH` absent | This account did not yield material through the no-preauthentication technique. It is not a failed password guess. |
| Principal unknown | That principal was not found in the queried realm; verify spelling and realm. |
| Policy, transport or encryption-type error | Inconclusive for this technique; retain the precise error instead of labelling the account nonexistent. |

The output is not plaintext and is not a ready-to-use `.ccache`; the TGT itself is not encrypted with the user's password. Match the downstream parser to the output dialect and encryption type. `-format john` is available when a John-compatible representation is required.

Check per-account diagnostics and the saved file, not just the process exit code: caught errors may leave a partial or empty result.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Absolute PDF pp. 5–6. Maintenance source: [upstream GetNPUsers implementation and CLI](https://github.com/fortra/impacket/blob/master/examples/GetNPUsers.py).
