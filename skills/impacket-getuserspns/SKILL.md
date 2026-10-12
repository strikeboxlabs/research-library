---
name: impacket-getuserspns
description: Enumerate user-associated AD service principal names and request selected service-ticket material with Impacket GetUserSPNs for a lab password audit. Use to separate SPN discovery, ticket requests and offline recovery.
---

# Impacket GetUserSPNs

Read this entire SKILL.md before acting. Select directory enumeration or the separately permitted ticket request, with the known identity, DC and selected account explicit. No conditional resource is required. Finish with observed mappings, request diagnostics and actual record coverage; missing LDAP/KDC prerequisites or partial output stays unresolved.

Check `impacket-GetUserSPNs -h`; upstream installations may use `GetUserSPNs.py`. Define `domain`, `user` and `dc_ip` for the in-scope AD domain, known requesting account and DC address. Start with enumeration, entering the known password at the prompt:

~~~bash
impacket-GetUserSPNs "$domain/$user" -dc-ip "$dc_ip"
~~~

Record the SPN-to-account mapping. The default user-account query is not a complete inventory of every machine/service principal. An SPN does not by itself establish privilege, an active service or a recoverable password. An empty result after LDAP failure is not evidence of absence.

For a selected account within the ticket-request scope, define `service_user` as its observed bare account name and `output` as a fresh file:

~~~bash
umask 077
impacket-GetUserSPNs "$domain/$user" -dc-ip "$dc_ip" -request-user "$service_user" -outputfile "$output"
~~~

This makes KDC requests and saves offline password-testing material. In the reviewed implementation, `-outputfile` itself enables requesting; do not add it to an intended enumeration-only command. `-request` without a user selector requests across the returned set. Multiple SPNs can map to one account, so output count need not equal the SPN count.

Keep complete `$krb5tgs$...` records, their account mapping and encryption type. Mode 13100 in Hashcat applies to etype 23, not every Kerberos ticket. The relevant ciphertext is the service ticket's encrypted part; avoid describing the entire TGS reply as encrypted with an NT hash for every encryption type.

GetUserSPNs does not create SPNs. An absent SPN is a finding to resolve from directory evidence, rather than permission to change an account's attributes.

If using a known file cache, add `-k -no-pass`, export its absolute path in `KRB5CCNAME`, and supply the correct DC FQDN via supported `-dc-host`. Check cache identity/expiry, DNS and time before retrying authentication. Retain per-account errors and validate the output file rather than relying only on exit status.

Use the [GetUserSPNs implementation and CLI](https://github.com/fortra/impacket/blob/master/examples/GetUserSPNs.py) to resolve installed request selectors and output behavior.
