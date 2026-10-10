---
name: ldapsearch
description: Query Active Directory from Linux with OpenLDAP ldapsearch using simple bind or Kerberos GSSAPI. Use for choosing a base DN, paged user/SPN searches, effective lockout policy, deleted-object visibility and interpreting authentication or incomplete-result errors.
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

A DN appearing in a broader query but missing from username-only output does not establish that it is a different object class. With the same bind context, inspect the observed DN using `-b "$observed_dn" -s base '(objectClass=*)' objectClass sAMAccountName description`. Filters and attribute visibility can change apparent coverage. CNs and home-directory names are candidate identities, not verified login names. Use an explicit presence filter, not a standalone `'*'`.

When inserting a literal value into a filter, apply RFC 4515 escaping: `*` → `\2a`, `(` → `\28`, `)` → `\29`, backslash → `\5c`, NUL → `\00`. Use a proper filter-escaping routine for arbitrary input; DN escaping and HTTP percent encoding solve different problems. An unescaped `*` changes equality into a presence/substring search. Zero entries, malformed-filter errors and access-denied results must stay distinct; a web application's wildcard behavior is not a universal LDAP end-of-string test.

## Read lockout policy for a selected user

Use the established authenticated connection and domain `base_dn`. Define `user_dn` as the exact DN of the selected user. Query the domain defaults and the user's resultant password-settings object separately:

~~~bash
ldapsearch -LLL -x -ZZ -H "ldap://$dc_fqdn" -D "$bind_upn" -W -b "$base_dn" -s base '(objectClass=*)' lockoutThreshold lockoutDuration lockOutObservationWindow
ldapsearch -LLL -x -ZZ -H "ldap://$dc_fqdn" -D "$bind_upn" -W -b "$user_dn" -s base '(objectClass=*)' sAMAccountName msDS-ResultantPSO
~~~

If `msDS-ResultantPSO` returns a DN, set `pso_dn` to that exact value and inspect its settings:

~~~bash
ldapsearch -LLL -x -ZZ -H "ldap://$dc_fqdn" -D "$bind_upn" -W -b "$pso_dn" -s base '(objectClass=*)' msDS-LockoutThreshold msDS-LockoutDuration msDS-LockoutObservationWindow
~~~

**Illustrative:** domain `lockoutThreshold: 0` alongside a selected user's resultant `msDS-LockoutThreshold: 5` means the domain-default observation did not settle that user's policy. Zero disables count-based lockout for the policy in question; it does not establish unlimited retries across applications or permission to try credentials. An omitted/denied attribute is not zero. If no resultant PSO is returned, establish successful object/attribute visibility before falling back to domain defaults; keep unresolved visibility as a limitation.

Preserve the DN, queried DC, bind identity and collection time with policy values. This reads configured policy, not current lockout state or the success of a particular authentication attempt. Microsoft's [resultant-policy documentation](https://learn.microsoft.com/en-us/powershell/module/activedirectory/get-aduserresultantpasswordpolicy) explains the user/group precedence behind `msDS-ResultantPSO`.

| Failure | Next check |
|---|---|
| `no mechanism available` | Client SASL GSSAPI support, before retrying credentials. |
| Service principal not found | Service FQDN, DNS canonicalization, realm and registered SPN; an IP alone may select the wrong principal. |
| Clock-skew or expired-ticket error | Actual client/DC time or cache lifetime; do not automatically reset the host clock. |
| Bind restriction/error `52f` | Verify the authentication method and account policy. This alone does not prove Protected Users membership. |

## Inspect deleted-object evidence

A normal AD search hides deleted objects. Using the same verified TLS/bind context, inspect RootDSE `supportedControl` and the naming context before changing the query. For the domain's usual Deleted Objects container:

~~~bash
deleted_base="CN=Deleted Objects,$base_dn"
ldapsearch -LLL -x -ZZ -H "ldap://$dc_fqdn" -D "$bind_upn" -W -b "$deleted_base" -s one -E '!1.2.840.113556.1.4.417' -E pr=500/noprompt '(isDeleted=TRUE)' objectGUID isDeleted isRecycled sAMAccountName lastKnownParent msDS-LastKnownRDN
~~~

The critical Show Deleted control has no value. `!` prevents silently ignoring an unsupported control. This changes visibility, not permissions: an empty result or denied container is not proof that no deletion occurred. Confirm the naming context/container and delegated list/read rights; a custom group named "AD Recycle Bin" does not by itself establish those rights or that the feature is enabled.

Select the returned deleted DN or correlate the retained `objectGUID`; a display name is not unique and may no longer be retained. To inspect one object, repeat the control with `-b "$deleted_dn" -s base '(isDeleted=TRUE)'` and explicitly requested identity/custom attributes. Use an LDIF-aware reader for encoded DNs and binary GUIDs; do not paste a base64 GUID into a text equality filter.

Retained fields depend on deletion state, schema and visibility. Recycle Bin retention is finite. Show Deleted includes tombstones/deleted objects but excludes recycled objects; when that distinction matters and the server supports it, Show Recycled (`1.2.840.113556.1.4.2064`) includes all three. Neither control recovers garbage-collected data. Consult Microsoft's [control comparison](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/4b8f2a0e-9ea6-4be3-b639-4b019948c568) and [object lifecycle](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/538ec135-1465-4266-bb0a-777924f02846) for missing-field cases. A recovered historical value is evidence of that object, not proof of another account's current credentials.
