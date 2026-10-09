---
name: sqlite3
description: Inspect existing SQLite files with the sqlite3 CLI, bounded queries and structured output. Use when a missing path creates an empty database, WAL sidecars affect results, or display separators obscure data.
---

# Inspect an existing database copy

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

Documentation reviewed 2026-10-09; Linux execution untested. Case: Artificial pp. 6, 8. Sources: [SQLite CLI](https://sqlite.org/cli.html), [WAL behavior](https://sqlite.org/wal.html), [backup API](https://sqlite.org/backup.html).
