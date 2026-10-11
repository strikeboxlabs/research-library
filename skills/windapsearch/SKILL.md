---
name: windapsearch
description: Inspect AD users, groups and selected attributes with the legacy Python windapsearch. Use to distinguish direct membership from effective access and interpret anonymous views, encoded values and misleading exit status.
---

# Select the implementation and directory view

Read this entire SKILL.md before acting. Select the implementation, permitted bind view and user/group or selected-object task below; use full attributes only for the selected-object task. Required prerequisites are the installed script/Python LDAP dependencies, reachable directory and permitted search view. Finish with returned DNs, attributes, status and diagnostics or the concrete transport/access prerequisite gap.

These commands target ropnop's Python `windapsearch.py`; the Go rewrite has a different interface. Define `windap_script` as the installed script path and `dc_ip` as the selected DC. Read `python3 "$windap_script" --help` before applying these flags. The [Python project](https://github.com/ropnop/windapsearch) points to the separate Go implementation.

The Python implementation connects through plain `ldap://` and simple bind, without a TLS option. The commands below inspect permitted anonymous visibility. For password-based investigation requiring protected transport, use a client supporting verified StartTLS/LDAPS; do not send credentials through this script merely because it offers a password prompt. Anonymous RootDSE discovery succeeding does not establish access to user records.

~~~bash
python3 "$windap_script" --dc-ip "$dc_ip" -U --attrs 'distinguishedName,sAMAccountName,userPrincipalName,description'
~~~

`-U` selects users; lowercase `-u` supplies a bind identity. Retain each object's identity with its attributes. If the search returns no users, distinguish bind/search errors from a successful empty visible set before inferring that accounts do not exist. Do not derive logon identities by grepping every line containing `@` and stripping UPN suffixes: accounts can lack UPNs, UPN prefixes can differ from sAMAccountName, and different domains can collapse to one string. Preserve the DN/attribute associations before creating any requested local inventory.

# Inspect one identity before expanding attributes

Set `user_filter` to a reviewed LDAP filter selecting the account, for example the illustrative `(&(objectCategory=user)(sAMAccountName=svc-audit))`. Escape literal filter values using RFC 4515 rules; shell quoting does not escape LDAP syntax.

~~~bash
python3 "$windap_script" --dc-ip "$dc_ip" --custom "$user_filter" --full
~~~

Custom-query output includes DNs, which help disambiguate names. `--full` requests `*` attributes and overrides `--attrs`; it neither selects extra objects nor bypasses attribute ACLs or retrieves every operational attribute. After discovering a relevant custom field, repeat the same filter with `--attrs 'distinguishedName,sAMAccountName,observedAttribute'`, substituting its actual schema name, and omit `--full`.

The pretty printer can base64-encode nonprintable/binary values without LDIF's double-colon marker. Conversely, printable base64 may already be the stored application value. Confirm schema and raw representation before decoding; keep binary output in a file. A decoded unreadable value alone does not establish encryption.

# Read group metadata without claiming effective access

For a permitted group inventory, use the same selected DC and anonymous-view prerequisites:

~~~bash
python3 "$windap_script" --dc-ip "$dc_ip" -G --attrs 'distinguishedName,cn,memberOf'
~~~

`-G` selects group objects, rather than recursively resolving one user's effective memberships. For one known group, reuse the selected-object custom filter with `objectCategory=group` and only the needed attributes. Preserve each object's DN and its direct `memberOf` links. Those links alone omit recursive closure and primary-group membership; missing values or inaccessible objects leave the chain incomplete. A returned group name or membership path does not prove a service's effective token, endpoint ACL or successful WinRM access. See [membership security properties](https://learn.microsoft.com/en-us/windows/win32/ad/security-properties).

For a known selected group's **direct** member attributes, define `group_dn` as its complete verified DN:

~~~bash
python3 "$windap_script" --dc-ip "$dc_ip" -m "$group_dn"
~~~

The reviewed `-m` implementation reads `member`, rather than recursively expanding nested groups or resolving primary-group membership. A short name can trigger fuzzy selection and an interactive choice between matches; use the established DN for a worker. Returned byte-looking DN values are members to resolve, not UPNs or a verified WinRM authorization decision. Combining -U adds a separate user inventory; it does not scope that inventory to this group. A missing member attribute is not proof that no effective members exist.

`--admin-objects` instead filters `adminCount=1`. That attribute is a historical protection clue, not a complete effective-administrator inventory or proof of current privileged membership. A zero-result anonymous view does not prove that the directory has no administrators.

The upstream Python cleanup function exits **1 even after successful queries**. Preserve status, stdout and stderr together; do not treat that code alone as either success or failure. A result count describes that filter and bind view; paging cannot overcome missing rights. Check the [implementation](https://github.com/ropnop/windapsearch/blob/master/windapsearch.py) when packaged behavior differs.
