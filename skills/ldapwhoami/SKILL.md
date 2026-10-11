---
name: ldapwhoami
description: Verify the authorization identity returned by an OpenLDAP Who Am I operation using an existing Kerberos context. Use when a ticket cache, SASL mechanism, service hostname or security-layer message is being mistaken for proof of directory permissions.
---

# Verify the selected LDAP bind identity

Read this entire SKILL.md before acting. Require the authorized LDAP endpoint, installed OpenLDAP client with GSSAPI SASL support, existing usable cache and established realm/transport settings. All steps are inline. Finish with the server's returned authorization identity and final status; a SASL startup message or local cache listing alone is incomplete.

Define `ldap_uri` as one actual protocol/host/port URI, `krb_config` as the established absolute Kerberos configuration and `cache` as the existing provider-supported cache name. Use the actual service FQDN rather than guessing an IP-based principal. Check the client version without binding, then perform the selected operation:

~~~bash
ldapwhoami -VV
KRB5_CONFIG="$krb_config" KRB5CCNAME="$cache" \
  ldapwhoami -Y GSSAPI -H "$ldap_uri" -o nettimeout=10
status=$?
~~~

`-Y GSSAPI` selects that SASL mechanism; it is not simple bind or a username/password retry. `-H` accepts protocol/host/port rather than an LDAP search DN/filter. `nettimeout` bounds connection establishment, not every later protocol operation. Retain diagnostics and final status. This bind and extended operation reads the session identity rather than enumerating the directory.

Keep the deployment's transport policy: `ldaps://` uses TLS directly; for an endpoint requiring StartTLS over `ldap://`, add `-ZZ` so TLS must succeed. Do not disable certificate verification to turn a trust failure into a successful identity claim. A non-TLS GSSAPI session can negotiate a SASL security layer; its reported SSF describes that session, not proof that server-wide signing or TLS channel-binding policies are enforced. A channel-binding token applies to a TLS-backed authentication session.

The final `u:...` or `dn:...` is the server-returned authorization identity. SASL username can differ from that identity. An empty successful Who Am I response can indicate anonymous authorization rather than the intended account. Confirm the documented server mapping and task's expected identity. This result does not establish arbitrary attribute access, group membership or permission to modify objects.

If service-principal lookup selects an unexpected reverse-DNS name, investigate the actual names first. OpenLDAP may canonicalize independently of MIT's `rdns` setting. On the verified client, `-N` disables its reverse-DNS SASL hostname canonicalization for this invocation; use it only when the intended service name is independently established. A missing GSSAPI mechanism, expired cache, unsupported Who Am I operation, policy rejection and name mismatch need different repairs. No unsupported-operation response should be reported as a verified identity.

References: [OpenLDAP command contract](https://github.com/openldap/openldap/blob/OPENLDAP_REL_ENG_2_6/doc/man/man1/ldapwhoami.1), [MIT/OpenLDAP canonicalization distinction](https://web.mit.edu/kerberos/krb5-latest/doc/admin/princ_dns.html).
