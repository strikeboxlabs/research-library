---
name: apache-directory-studio
description: Read selected LDAP directory objects through an installed Apache Directory Studio Linux GUI. Use to distinguish connection, bind, naming-context and object-attribute evidence without editing the directory.
---

# Read the selected directory object

Read this entire SKILL.md before acting. Require the owner's selected endpoint, account/authentication method, permitted object scope, trusted installed launcher and graphical session. No conditional resources are required. Finish with the selected DN/object identity, attributes relevant to the question, bind/search result and scope limits.

Define `studio_bin` as the existing installation's actual launcher:

~~~bash
"$studio_bin"
~~~

Open the LDAP perspective and create/select the intended connection. Set the verified host/port and required StartTLS or LDAPS transport, checking peer trust rather than accepting an unexpected certificate. Enable the connection's Read-Only option when offered by this version. Enter the prepared bind identity and use the password prompt without saving it unless retention is explicitly required. A network-parameter check establishes reachability separately from Check Authentication, which attempts the bind. Neither establishes permission to read every object.

Open the connection and inspect RootDSE naming contexts. For AD, retain `defaultNamingContext` when available; do not assume `CN=Users` contains every account. Navigate directly to the selected observed DN through Go to DN or the DIT tree, then read its Entry editor attributes. Retain objectClass and objectSID/sAMAccountName when needed to identify the object, not only its display name. Directory text such as `info` is an attribute value, not proof that it is a usable password.

Retain the selected DN and final search/error context. Client count/time limits, paging, referrals and attribute visibility constrain coverage; a displayed container count is not an all-domain user inventory. A missing object and a rejected bind require different next checks. Stop once the selected object's requested evidence is complete, close the connection and retain only redacted findings. Editing a value or importing LDIF writes directory state and is outside this read task.

Use the [connection wizard](https://nightlies.apache.org/directory/studio/2.0.0.v20210717-M17/userguide/ldap_browser/tools_newconnection_wizard.html) and [browser guide](https://nightlies.apache.org/directory/studio/2.0.0.v20210717-M17/userguide/ldap_browser/gettingstarted_browse.html) for the matching installed interface. The wizard's Save password setting stores credentials in configuration; distinguish that from entering a password for the current connection.
