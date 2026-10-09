---
name: mysql
description: Connect with the Linux mysql client and inspect selected database metadata. Use for Unix-socket versus TCP confusion, account/host mismatches and understanding which machine LOAD DATA LOCAL reads.
---

# MySQL connection and inspection

Check `mysql --version` and local help. The command can come from MySQL or a MariaDB compatibility package; TLS/authentication options are not identical across releases/vendors. The client version does not establish the server version.

Define `db_host`, `db_port` and `db_user` for the intended endpoint and known account. For TCP, including an SSH-forwarded local port:

~~~bash
mysql --protocol=TCP --host="$db_host" --port="$db_port" --user="$db_user" --password
~~~

Enter the password at the prompt. On Unix, `localhost` normally selects a Unix socket and can make `-P` irrelevant; explicit `--protocol=TCP` prevents that ambiguity. For an intended socket connection, instead specify its actual `--socket` path and socket protocol. Keep the service's required TLS policy; do not treat disabling TLS as a routine login fix.

At the **SQL prompt**, establish context before reading application data:

~~~sql
SELECT USER(), CURRENT_USER(), DATABASE(), VERSION();
SHOW DATABASES;
~~~

`USER()` describes the connecting identity; direct `CURRENT_USER()` identifies the account matched for authentication. Its host component matters. Across a tunnel, the server sees the connection from the SSH endpoint, which can match a different account rule. `DATABASE()` can be NULL until one is selected. Database visibility is privilege-dependent.

Select an observed database with `USE`, inspect `SHOW TABLES` and `SHOW COLUMNS FROM` the chosen table, then request only relevant columns with a bounded `SELECT ... LIMIT`. Use actual identifiers with SQL quoting; shell variable syntax does not interpolate at this prompt. An empty table and a denied query are different outcomes. Avoid importing a supplied SQL dump merely to inspect it: scripts can contain writes.

`LOAD DATA INFILE` reads on the database server. `LOAD DATA LOCAL INFILE` reads through the client process; for Adminer, that client is the web application host. It also loads data into a table. Enabling local-infile changes file-access exposure and is not required for normal SELECT queries or an authentication repair.

`LOAD_FILE()` instead returns a server-side file as a value. It needs FILE privilege, a readable absolute server path, applicable `secure_file_priv` permission and size below `max_allowed_packet`; NULL can mean any unmet condition. Successful reading does not establish write access to that directory. `SELECT ... INTO OUTFILE` creates a server-side file and refuses an existing path; it is a write operation despite beginning with SELECT. An application's HTTP 500 after a database write does not prove rollback: inspect state before retrying.

Documentation reviewed 2026-10-09; Linux execution untested. Cases: Admirer pp. 11–16; Agile pp. 13–14; Altered pp. 11–17. Sources: [connections](https://dev.mysql.com/doc/refman/8.4/en/connecting.html), [identity functions](https://dev.mysql.com/doc/refman/8.4/en/information-functions.html), [metadata](https://dev.mysql.com/doc/refman/8.4/en/getting-information.html), [LOCAL file access](https://dev.mysql.com/doc/refman/8.4/en/load-data-local-security.html), [LOAD_FILE](https://dev.mysql.com/doc/refman/8.4/en/string-functions.html#function_load-file), [OUTFILE](https://dev.mysql.com/doc/refman/8.4/en/select-into.html).
