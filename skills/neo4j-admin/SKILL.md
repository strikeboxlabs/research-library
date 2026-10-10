---
name: neo4j-admin
description: Set the initial native Neo4j database password before first startup and interpret setup-password commands found in shell history. Use when preparing a new Neo4j database or distinguishing database credentials from current Linux account credentials.
---

# Initial Neo4j database password

Read this entire SKILL.md before acting; reuse complete current context. Establish that this is a new database which has not started, the installed Neo4j version and the intended native database account. Finish with the admin command's outcome and the requested first-login/password-change result; a historical command is not evidence of current credentials.

`neo4j-admin dbms set-initial-password` initializes the native database user `neo4j`; it does not set the Linux user's password or rotate an already initialized database password. Check the installed command before using the Neo4j 5+ namespace:

~~~bash
neo4j-admin --version
neo4j-admin dbms set-initial-password --help
~~~

For an authorized first-time initialization before the database's first startup, read the chosen password without putting a literal secret into interactive shell history:

~~~bash
IFS= read -r -s -p 'Initial database password: ' initial_password
printf '\n'
neo4j-admin dbms set-initial-password "$initial_password"
admin_status=$?
unset initial_password
printf 'initial-password command status=%s\n' "$admin_status"
~~~

The value still reaches the process as an argument; shell prompt suppression is not protection from process inspection or tracing. Use the deployment's approved secret handling, and retain status/first-login evidence without copying the password into a report. `--require-password-change=true` can require a change at first login on supporting versions; plan that interaction when setting a temporary password.

If the database has already started, use its supported authenticated password-change or recovery procedure rather than rerunning initialization and claiming a reset. Select the documentation for the installed version: older releases use a different command layout. A zero admin-command exit is an initialization result, not evidence that a server is running or a later authentication succeeded.

A `set-initial-password` entry in `.bash_history` is evidence of a setup attempt for the database account. It can be stale, failed or followed by a password change. Resolve the OS service account's home from account metadata instead of guessing `/home/neo4j`; Linux and database usernames need not share credentials. Password reuse with another account is established only by a separately authorized authentication result, not by reading that history entry.

See [Neo4j initial-password semantics](https://neo4j.com/docs/operations-manual/current/configuration/set-initial-password/) for version, first-start and password-change conditions.
