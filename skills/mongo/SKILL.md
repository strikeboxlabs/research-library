---
name: mongo
description: Identify the selected database and its collection names with the legacy MongoDB mongo shell. Use when an existing older deployment has mongo rather than mongosh and shell/server versions or database context are ambiguous.
---

# Inspect legacy MongoDB collection metadata

Read this entire SKILL.md before acting. Establish the installed shell, inspected startup environment, known endpoint, database and configured authentication/TLS. Finish with the selected database and collection names or the concrete access/connection gap, then close the session. This narrow task does not retrieve document contents.

Check `mongo --version` and local help; this is the legacy shell, whose options should not be assumed for `mongosh`. Define `uri` as the known connection string with the intended database and configured transport, omitting passwords. For an endpoint configured without authentication:

~~~bash
mongo --norc "$uri"
~~~

For configured password authentication, define the known `username` and `auth_database` and use a final argumentless password option:

~~~bash
mongo --norc "$uri" --username "$username" --authenticationDatabase "$auth_database" --password
~~~

`--norc` skips startup evaluation of `~/.mongorc.js`. Legacy documentation distinguishes a global `/etc/mongorc.js`, which this option does not suppress; inspect the installed implementation and global startup file rather than assuming all startup code is disabled. The shell itself executes JavaScript; do not load unknown scripts to inspect metadata. Preserve connection diagnostics and distinguish client version from the server version shown at connection. A denied startup/history-file access is separate from a server connection failure: later successful metadata responses can coexist with that local error. An access-control warning describes the reported server configuration, not OS privileges or the authorization to retrieve every document.

At the **mongo prompt**, inspect the current database and its collections:

~~~text
db
show collections
~~~

An empty list, authorization error and wrong database are different outcomes. A collection name does not establish row count, schema or document access. Use the configured database rather than inferring it from an application's directory name. Exit the shell when the requested evidence is collected.

See MongoDB's [legacy CLI options](https://github.com/mongodb/docs/blob/v4.4/source/reference/program/mongo.txt) and [shell helpers](https://github.com/mongodb/docs/blob/v4.4/source/reference/mongo-shell.txt).
