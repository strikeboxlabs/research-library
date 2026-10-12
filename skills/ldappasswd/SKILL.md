---
name: ldappasswd
description: Set a selected administered LDAP entry password through OpenLDAP Password Modify. Use to distinguish bind credentials, the changed identity and unsupported extended operations.
---

# Keep bind and target identities separate

Read this entire SKILL.md before acting. Require the administered LDAP endpoint, permitted bind identity and exact target entry. No conditional resources are required. Finish with the operation result and any separately requested account check; silence alone is insufficient.

Check `ldappasswd -VV`. Define `ldap_uri`, `bind_dn` and `user_dn` from the intended directory. For simple bind over required StartTLS:

~~~bash
ldappasswd -x -ZZ -H "$ldap_uri" -D "$bind_dn" -W -S "$user_dn"
status=$?
~~~

`-W` prompts for the bind password; `-S` prompts for the new target password. `-A` separately prompts for an old target password when required. Preserve exact submitted bytes without putting them in a transcript. Trusted LDAPS uses `ldaps://` without `-ZZ`.

This invokes the LDAPv3 Password Modify extended operation, not a generic OS password command or arbitrary attribute update. Server support, ACLs and password policy govern acceptance. Retain status/diagnostics; unsupported operation differs from invalid credentials or policy rejection. Omitting the target changes the associated identity; omitting a new password without prompting asks the server to generate one. Do not make either omission accidentally. `-n` does not change a password.

Source: [OpenLDAP ldappasswd](https://manpages.debian.org/bookworm/ldap-utils/ldappasswd.1.en.html).
