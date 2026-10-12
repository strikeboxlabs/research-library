---
name: ldapmodify
description: Replace one authorized LDAP contact attribute with OpenLDAP ldapmodify. Use when LDIF syntax, SASL identity, transport, replace semantics or read-back evidence determines whether the intended change occurred.
---

# Change one selected contact field

Read this entire SKILL.md before acting; reuse complete current context. Require the exact owned entry DN, authorization for its contact-field change, a preserved prior value, a reviewed one-entry LDIF file and the known bind/transport context. Preview the input, apply only the intended change and read it back with the same identity; missing bind, permission or post-change evidence remains unresolved.

Check `ldapmodify -VV` and installed options. It defaults to SASL, not anonymous or simple bind; explicitly select the intended mechanism. For Kerberos, require a usable selected cache and the client's GSSAPI mechanism, correct service FQDN/SPN and established TLS trust. Define `uri` as that `ldap://` endpoint and `entry_dn` as the exact observed DN. Capture the existing mobile value first:

~~~bash
ldapsearch -LLL -Y GSSAPI -ZZ -H "$uri" -b "$entry_dn" -s base '(objectClass=*)' mobile
~~~

Require successful search status and one intended entry; retain absent versus present values. Create `changes` as a private LDIF file. This is an **illustrative input**; replace the DN and number with the selected approved values:

~~~ldif
dn: CN=Contact,OU=Lab,DC=example,DC=invalid
changetype: modify
replace: mobile
mobile: +45 5555 0100
-
~~~

`replace` replaces the attribute's complete value set. A replacement with no values removes the attribute, so an accidentally empty field is consequential. Use proper LDIF encoding for arbitrary values; shell echo escapes and filter/DN escaping are different formats. Review the complete file for extra entries/operations and file-URL values before passing it to the tool.

Preview and inspect status/diagnostics:

~~~bash
ldapmodify -n -v -f "$changes"
~~~

`-n` suppresses modification; it does not establish online permissions or successful application. Once the selected change is authorized and the preview is correct:

~~~bash
ldapmodify -Y GSSAPI -ZZ -H "$uri" -f "$changes"
status=$?
~~~

`-ZZ` requires StartTLS success; resolve trust/transport errors before sending the change. For a provisioned simple-bind workflow, `-x -D "$bind_dn" -W` selects that identity and prompts for its password under the same required protected transport. Do not treat Linux UID0 as directory authorization.

Require zero status and repeat the selected base search to compare actual values. A “modifying entry” line alone is not a retained final result. Avoid `-c`, which continues after errors, for this one-entry task. If another writer changed the entry, preserve that observation and re-evaluate the requested value rather than overwriting it automatically. A later application's report is separate consumer evidence, not a substitute for LDAP read-back. See the [OpenLDAP ldapmodify manual](https://manpages.debian.org/bookworm/ldap-utils/ldapmodify.1.en.html) and [LDIF format](https://www.rfc-editor.org/rfc/rfc2849).
