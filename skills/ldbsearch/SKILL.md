---
name: ldbsearch
description: Inspect records in an offline SSSD LDB cache while preserving identity and attribute context. Use when strings output cannot map a value to an account or a cache query appears empty.
---

# Inspect an SSSD cache as records

Read this entire SKILL.md before acting. Require a consistent acquired cache and compatible parser, preserve selected record/attribute identity, and finish with query status plus supported mapping. A cache hit or recovered offline verifier does not establish a current login.

Use an already acquired, consistent copy of the selected domain cache, typically `cache_<domain>.ldb` under `/var/lib/sss/db`. Confirm the actual path and SSSD version from acquisition evidence. A live-file copy made during writes may be inconsistent. Keep the original untouched; operate on a disposable working copy with compatible LDB libraries/modules. Do not clear or rebuild the service cache to make an evidence query work.

Check `ldbsearch --help`. Define `cache` as the absolute path to the existing local working copy, and `inventory` as a fresh private output file. Use an explicit `-H` so an ambient `LDB_URL` cannot select another database or a remote service:

~~~bash
umask 077
test -f "$cache" && ldbsearch -H "$cache" -b 'cn=sysdb' -s sub '(name=*)' name objectClass objectCategory uidNumber gidNumber >"$inventory"
~~~

Require a successful command before interpreting the saved LDIF. Preserve complete records, including each `dn:`. An **illustrative** record with `name: analyst@example.test` and `uidNumber: 10042` associates those fields in this cache; it does not establish that the account can currently authenticate. Choose an observed DN rather than constructing one from a short username.

For a selected record, define `user_dn` as its exact DN and `record` as a fresh private output:

~~~bash
ldbsearch -H "$cache" -b "$user_dn" -s base '(name=*)' name uidNumber originalDN lastUpdate lastOnlineAuth >"$record"
~~~

`base` selects that record, while `sub` searches descendants as well. Missing attributes and zero matching records are different outcomes. On zero/error, check the chosen domain cache, base DN, filter, read permissions and LDB/module compatibility before declaring an identity absent. Stale data and an incomplete acquisition remain possible even with successful parsing.

When an authorised offline credential audit specifically requires the verifier, add `cachedPassword cachedPasswordType` to the **selected-record** attribute list and keep that output private. Preserve its DN/name association. A `$6$` value is a sha512crypt verifier, not an NT hash or Kerberos ticket; other values require producer/version verification. SSSD process names or a domain-like cache filename alone do not prove working Active Directory membership. Identity caching and cached authentication have distinct purposes. SSSD cache LDB files are state databases, not log files. In an acquired `sssd.conf`, `cache_credentials = true` permits password-verifier caching; it does not mean every GSSAPI login stored a password or that all Kerberos tickets appear there. A `simple_allow_groups` entry matters when the configured access provider is `simple`; a textual group name alone is not current access policy. Keep identity lookup, authentication and access-provider decisions separate and compare the actual selected record/configuration rather than inferring membership from a process name.

LDIF can fold lines and base64-encode values (`attribute:: value`). Decode according to [LDIF syntax](https://www.rfc-editor.org/rfc/rfc2849.html) before using a value; do not sort extracted lines or assume every colon separates plaintext. Keep command status, cache acquisition context and the selected record together. This procedure searches a copy; it is not a cache repair or a live directory query.

Resolve syntax with the [upstream ldbsearch manual](https://github.com/samba-team/samba/blob/master/lib/ldb/man/ldbsearch.1.xml), and cache/schema differences with [SSSD cache troubleshooting](https://sssd.io/troubleshooting/backend.html), its [local LDB query example](https://sssd.io/troubleshooting/sudo.html) and [attribute definitions](https://github.com/SSSD/sssd/blob/master/src/db/sysdb.h).
