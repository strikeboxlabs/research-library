---
name: ldapsearch
description: Query Active Directory from Linux with OpenLDAP ldapsearch using simple bind or Kerberos GSSAPI. Use for choosing a base DN, paged user/SPN searches and interpreting authentication or incomplete-result errors.
---

# Ldapsearch against Active Directory

Use OpenLDAP `ldapsearch`; inspect `ldapsearch -VV` and installed options. `-x` selects simple bind, not NTLM. `-Y GSSAPI` selects SASL Kerberos and needs a usable ticket cache, realm/name configuration and the SASL mechanism on the client.

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

When inserting a literal value into a filter, apply RFC 4515 escaping: `*` → `\2a`, `(` → `\28`, `)` → `\29`, backslash → `\5c`, NUL → `\00`. Use a proper filter-escaping routine for arbitrary input; DN escaping and HTTP percent encoding solve different problems. An unescaped `*` changes equality into a presence/substring search. Zero entries, malformed-filter errors and access-denied results must stay distinct; a web application's wildcard behavior is not a universal LDAP end-of-string test.

| Failure | Next check |
|---|---|
| `no mechanism available` | Client SASL GSSAPI support, before retrying credentials. |
| Service principal not found | Service FQDN, DNS canonicalization, realm and registered SPN; an IP alone may select the wrong principal. |
| Clock-skew or expired-ticket error | Actual client/DC time or cache lifetime; do not automatically reset the host clock. |
| Bind restriction/error `52f` | Verify the authentication method and account policy. This alone does not prove Protected Users membership. |

Documentation reviewed 2026-10-09; Linux execution untested. Cases: Absolute pp. 7–9; Active pp. 6–8; Analysis pp. 8–10. Sources: [OpenLDAP manual](https://github.com/openldap/openldap/blob/master/doc/man/man1/ldapsearch.1), [Microsoft account flags](https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/useraccountcontrol-manipulate-account-properties), [Kerberos troubleshooting](https://web.mit.edu/kerberos/krb5-latest/doc/admin/troubleshoot.html), [RFC 4515 filters](https://www.rfc-editor.org/rfc/rfc4515.html).
