---
name: impacket-dacledit
description: Inspect and save a selected AD object's DACL with Impacket dacledit from Linux. Use when checking graph-derived permission claims, interpreting trustee filters and inheritance, or assessing the scope of an existing DACL backup.
---

# Inspect a selected directory DACL

Check local help for `impacket-dacledit` or `dacledit.py`; packaged releases differ from upstream development versions. This procedure requires support for `-dc-host`, `-dc-ip`, `-use-ldaps` and the target selector below. Use a known, authorized directory identity and preserve required authentication/transport policy.

Define `dacledit_bin` as the verified executable, `domain` as the AD DNS domain, `user` as the cache's account, `dc_fqdn` as the actual DC hostname, `dc_ip` as its address, and `target_dn` as the exact object's distinguished name. Set `KRB5CCNAME` to an existing, valid cache's absolute path. Define `report` as a fresh private log path:

~~~bash
umask 077
"$dacledit_bin" "$domain/$user" -k -no-pass \
  -dc-host "$dc_fqdn" -dc-ip "$dc_ip" -use-ldaps \
  -action read -target-dn "$target_dn" >"$report" 2>&1
~~~

Read the log for a parsed DACL and errors. The reviewed entrypoint catches exceptions without consistently setting a failing exit status; a zero exit code or created log is insufficient. On a bind, name or target-lookup error, check cache identity/expiry, DC resolution, transport policy and the exact DN before interpreting permissions. `-no-pass` suppresses prompting; it does not supply credentials.

Start with the full DACL. Define `trustee_sid` as the SID being investigated; adding `-principal-sid "$trustee_sid"` filters the displayed trustees. Check the full printed SID: the reviewed implementation uses a substring test on the rendered trustee text. This filter neither expands group memberships nor computes effective access. No direct match therefore does not establish that the account lacks access. Keep the unfiltered result for applicable group and deny entries. Unresolved names or unsupported ACE messages leave interpretation incomplete.

| Parsed evidence | Interpretation and next check |
|---|---|
| Allow/deny type, access mask and trustee SID | Identify the actual principal and requested right; evaluate applicable entries together with the current security context. |
| Object/property GUID and inherited-object restriction | Resolve the GUID before translating an entry into control over a particular attribute, extended right or object class. |
| `INHERIT_ONLY_ACE` | The entry is intended for descendants and does not apply to the object carrying it. |
| Inheritance flags | Follow the directory container tree. Group membership is not container ancestry; an inheritable ACE on a group does not thereby apply to its member objects. |

Microsoft's [AD inheritance rules](https://learn.microsoft.com/en-us/windows/win32/ad/access-control-inheritance) explain applicability. Check actual inheritance protection and object class rather than inferring them from one printed flag or group name.

## Preserve the DACL without treating it as a full rollback

For a local backup of that same object's DACL, define `backup_file` as a new private filename and run:

~~~bash
"$dacledit_bin" "$domain/$user" -k -no-pass \
  -dc-host "$dc_fqdn" -dc-ip "$dc_ip" -use-ldaps \
  -action backup -target-dn "$target_dn" -file "$backup_file"
~~~

Confirm the logged output filename and stored DN. The tool may choose another filename when the requested path already exists. Its DACL-focused security-descriptor request is not an owner, membership or arbitrary-attribute snapshot. An automatic backup created during a later write cannot recover an earlier owner change, and it cannot undo changes to `member`, `userPrincipalName` or `msDS-KeyCredentialLink`. `restore` writes the saved DACL and can replace intervening ACL changes; do not use it as a read check.

Use the [upstream parser and read/backup implementation](https://github.com/fortra/impacket/blob/master/examples/dacledit.py) for release differences and unsupported ACE handling.
