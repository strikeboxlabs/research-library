# Selected membership and ownership changes

Define the `ad` Bash array using the authenticated DC connection in the entrypoint. Resolve `group_dn`, `member_dn` or `target_dn` first. Read the current object and preserve the affected values in the task evidence before changing them. A graph edge suggests a permission to investigate; it does not replace a successful write and read-back.

## Add or remove a direct member

For an authorized membership change, capture the current member set, then add the selected principal:

~~~bash
"${ad[@]}" get object "$group_dn" --attr distinguishedName,member
"${ad[@]}" add groupMember "$group_dn" "$member_dn"
"${ad[@]}" get object "$group_dn" --attr distinguishedName,member
~~~

Compare the exact DN, not a substring of the account name. An already present member is not a new change owned by this task. If the request is temporary, remove only the member this task added and read back again:

~~~bash
"${ad[@]}" remove groupMember "$group_dn" "$member_dn"
"${ad[@]}" get object "$group_dn" --attr distinguishedName,member
~~~

Keep other membership changes intact. Directory membership becoming visible does not refresh an existing Kerberos ticket or process token; distinguish successful LDAP change from subsequent session authorization. After an uncertain connection failure, read current state before repeating the write.

## Change the owner

Read the security descriptor with SID resolution and record the owner SID, separately from the DACL:

~~~bash
"${ad[@]}" get object "$target_dn" --attr nTSecurityDescriptor --resolve-sd
"${ad[@]}" set owner "$target_dn" "$new_owner_sid"
"${ad[@]}" get object "$target_dn" --attr nTSecurityDescriptor --resolve-sd
~~~

Set `new_owner_sid` to the specifically authorized principal. Owner changes do not automatically add group members or grant every application permission. WRITE_OWNER commonly permits taking ownership as the caller; assigning an arbitrary other owner requires additional rights. Restoration to the original SID can therefore require an administrator even when taking ownership succeeded. Establish that recovery path before a temporary change, and verify the original owner after restoration.

Access denied, an invalid SID and a constraint violation are different failures. Check the precise object/right and server response; do not escalate a failed selected change into a broader grant by default. See the [owner and membership commands](https://github.com/CravateRouge/bloodyAD/wiki/User-Guide) for installed-version differences.
