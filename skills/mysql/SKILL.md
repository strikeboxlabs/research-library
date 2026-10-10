---
name: mysql
description: Connect with the Linux mysql client and inspect selected database metadata. Use for Unix-socket versus TCP confusion, account/host mismatches, string truncation or trailing-space surprises and understanding client shell commands and which machine LOAD DATA LOCAL reads.
---

# MySQL connection and inspection

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

When an interactive database shell is inconvenient, define `database` as the observed database name and `query` as one reviewed, bounded SELECT using its actual schema:

~~~bash
mysql --protocol=TCP --host="$db_host" --port="$db_port" --user="$db_user" --password --database="$database" --batch --execute="$query"
~~~

This still prompts for the password. Batch output is tab-separated with special characters escaped by default; it is not CSV. Check the exit status before interpreting an empty result. `--execute`/`--batch` change execution/output style, not SQL privileges or side effects. A supplied query file can still write data; avoid `SELECT *` when selected columns answer the question.

## Investigate string truncation and comparison

At the SQL prompt, replace `observed_table` with the selected real table:

~~~sql
SELECT VERSION(), @@SESSION.sql_mode;
SHOW FULL COLUMNS FROM `observed_table`;
SHOW CREATE TABLE `observed_table`;
~~~

Read the type, character limit, collation and actual unique constraints. Frontend length checks and a shortened display do not establish the database schema. The CLI session's SQL mode may differ from the application's connection.

- `VARCHAR` retains trailing spaces within its limit; `CHAR` normally strips them on retrieval. Retrieval and equality comparison are separate questions.
- For nonbinary strings, `PAD SPACE` collations ignore trailing spaces in equality comparisons; `NO PAD` collations preserve their significance. On MySQL versions providing it, inspect the actual collation's `INFORMATION_SCHEMA.COLLATIONS.PAD_ATTRIBUTE`. Do not infer this solely from a case-insensitive suffix or the connection default.
- Overlength nonspace input can be truncated with warnings in non-strict mode; strict mode normally rejects it, while `IGNORE` can downgrade errors. Excess trailing spaces have separate rules: `VARCHAR` truncates them with a warning, `CHAR` silently, regardless of strict mode.

For a statement already executed in your session, run `SHOW WARNINGS` immediately, before another nondiagnostic statement replaces its diagnostics. It cannot retrieve warnings from an earlier web request's session. Establish the schema, application query and connection settings before attributing an identity collision to truncation; avoid inserting probe accounts or relaxing SQL mode just to explain an observation.

Consult the server version's [string-type rules](https://dev.mysql.com/doc/refman/8.4/en/char.html), [SQL modes](https://dev.mysql.com/doc/refman/8.4/en/sql-mode.html) and [warning scope](https://dev.mysql.com/doc/refman/8.4/en/show-warnings.html) for exceptions. MariaDB and older MySQL releases require their own matching documentation.

## Distinguish server and client file access

`LOAD DATA INFILE` reads on the database server. `LOAD DATA LOCAL INFILE` reads through the client process; for Adminer, that client is the web application host. It also loads data into a table. Enabling local-infile changes file-access exposure and is not required for normal SELECT queries or an authentication repair.

`LOAD_FILE()` instead returns a server-side file as a value. It needs FILE privilege, a readable absolute server path, applicable `secure_file_priv` permission and size below `max_allowed_packet`; NULL can mean any unmet condition. Successful reading does not establish write access to that directory. `SELECT ... INTO OUTFILE` creates a server-side file and refuses an existing path; it is a write operation despite beginning with SELECT. An application's HTTP 500 after a database write does not prove rollback: inspect state before retrying.

## Recognize commands processed by the client

When reviewing a wrapper or query file, separate the operating-system shell, mysql's input parser and the database server. The client's `system` / `\!` command invokes a shell on the **client host**, using that client's OS identity. It does not require the server's FILE privilege and does not by itself establish execution on a remote database host.

`-s` (silent) and `-N` (omit column names) adjust output; they do not disable client commands. Shell quoting preserves an argument boundary but does not turn supplied text into safe SQL or disable mysql's parser. Data read from a file or shared-memory segment remains input even when the wrapper's username argument was filtered.

For an existing integration, inspect its actual client version and input mode. MySQL's noninteractive `--binary-mode` disables client commands except `charset` and `delimiter`; it also changes byte handling. MySQL 8.4.3+ offers `--system-command=OFF`; 8.4.6+ adds the broader `--commands=OFF`, with documented exceptions and interactions. Do not assume these options exist in MariaDB or older clients. None makes arbitrary SQL harmless or limits server privileges. Use [client-command documentation](https://dev.mysql.com/doc/refman/8.4/en/mysql-commands.html) and the matching [option reference](https://dev.mysql.com/doc/refman/8.4/en/mysql-command-options.html) before changing a wrapper.
