# LDAP protection and AD CS endpoint observations

Use when deciding whether a selected directory authentication route is permitted or when locating certificate-service roles. Require the selected DC and known single credential pair from the entrypoint. LDAP policy probes make network/authentication requests; retain the same account budget and do not interpret them as passive local configuration reading.

With `nxc_bin`, `target`, `domain`, `users_file` and `passwords_file` as already verified values:

~~~bash
"$nxc_bin" ldap "$target" -d "$domain" -u "$users_file" -p "$passwords_file" --no-bruteforce
~~~

Inspect this installation's host banner, check errors and actual authentication outcome. Historical `-M ldap-checker` reported signing/channel-binding findings; the reviewed newer module prints that it was removed and those checks are natively reported in the host banner. A module deprecation message is not a fresh finding. Check version/source rather than repeatedly invoking the removed module.

LDAP signing requirements and LDAPS channel-binding requirements are distinct. An illustrative current `signing:None`/`channel binding:Never` (older output may label signing `False`) indicates the reported checks for that endpoint/build, not a successful relay or unrestricted directory writes. Connection failures, unavailable TLS and unsupported probes remain unknown. The SMB banner's signing value concerns SMB, not LDAP. SMB signing enabled on the DC does not resolve LDAP relay conditions; disabled signing on another host is not permission to relay to the DC.

For directory AD CS role discovery, use this build's `adcs` module:

~~~bash
"$nxc_bin" ldap "$target" -d "$domain" -u "$users_file" -p "$passwords_file" --no-bruteforce -M adcs
~~~

Read the returned CA/configuration and enrollment-service endpoint labels. A Certificate Enrollment Web Service using Kerberos is not automatically classic `/certsrv/` Web Enrollment or a URL that accepts NTLM. Resolve the actual target URL, TLS policy, offered authentication scheme and permitted template before a relay/enrollment test. A found role is configuration evidence, not issuance permission. An HTTP endpoint without an NTLM challenge can explain an NTLM relay failure; it does not prove Kerberos relay will succeed.

Machine-account quota is covered in the entrypoint. A zero quota does not negate delegated creation rights; DNSAdmins membership also does not universally grant every DNS-node operation to the current token. Evaluate each intended object's current rights and actual operation.

Complete with selected endpoint/version, checks that ran, authentication status and unresolved conditions. See [LDAP implementation](https://github.com/Pennyw0rth/NetExec/blob/main/nxc/protocols/ldap.py), [retired checker](https://github.com/Pennyw0rth/NetExec/blob/main/nxc/modules/ldap-checker.py) and [AD CS discovery module](https://github.com/Pennyw0rth/NetExec/blob/main/nxc/modules/adcs.py).
