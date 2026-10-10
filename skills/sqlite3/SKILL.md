---
name: sqlite3
description: Inspect existing SQLite files with the sqlite3 CLI, bounded queries and structured output. Use when a missing path creates an empty database, WAL sidecars affect results, or display separators obscure data; export selected Grafana verifier rows with their actual parameters.
---

# Inspect an existing database copy

Read this entire SKILL.md before acting; reuse complete current context. Work from a coherent database copy, inspect the actual schema and retain query status with selected records. For selected historical Grafana verifier rows, read [Grafana records](references/grafana-records.md) before export/parameter interpretation. For a Rails-like user table with password_digest and role fields, read [selected authentication rows](references/auth-records.md) before exporting or mapping identities. For Firefox history or extension storage, read [browser databases](references/firefox-storage.md) before interpreting those tables. Finish with the requested rows and their supported meaning; missing tables, sidecars or decoding remain explicit limitations.

Define `database` as an existing absolute working-copy path. Opening a misspelled filename normally creates a new empty database; use read-only mode for inspection:

~~~bash
sqlite3 --version
sqlite3 -init /dev/null -readonly -batch -bail -header -column "$database" "SELECT name, type FROM sqlite_schema WHERE type IN ('table','view') ORDER BY name LIMIT 50;"
~~~

`-init /dev/null` avoids executing a user's startup file. `-bail` stops on the first error, and `-readonly` prevents creating/writing the primary database. These options do not make arbitrary supplied SQL or CLI dot-commands safe: `.shell`, `.load` and extension functions can execute code. Read a dump/script before considering execution.

Inspect the selected table's schema before requesting data. In the interactive CLI, `.schema table_name` is a dot-command on its own line; SQL instead terminates with a semicolon. Use actual SQL-quoted identifiers, choose relevant columns and add a meaningful `WHERE`/`LIMIT`. An empty result, an absent table and a denied/failed query are different findings.

For export, define `query` as one reviewed, bounded SELECT with the actual schema:

~~~bash
sqlite3 -init /dev/null -readonly -batch -bail -header -csv "$database" "$query"
~~~

Parse it as CSV, not by splitting on commas or newlines. The default pipe-separated display can be ambiguous when values contain separators. JSON output is another option where the installed version supports it. Treat password-looking values according to the application's format, not column names or string length alone.

With WAL-mode databases, committed rows may still reside in `database-wal`. Preserve a consistent database/WAL set and any captured `-shm`; do not discard sidecars to clear an error. Modern SQLite can read WAL databases under documented sidecar/directory conditions, but read-only database access can still require sidecar handling. Use working copies. For a live acquisition, use SQLite's backup API or an application-coordinated snapshot instead of independently copying changing files. `immutable=1` is a promise that files cannot change, not a universal lock-error workaround.


## Keep an encoded field attached to its record

Before exporting a suspected encrypted value, inspect its storage type and retain the account/domain plus a stable row identifier. For the **illustrative schema** `LDAP(Id, Uname, Domain, Pwd)`, after confirming those columns exist:

~~~bash
sqlite3 -init /dev/null -readonly -batch -bail -header -column "$database" 'SELECT Id, Uname, Domain, typeof(Pwd) AS storage_type, length(CAST(Pwd AS BLOB)) AS stored_bytes FROM LDAP ORDER BY Id LIMIT 20;'
~~~

These are stored bytes, not decoded ciphertext length. `NULL`, empty text and a BLOB are different states; none identifies a cipher. Export the required field for the selected identifier using the reviewed CSV query above, then trace the consuming application's decoding/decryption path. Unreadable decoded bytes are insufficient evidence of encryption.

An application doing `SELECT *` followed by a single reader `Read()` consumes one row, not every account. Without `ORDER BY`, SQLite does not guarantee which row appears first. If multiple rows exist, preserve that ambiguity instead of silently treating your sorted first row as the application's selected identity; an empty result needs separate handling too.
