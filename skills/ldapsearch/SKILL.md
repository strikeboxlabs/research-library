---
name: ldapsearch
description: Query LDAP directories from Linux with OpenLDAP ldapsearch. Use for AD identities/policy/deleted objects or POSIX users/groups, with correct naming contexts, authentication and incomplete-result interpretation.
---

# Choose the directory model before querying

Read this entire SKILL.md before acting; reuse complete current context. Retain bind identity, selected naming context, returned DNs and final result status. Read the applicable reference fully before its procedure: [POSIX users/groups](references/posix-identities.md), [AD lockout policy](references/lockout-policy.md), or [AD deleted objects](references/deleted-objects.md). The discovery/SPN example below is AD-specific; omitted attributes or partial searches are not proof of absence.

Use OpenLDAP `ldapsearch`; inspect `ldapsearch -VV` and installed options. `-x` selects simple bind, not NTLM. `-Y GSSAPI` selects SASL Kerberos and needs a usable ticket cache, realm/name configuration and the SASL mechanism on the client.

RootDSE is the server-specific entry with the empty DN, queried using `-b '' -s base`. A DN returned in `namingContexts` identifies a directory naming context, not RootDSE itself. An empty displayed `dn:` is therefore expected in this discovery result. Select the relevant returned context for subsequent searches; do not assume an AD-only `defaultNamingContext` exists on another directory implementation. RootDSE readability does not establish access to entries or attributes under that context. See [RFC 4512 server metadata](https://www.rfc-editor.org/rfc/rfc4512.html#section-5.1).

Define `dc_fqdn` as the DC's verified DNS name and `bind_upn` as the known `user@domain` identity. Discover the directory base through a RootDSE base search. For password-based simple bind over required StartTLS:

~~~bash
ldapsearch -LLL -x -ZZ -H "ldap://$dc_fqdn" -D "$bind_upn" -W -b '' -s base '(objectClass=*)' defaultNamingContext
~~~

`-W` prompts for the password. If StartTLS/certificate validation fails, resolve trust/support or use an appropriate authenticated transport; do not silently remove `-ZZ`. LDAPS uses `ldaps://` without `-ZZ`. For a Kerberos-only account, perform the same RootDSE base/filter query with GSSAPI authentication as below; simple bind is not a prerequisite.

Set `base_dn` to the returned `defaultNamingContext`. For Kerberos, select an existing cache with `KRB5CCNAME`, check its identity/expiry with `klist`, then query enabled person/user objects with SPNs:

~~~bash
filter='(&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2))(servicePrincipalName=*))'
ldapsearch -LLL -Y GSSAPI -H "ldap://$dc_fqdn" -b "$base_dn" -s sub -E pr=500/noprompt -o ldif_wrap=no "$filter" sAMAccountName servicePrincipalName description
~~~

The bitwise condition excludes disabled accounts; it does not prove they can log in. Remove the SPN condition when investigating all enabled users. Search the domain base rather than assuming every user lives under `CN=Users`. Retain DNs and multivalued attributes; LDIF `::` denotes base64 values, and grep-only output can lose their association. Paging addresses ordinary result-page limits; check final status for time/size limits or access restrictions.

A DN appearing in a broader query but missing from username-only output does not establish that it is a different object class. With the same bind context, inspect the observed DN using `-b "$observed_dn" -s base '(objectClass=*)' objectClass sAMAccountName description`. Filters and attribute visibility can change apparent coverage. CNs and home-directory names are candidate identities, not verified login names. Use an explicit presence filter, not a standalone `'*'`.

Read-only-domain-controller indicators are queryable directly: `krbtgt_%d` accounts among users, and computer objects whose `userAccountControl` carries bit `0x4000000` (PARTIAL_SECRETS_ACCOUNT). On such a computer object request `msDS-RevealedList`, `msDS-RevealOnDemandGroup`, `msDS-NeverRevealGroup`, `msDS-AuthenticatedToAccountlist` and `msDS-KrbTgtLink`: `msDS-RevealedList` values are `S:<ver>:<secretAttr>:<DN>` records naming exactly whose `unicodePwd`/`supplementalCredentials` are cached on that RODC — a privileged-account DN there is a domain-compromise lead. Fetch these with `-o ldif-wrap=no` and never pipe a multi-valued dump through `head`/`grep` when enumerating: an early truncation silently drops later values and reads as absence. OpenLDAP `ldapsearch` rejects the AD SD flags extension (`-E '!sdflags=4'` → `Invalid search extension name`); to read `nTSecurityDescriptor` DACLs use an LDAP library where the raw OID control `1.2.840.113556.1.4.801` (value `b'\x30\x03\x02\x01\x04'`) can be attached, then decode with `impacket.ldap.ldaptypes.SR_SECURITY_DESCRIPTOR` (note the `SR_` prefix; plain `SECURITY_DESCRIPTOR` does not exist there), mapping ACE ObjectType bytes through `uuid.UUID(fields_le=...)` against the schema's `schemaIDGUID` map. Attribute-scoped writes inherited from an OU are easy to miss in parsed ACL dumps; the raw SD shows the exact attribute GUID the trustee may write.

Keep the positional search filter separate from the requested attribute names. In OpenLDAP, a remaining argument without an opening parenthesis or equals sign is an attribute selector; the omitted filter defaults to `(objectclass=*)`. A trailing `Administrator` therefore does not select that account. Supply an explicit filter and then the required attributes; `'*'` selects user attributes, not a username. Retain the actual filter, base, scope and final LDAP result, rather than inferring them from a shell comment.

When inserting a literal value into a filter, apply RFC 4515 escaping: `*` → `\2a`, `(` → `\28`, `)` → `\29`, backslash → `\5c`, NUL → `\00`. Use a proper filter-escaping routine for arbitrary input; DN escaping and HTTP percent encoding solve different problems. An unescaped `*` changes equality into a presence/substring search. Zero entries, malformed-filter errors and access-denied results must stay distinct; a web application's wildcard behavior is not a universal LDAP end-of-string test.

| Failure | Next check |
|---|---|
| `no mechanism available` | Client SASL GSSAPI support, before retrying credentials. |
| Service principal not found | Service FQDN, DNS canonicalization, realm and registered SPN; an IP alone may select the wrong principal. |
| Clock-skew or expired-ticket error | Actual client/DC time or cache lifetime; do not automatically reset the host clock. |
| Bind restriction/error `52f` | Verify the authentication method and account policy. This alone does not prove Protected Users membership. |
