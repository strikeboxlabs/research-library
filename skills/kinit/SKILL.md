---
name: kinit
description: Obtain MIT Kerberos tickets in a dedicated credential cache with a known password, provisioned keytab or existing authorized PKINIT certificate. Use when realm, service naming, cache selection, clock or certificate trust prevents the intended authentication.
---

# MIT kinit and cache selection

Read this entire SKILL.md before acting. Require the exact authorized principal, installed MIT client and established realm/KDC configuration. The password workflow, conditional provisioned-keytab and PKINIT workflows and conditional TCP-proxy settings are inline; select only the applicable branches. Finish with command status and the cache's principal, service and validity evidence, then its intended consumer/cleanup state. Missing credentials, client mechanism or trust remain explicit gaps.

Check the installed Kerberos implementation and `kinit`/`klist` help; MIT and Heimdal options differ. Establish the principal, realm, reachable KDC, DNS and clock state before treating authentication failure as a wrong password.

Define `principal` as the exact `user@REALM`, `krb_config` as an existing task-specific MIT config containing the actual realm/KDC settings, and `cache_path` as a fresh absolute path in a private directory:

~~~bash
umask 077
KRB5_CONFIG="$krb_config" kinit -c "FILE:$cache_path" "$principal"
kinit_status=$?
if [ "$kinit_status" -eq 0 ]; then
  klist -c "FILE:$cache_path"
fi
~~~

Enter the known password at the prompt and check kinit's status before accepting the cache. Explicit `-c` selects this cache instead of replacing the user's default, but can replace an existing selected file; keep the selected path fresh. Verify the resulting default principal, ticket service and validity period; a cache file's existence alone is not success. Set `KRB5_CONFIG="$krb_config"` and `KRB5CCNAME="FILE:$cache_path"` in the actual intended consuming process's environment. A setting on the kinit invocation is not automatically exported to a later client. Some non-MIT clients expect different cache argument syntax; inspect their actual help.

Use absolute configuration/cache paths so changing directories does not change selection. Realm mapping and a reachable KDC enable ticket acquisition; service clients also need their actual FQDN/SPN. Putting the DC hostname before a domain alias in a hosts entry can affect canonical names on some name-service implementations, but is not a universal Kerberos requirement. MIT DNS canonicalization and reverse lookup settings are distinct, and an application such as OpenLDAP can additionally canonicalize names. Diagnose the principal actually requested before changing task-local settings. A successful TGT request does not prove a web/LDAP service accepts it or authorizes its requested operation.

For **PKINIT with an existing authorized certificate**, confirm the MIT PKINIT plugin is installed, the certificate/key match and the KDC supports it. Define `cert`, `key` and `ca_bundle` as absolute PEM paths, with the CA trust established independently:

~~~bash
KRB5_CONFIG="$krb_config" kinit -c "FILE:$cache_path" -X "X509_user_identity=FILE:$cert,$key" -X "X509_anchors=FILE:$ca_bundle" "$principal"
kinit_status=$?
if [ "$kinit_status" -eq 0 ]; then
  klist -c "FILE:$cache_path"
fi
~~~

The configuration spelling is `pkinit_identities`, not `pkinit_identites`. CSR validation is insufficient: the issued certificate, mapped principal, usages, trust chain and KDC certificate policy must agree. Inspect specific errors before changing EKU/SAN validation settings; weakening verification is not a routine repair.

For an **administrator-provisioned keytab** for the selected principal, define `keytab` as that existing private absolute file. Inspect entry metadata without printing key contents, then select it explicitly:

~~~bash
klist -k -e "$keytab"
KRB5_CONFIG="$krb_config" kinit -k -t "$keytab" -c "FILE:$cache_path" "$principal"
kinit_status=$?
if [ "$kinit_status" -eq 0 ]; then
  klist -c "FILE:$cache_path"
fi
~~~

A keytab is long-term credential material, distinct from a ticket cache. Its entry principal, key version and encryption type must fit current account/KDC policy; listing metadata does not validate the key online. A stale key or unsupported encryption type needs provisioning/policy evidence, not a default to weaker cryptography. Do not add `-f` unless ticket forwarding is part of the selected task. Keep the same cache verification, consumer selection and cleanup requirements as the password branch.

If a TCP-only proxy is involved, `[libdefaults] udp_preference_limit = 1` makes normal MIT requests prefer TCP, but does not disable fallback. Apply it in the task config and verify the transport actually used. Protect optional `KRB5_TRACE` output because it exposes environment and identity details.

After use, `kdestroy -c "FILE:$cache_path"` destroys this cache only. Do not destroy unrelated default/collection caches. Record the selected principal, cache and expiry without copying tickets into reports.

References: [kinit](https://web.mit.edu/kerberos/krb5-latest/doc/user/user_commands/kinit.html), [klist](https://web.mit.edu/kerberos/krb5-latest/doc/user/user_commands/klist.html), [configuration and PKINIT](https://web.mit.edu/kerberos/krb5-latest/doc/admin/conf_files/krb5_conf.html), [service principal naming and application canonicalization](https://web.mit.edu/kerberos/krb5-latest/doc/admin/princ_dns.html).
