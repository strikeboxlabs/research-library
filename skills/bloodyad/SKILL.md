---
name: bloodyad
description: Read Active Directory objects and make selected LDAP membership or ownership changes with bloodyAD. Use when a worker needs a Linux AD administration client, exact object identity, or verification of a delegated directory write.
---

# Resolve the object and select the LDAP action

Read this entire file before acting. For writes, read [membership and ownership](references/directory-changes.md) fully. Finish with the exact object/DC and observed result; authentication, permission to read and permission to change are separate findings.

Check `bloodyAD --help` and the selected subcommand's help. For a current build accepting explicit cache selection, define `cache`, `domain`, `user`, `dc_fqdn`, `dc_ip` and `target_dn`:

~~~bash
ad=(bloodyAD -k "ccache=$cache" -d "$domain" -u "$user" -H "$dc_fqdn" -i "$dc_ip" -s)
"${ad[@]}" get object "$target_dn" --attr distinguishedName,objectSid,member
~~~

Use a cache matching the identity and domain. `-H` identifies the server; `-i` supplies its address. Keep Kerberos names, DNS and time coherent. `-s` selects LDAPS in current builds; `-ss` removes transport protection and is not a stronger form of `-s`. A TLS/bind error occurs before the object query; changing the search filter will not fix it.

Use a DN or resolved SID when a display name could select the wrong object. Restrict attributes to the question. Group `member` values describe that object's direct membership, not every nested group or an already issued token. An empty query, unreadable attribute and absent attribute need different conclusions; retain the diagnostic and selected base/object.

The [upstream guide](https://github.com/CravateRouge/bloodyAD/wiki/User-Guide) documents additional actions. Choose the smallest matching action rather than a broad grant merely because a walkthrough used one.
