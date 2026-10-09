---
name: impacket-getuserspns
description: Enumerate user-associated AD service principal names and request selected service-ticket material with Impacket GetUserSPNs for a lab password audit. Use to separate SPN discovery, ticket requests and offline recovery.
---

# Impacket GetUserSPNs

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

GetUserSPNs does not create SPNs. Tools such as targetedKerberoast can temporarily add one using directory write rights before requesting a ticket, then attempt removal. That is a separate modifying workflow requiring an exact target, prior-state evidence and verified restoration, including after failures. An account with no SPN is not a reason to substitute that workflow silently.

If using a known file cache, add `-k -no-pass`, export its absolute path in `KRB5CCNAME`, and supply the correct DC FQDN via supported `-dc-host`. Check cache identity/expiry, DNS and time before retrying authentication. Retain per-account errors and validate the output file rather than relying only on exit status.

Documentation reviewed 2026-10-09; Linux execution untested. Cases: Active pp. 7–9; Administrator pp. 9–10. Sources: [GetUserSPNs implementation and CLI](https://github.com/fortra/impacket/blob/master/examples/GetUserSPNs.py), [targetedKerberoast's additional write behaviour](https://github.com/ShutdownRepo/targetedKerberoast).
