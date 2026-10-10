# Grant or remove one selected directory right

Use the exact target DN, trustee SID and intended right from the task. Confirm the caller can edit that DACL and preserve an explicit fresh backup and full read before changing it. A graph edge or object ownership alone is not proof that this particular write will succeed. Keep the entrypoint's `dacledit_bin`, `domain`, `user`, `dc_fqdn`, `dc_ip`, `target_dn` and Kerberos cache context.

For a selected group's membership delegation, define `trustee_sid` as the intended delegate. This grants a right on the group; it does not add anyone as a member:

~~~bash
"$dacledit_bin" "$domain/$user" -k -no-pass -dc-host "$dc_fqdn" \
  -dc-ip "$dc_ip" -use-ldaps -target-dn "$target_dn" \
  -principal-sid "$trustee_sid" -action write -rights WriteMembers
"$dacledit_bin" "$domain/$user" -k -no-pass -dc-host "$dc_fqdn" \
  -dc-ip "$dc_ip" -use-ldaps -target-dn "$target_dn" -action read
~~~

Check the LDAP write result and the actual new ACE: trustee, allow/deny, property GUID, mask and inheritance flags. `WriteMembers` concerns the member attribute; `ResetPassword` is an extended right. `FullControl` is broader and is the reviewed parser's default, so never omit `-rights` when intending a narrow grant. `DCSync` creates replication rights and is not a synonym for group management.

Do not add `-inheritance` automatically. It changes propagation to descendants of a container/OU; group membership is not directory ancestry. Protected objects and actual ACE flags govern applicability. Verify the specific intended operation under the delegate's security context when that test is authorized; a printed ACE is not the complete effective-rights computation.

For removal of the owned, previously absent grant, select the same target, trustee, ACE type/right and inheritance settings with `-action remove`. Compare with the pre-state first: removing a matching ACE that already existed would remove someone else's delegation. Reread the full DACL after the removal.

An explicit restore uses the saved file:

~~~bash
"$dacledit_bin" "$domain/$user" -k -no-pass -dc-host "$dc_fqdn" \
  -dc-ip "$dc_ip" -use-ldaps -action restore -file "$backup_file"
~~~

Inspect the backup's stored DN before restoring. A full DACL restore can overwrite intervening legitimate changes; reconcile concurrent edits rather than treating it as an unconditional undo. It restores neither object ownership nor membership/password/UPN/key-credential changes made through other operations. Report those states separately.

The entrypoint can log an exception without a reliable failing process status; verify the server result and post-state, not just exit code. See [upstream actions and right construction](https://github.com/fortra/impacket/blob/master/examples/dacledit.py).
