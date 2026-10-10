---
name: mysql
description: Use mysql for explicit socket/TCP connections, database metadata and selected Mattermost account records. Diagnose account matching, password-format context, native functions, string comparison and client/server execution boundaries.
---

# MySQL connection and inspection

Read this entire SKILL.md before acting; complete current context need not be re-read. Establish the client/server and connection identity for a database task; native loadable-function metadata is covered below. Read the selected reference fully before its procedure; leave unrelated branches unloaded. Finish with the actual query/result and its scope; a denied query, empty result or client-side effect is not interchangeable with a server finding.

- Mattermost config/DSN and selected user-password records: [account record context](references/mattermost-records.md).
- Truncation, padding or collation surprises: [string comparison](references/string-comparison.md).
- Server/client file access or wrapper/query-file execution: [execution boundaries](references/execution-boundaries.md).

Check `mysql --version` and local help. The command can come from MySQL or a MariaDB compatibility package; TLS/authentication options are not identical across releases/vendors. The client version does not establish the server version.

Define `db_host`, `db_port` and `db_user` for the intended endpoint and known account. For TCP, including an SSH-forwarded local port:

~~~bash
mysql --protocol=TCP --host="$db_host" --port="$db_port" --user="$db_user" --password
~~~

Enter the password at the prompt. On Unix, `localhost` normally selects a Unix socket and can make `-P` irrelevant; explicit `--protocol=TCP` prevents that ambiguity. For an intended socket connection, instead specify its actual `--socket` path and socket protocol. Keep the service's required TLS policy; do not treat disabling TLS as a routine login fix.

Quoting `-p"$password"` keeps one shell argument; it still puts the expanded secret in the process arguments. Some clients erase that argument after startup, leaving an exposure window. For an unattended job, use its already configured, protected credential mechanism rather than replacing the prompt with a command-line secret. See MySQL's [password handling guidance](https://dev.mysql.com/doc/refman/8.4/en/password-security-user.html).

At the **SQL prompt**, establish context before reading application data:

~~~sql
SELECT USER(), CURRENT_USER(), DATABASE(), VERSION();
SHOW DATABASES;
~~~

`USER()` describes the connecting identity; direct `CURRENT_USER()` identifies the account matched for authentication. Its host component matters. Across a tunnel, the server sees the connection from the SSH endpoint, which can match a different account rule. `DATABASE()` can be NULL until one is selected. Database visibility is privilege-dependent.

Select an observed database with `USE`, inspect `SHOW TABLES` and `SHOW COLUMNS FROM` the chosen table, then request only relevant columns with a bounded `SELECT ... LIMIT`. Use actual identifiers with SQL quoting; shell variable syntax does not interpolate at this prompt. An empty table and a denied query are different outcomes. Avoid importing a supplied SQL dump merely to inspect it: scripts can contain writes.

For repeatable bounded results, use `ORDER BY` with a unique tie-breaker from the actual schema. Without ordering, row position is not insertion order or a reliable way to pair rows with another process's random-number calls. Preserve the SELECT column order when interpreting native `row[n]` indexing. An empty later query does not identify a cleanup process; confirm the database/session and observed writes separately. See [ordering and LIMIT](https://dev.mysql.com/doc/refman/8.4/en/limit-optimization.html).

Prefer separate rows over a `GROUP_CONCAT` string when identity or completeness matters. Its `group_concat_max_len` bounds returned bytes, NULL expressions can omit tuples, and an outer `LIMIT` limits result rows rather than entries within the aggregate. Inspect `@@SESSION.group_concat_max_len` and immediate `SHOW WARNINGS` when diagnosing truncation. For account metadata, preserve both user and host; repeated usernames can identify different accounts. Inspect the actual schema/plugin before assuming a legacy `password` column exists. See [MariaDB aggregate semantics](https://mariadb.com/docs/server/reference/sql-functions/aggregate-functions/group_concat).

When an interactive database shell is inconvenient, define `database` as the observed database name and `query` as one reviewed, bounded SELECT using its actual schema:

~~~bash
mysql --protocol=TCP --host="$db_host" --port="$db_port" --user="$db_user" --password --database="$database" --batch --execute="$query"
~~~

This still prompts for the password. Batch output is tab-separated with special characters escaped by default; it is not CSV. Check the exit status before interpreting an empty result. `--execute`/`--batch` change execution/output style, not SQL privileges or side effects. A supplied query file can still write data; avoid `SELECT *` when selected columns answer the question.

## Inspect native loadable-function metadata

In the established SQL session, inspect registrations without calling the functions:

~~~sql
SELECT name, dl FROM mysql.func ORDER BY name LIMIT 100;
SHOW VARIABLES LIKE 'plugin_dir';
~~~

`name` is the registered function; `dl` names its shared library under the server's plugin directory. These are native loadable functions, distinct from SQL stored functions. The table is not a complete inventory of component/plugin-provided functions; interpret it using the actual server vendor/version. A denied query is not an empty registry, and 100 rows may mean a capped result.

A registration or unusual filename is a lead, not proof of a malicious library or that it is currently loaded. Compare an acquired library with a trusted matching package and inspect its exports/code. Do not invoke an unknown function to test it: a `SELECT` can execute native code with server-process OS effects. A database account named root does not imply the server runs as OS root. See [MySQL loading rules](https://dev.mysql.com/doc/refman/8.4/en/function-loading.html) and [MariaDB's table definition](https://mariadb.com/docs/server/reference/system-tables/the-mysql-database-tables/mysql-func-table).
