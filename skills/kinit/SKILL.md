---
name: kinit
description: Obtain and inspect MIT Kerberos tickets in a dedicated credential cache, including PKINIT with an existing certificate. Use when realm configuration, cache selection or certificate trust prevents authentication.
---

# MIT kinit and cache selection

Check the installed Kerberos implementation and `kinit`/`klist` help; MIT and Heimdal options differ. Establish the principal, realm, reachable KDC, DNS and clock state before treating authentication failure as a wrong password.

Define `principal` as the exact `user@REALM`, `krb_config` as an existing task-specific MIT config containing the actual realm/KDC settings, and `cache_path` as a fresh absolute path in a private directory:

~~~bash
umask 077
KRB5_CONFIG="$krb_config" kinit -c "FILE:$cache_path" "$principal"
klist -c "FILE:$cache_path"
~~~

Enter the known password at the prompt. Explicit `-c` prevents unexpectedly replacing the user's default cache. Verify the resulting default principal, ticket service and validity period; a cache file's existence alone is not success. Set `KRB5CCNAME="FILE:$cache_path"` for the intended consuming process. Some non-MIT clients expect different cache argument syntax; inspect their actual help.

For **PKINIT with an existing authorized certificate**, confirm the MIT PKINIT plugin is installed, the certificate/key match and the KDC supports it. Define `cert`, `key` and `ca_bundle` as absolute PEM paths, with the CA trust established independently:

~~~bash
KRB5_CONFIG="$krb_config" kinit -c "FILE:$cache_path" -X "X509_user_identity=FILE:$cert,$key" -X "X509_anchors=FILE:$ca_bundle" "$principal"
klist -c "FILE:$cache_path"
~~~

The configuration spelling is `pkinit_identities`, not `pkinit_identites`. CSR validation is insufficient: the issued certificate, mapped principal, usages, trust chain and KDC certificate policy must agree. Inspect specific errors before changing EKU/SAN validation settings; weakening verification is not a routine repair.

If a TCP-only proxy is involved, `[libdefaults] udp_preference_limit = 1` makes normal MIT requests prefer TCP, but does not disable fallback. Apply it in the task config and verify the transport actually used. Protect optional `KRB5_TRACE` output because it exposes environment and identity details.

After use, `kdestroy -c "FILE:$cache_path"` destroys this cache only. Do not destroy unrelated default/collection caches. Record the selected principal, cache and expiry without copying tickets into reports.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Anubis p. 17. Sources: [kinit](https://web.mit.edu/kerberos/krb5-latest/doc/user/user_commands/kinit.html), [klist](https://web.mit.edu/kerberos/krb5-latest/doc/user/user_commands/klist.html), [configuration and PKINIT](https://web.mit.edu/kerberos/krb5-latest/doc/admin/conf_files/krb5_conf.html).
