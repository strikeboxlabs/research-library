---
name: windapsearch
description: Inspect AD users and custom attributes with the legacy Python windapsearch. Use to narrow full-attribute searches and interpret anonymous access, encoded values and misleading exit status.
---

# Select the implementation and directory view

These commands target ropnop's Python `windapsearch.py`; the Go rewrite has a different interface. Define `windap_script` as the installed script path and `dc_ip` as the selected DC. Read `python3 "$windap_script" --help` before applying these flags. The [Python project](https://github.com/ropnop/windapsearch) points to the separate Go implementation.

The Python implementation connects through plain `ldap://` and simple bind, without a TLS option. The commands below inspect permitted anonymous visibility. For password-based investigation requiring protected transport, use a client supporting verified StartTLS/LDAPS; do not send credentials through this script merely because it offers a password prompt. Anonymous RootDSE discovery succeeding does not establish access to user records.

~~~bash
python3 "$windap_script" --dc-ip "$dc_ip" -U --attrs 'distinguishedName,sAMAccountName,userPrincipalName,description'
~~~

`-U` selects users; lowercase `-u` supplies a bind identity. Retain each object's identity with its attributes. If the search returns no users, distinguish bind/search errors from a successful empty visible set before inferring that accounts do not exist.

# Inspect one identity before expanding attributes

Set `user_filter` to a reviewed LDAP filter selecting the account, for example the illustrative `(&(objectCategory=user)(sAMAccountName=svc-audit))`. Escape literal filter values using RFC 4515 rules; shell quoting does not escape LDAP syntax.

~~~bash
python3 "$windap_script" --dc-ip "$dc_ip" --custom "$user_filter" --full
~~~

Custom-query output includes DNs, which help disambiguate names. `--full` requests `*` attributes and overrides `--attrs`; it neither selects extra objects nor bypasses attribute ACLs or retrieves every operational attribute. After discovering a relevant custom field, repeat the same filter with `--attrs 'distinguishedName,sAMAccountName,observedAttribute'`, substituting its actual schema name, and omit `--full`.

The pretty printer can base64-encode nonprintable/binary values without LDIF's double-colon marker. Conversely, printable base64 may already be the stored application value. Confirm schema and raw representation before decoding; keep binary output in a file. A decoded unreadable value alone does not establish encryption. Group names describe membership, not effective permissions.

The upstream Python cleanup function exits **1 even after successful queries**. Preserve status, stdout and stderr together; do not treat that code alone as either success or failure. A result count describes that filter and bind view; paging cannot overcome missing rights. Check the [implementation](https://github.com/ropnop/windapsearch/blob/master/windapsearch.py) when packaged behavior differs.
