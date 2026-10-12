# Query a POSIX directory without assuming AD attributes

Use the approved directory endpoint and credentials. Define `ldap_host` as its verified DNS name and `bind_dn` as the known full bind DN. Simple bind here requires StartTLS and trusted certificates:

~~~bash
ldapsearch -LLL -x -ZZ -H "ldap://$ldap_host" -D "$bind_dn" -W -b '' -s base '(objectClass=*)' namingContexts
~~~

Choose `base_dn` from the returned naming contexts or verified directory configuration. `defaultNamingContext`, `sAMAccountName` and AD bitwise filters are not portable POSIX-directory assumptions. A readable SSSD configuration can identify the provider/base, but package presence or a large Linux UID alone cannot.

For one known group's exact `group_dn`, inspect the base object rather than dumping the entire directory:

~~~bash
ldapsearch -LLL -x -ZZ -H "ldap://$ldap_host" -D "$bind_dn" -W -b "$group_dn" -s base '(objectClass=posixGroup)' cn gidNumber memberUid
~~~

RFC 2307 `memberUid` values are login names, not DNs. The group has a numeric `gidNumber`; a user's primary `gidNumber` can establish membership without that name appearing in the group's `memberUid` list. Other schemas may instead use DN-valued `member` attributes. Inspect the actual object classes before composing filters. A custom `corpMemberOf`-like attribute has application-defined semantics and is not proof of transitive/effective OS membership.

For one selected `user_dn` obtained from a correctly escaped UID query or known directory entry:

~~~bash
ldapsearch -LLL -x -ZZ -H "ldap://$ldap_host" -D "$bind_dn" -W -b "$user_dn" -s base '(objectClass=posixAccount)' uid uidNumber gidNumber homeDirectory loginShell
~~~

Request only the needed attributes; do not request `userPassword` simply to resolve identity. Retain final LDAP status and each entry DN. A successful base search identifies one directory object; Linux NSS caching, mapping and current process groups still affect actual access. Use keyed NSS/account evidence for that layer. A denied attribute, zero entries or unsupported schema needs separate diagnosis, not a broader credential dump or plaintext-bind fallback.

`-x` selects simple bind, not anonymous identity. A nonempty bind DN with no password is an unauthenticated bind and can be rejected separately from a search ACL denial; preserve that diagnostic rather than calling both anonymous-search failure. Use the provisioned credential through `-W` and the selected protected transport. An entry's `description: LDAP administrator` is editable descriptive data, not proof of write privileges or server policy. Search access does not establish modification rights. Likewise, a user's `gidNumber` is its directory primary-group value; do not describe it as a supplementary-group addition or infer sudo authority from a conventional numeric GID. Finish identity diagnosis with the actual NSS/process mapping and applicable policy, without changing directory attributes as a probe.

References: [OpenLDAP search options](https://www.openldap.org/software/man.cgi?query=ldapsearch), [RFC 2307 schema](https://www.rfc-editor.org/rfc/rfc2307.html).
