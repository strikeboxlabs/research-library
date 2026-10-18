---
name: bloodyad
description: Read Active Directory objects and make selected LDAP membership or ownership changes with bloodyAD. Use when a worker needs a Linux AD administration client, exact object identity, or verification of a delegated directory write.
---

# Resolve the object and select the LDAP action

Read this entire SKILL.md before acting; reuse complete current context. Require the selected object/DC and known authenticated context, then choose the read or authorized write. For writes, read [membership and ownership](references/directory-changes.md) fully before the procedure. Finish with exact object identity, operation/read-back evidence and unresolved access or lifecycle gaps; authentication, permission to read and permission to change are separate findings.

Check `bloodyAD --help` and the selected subcommand's help. For a current build accepting explicit cache selection, define `cache`, `domain`, `user`, `dc_fqdn`, `dc_ip` and `target_dn`:

~~~bash
ad=(bloodyAD -k "ccache=$cache" -d "$domain" -u "$user" -H "$dc_fqdn" -i "$dc_ip" -s)
"${ad[@]}" get object "$target_dn" --attr distinguishedName,objectSid,member
~~~

Use a cache matching the identity and domain. `-H` identifies the server; `-i` supplies its address. Keep Kerberos names, DNS and time coherent. `-s` selects LDAPS in current builds; `-ss` removes transport protection and is not a stronger form of `-s`. A TLS/bind error occurs before the object query; changing the search filter will not fix it.

Use a DN or resolved SID when a display name could select the wrong object. Restrict attributes to the question. Group `member` values describe that object's direct membership, not every nested group or an already issued token. An empty query, unreadable attribute and absent attribute need different conclusions; retain the diagnostic and selected base/object.

For an inherited-permission discrepancy, compare the selected object's actual security descriptor, applicable ACE class/inheritance restrictions and current protected-group membership. `adminCount=1` can persist after protected-group removal; it alone does not prove current protection or the DACL inheritance state. A parent OU grant does not establish effective rights on every descendant. Clearing that attribute alone is not an inheritance repair. Preserve these separate observations for the directory administrator; see [Microsoft's protected-account guidance](https://learn.microsoft.com/windows-server/identity/ad-ds/plan/security-best-practices/appendix-c--protected-accounts-and-groups-in-active-directory).

The [upstream guide](https://github.com/CravateRouge/bloodyAD/wiki/User-Guide) documents additional actions. Choose the smallest matching action rather than a broad grant merely because a walkthrough used one.

Two action-specific notes verified in practice: `add rbcd <target> <service>` writes the binary security-descriptor attribute `msDS-AllowedToActOnBehalfOfOtherIdentity` (note the full attribute name; `msDS-AllowedToActTo` is not the stored attribute, and pushing SDDL text via raw `ldapmodify` fails with `Error in attribute conversion` because the value must be a binary SD). `set password <dn> <new>` exercises the `User-Force-Change-Password` reset right and needs no current password, unlike `net user <name> <pw> /domain`, which performs change semantics and fails without the old password; on Windows hosts the equivalent reset is `Set-ADAccountPassword -Reset`. `set object` on unknown schema attributes can reject the value's conversion type before any LDAP write — prefer the dedicated subcommand when one exists.

RODC chains hinge on who can rewrite the Password Replication Policy. Decode the RODC computer object's full security descriptor and resolve every trustee: the PRP attributes (`msDS-NeverRevealGroup`, `msDS-RevealOnDemandGroup`) are attribute-scoped WriteProperty grants, commonly held by the domain "RODC Administrators" group rather than by the principal you already control — and that group typically carries a `Self`/Member ACE for a tier group (observed: Tier 1 members could add themselves). Join through that self-membership right first, then rewrite the PRP with `set object` (REPLACE semantics; no `-v` clears the attribute, and deny-list entries always override allow-list entries, so clear `msDS-NeverRevealGroup` before adding the victim to `msDS-RevealOnDemandGroup`). Only then will a KDC accept a krbtgt_%d-signed golden ticket for a privileged user and answer a Kerberos KEY_LIST request with the account's real hash.
