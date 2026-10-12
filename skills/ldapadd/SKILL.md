---
name: ldapadd
description: Add reviewed LDIF entries to an administered LDAP directory with OpenLDAP ldapadd. Use when parent/schema requirements or partial batches affect an intended entry creation.
---

# Add the selected entries

Read this entire SKILL.md before acting. Require the administered endpoint, permitted bind identity, exact new DNs and reviewed LDIF/schema. No conditional resources are required. Finish with per-entry outcomes and read-back; a preview is not a server change.

Check `ldapadd -VV`. Define `ldap_uri` as the selected LDAP URI, `bind_dn` as the known administrator DN and `ldif` as the reviewed local file. For simple bind over required StartTLS:

~~~bash
ldapadd -n -v -x -ZZ -H "$ldap_uri" -D "$bind_dn" -W -f "$ldif"
ldapadd -x -ZZ -H "$ldap_uri" -D "$bind_dn" -W -f "$ldif"
status=$?
~~~

Review the preview before applying. `-n` suppresses modifications; it does not establish server acceptance. Use trusted LDAPS without `-ZZ` when that is the selected transport. `-W` prompts instead of exposing the bind password in arguments.

LDIF needs a DN, schema-required object classes/attributes and blank lines between entries. Add an absent parent before its children. Entries can succeed before a later error; default stopping does not roll back the batch. Reconcile exact successful DNs before retrying. Already-exists, schema and access errors require different fixes. Read back the intended attributes using the same directory context.

Sources: [ldapadd](https://manpages.debian.org/bookworm/ldap-utils/ldapadd.1.en.html), [OpenLDAP entry creation](https://www.openldap.org/doc/admin25/dbtools.html).
