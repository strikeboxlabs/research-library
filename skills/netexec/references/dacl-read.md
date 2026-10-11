# Read a selected directory object's DACL

Require the approved DC, existing single known login pair and attempt budget from the entrypoint. Check `ldap --help` and `ldap -M daclread --options` for this installation. Define `target_dn` as the exact known object's distinguished name. Use validated literal selector values: the reviewed module interpolates LDAP filters, and a selector matching a local filename can instead load multiple targets from that file.

Read allowed and denied ACEs separately, using the existing variables:

~~~bash
for ace_type in allowed denied; do
  "$nxc_bin" ldap "$target" -d "$domain" -u "$users_file" -p "$passwords_file" \
    --no-bruteforce -M daclread -o "TARGET_DN=$target_dn" ACTION=read "ACE_TYPE=$ace_type"
done
~~~

Keep the resolved target DN, trustee SID, ACE type, mask, object/property-set GUID and inheritance flags. `ACTION=read` queries and prints a DACL; the separate backup action writes local artifacts. This view is not a complete effective-access evaluation. The module's default allowed-only selection can hide denied ACEs. The reviewed current parser also loses type/flag fields on some ordinary ACEs, so omitted rows or debug parsing warnings require checking raw ACL data with another read-only directory facility rather than concluding no rights.

If a focused trustee comparison is needed, add `PRINCIPAL` only after verifying its resolved SID. This filters direct trustee matches; it does not expand nested groups, evaluate all token SIDs or recursively inspect other objects. A returned object-specific WriteProperty permission can identify a property set rather than every property. Resolve GUIDs against the deployed schema and applicable attribute-security GUIDs; a human-readable label alone does not prove permission to a chosen attribute.

For a Group Policy object, the directory object and its SYSVOL policy files are separate evidence. WriteProperty/CreateChild/GenericExecute labels on one object do not establish permission to create arbitrary policies, write every policy file, link the GPO or execute commands. Resolve the exact GUID/display name, file access, links, security/WMI filtering and computer/user scope when explaining intended policy application. A successful refresh or changed membership is distinct from a newly issued process token. Preserve that distinction without applying a privilege-changing policy to test it.

Authentication/descriptor-read errors, unresolved identities and unsupported ACE types remain coverage gaps. Finish with the target, observed ACEs and the limits above. Do not translate graph edges or one ACL row into permission for account, certificate or delegation changes. See the [module's options, query and filters](https://github.com/Pennyw0rth/NetExec/blob/main/nxc/modules/daclread.py) and [Group Policy processing](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-policy/group-policy-processing).
