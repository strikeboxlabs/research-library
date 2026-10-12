# Distinguish server and client file access

`LOAD DATA INFILE` reads on the database server. `LOAD DATA LOCAL INFILE` reads through the client process; for Adminer, that client is the web application host. It also loads data into a table. Enabling local-infile changes file-access exposure and is not required for normal SELECT queries or an authentication repair.

`LOAD_FILE()` instead returns a server-side file as a value. It needs FILE privilege, a readable absolute server path, applicable `secure_file_priv` permission and size below `max_allowed_packet`; NULL can mean any unmet condition. Successful reading does not establish write access to that directory. `SELECT ... INTO OUTFILE` creates a server-side file and refuses an existing path; it is a write operation despite beginning with SELECT. An application's HTTP 500 after a database write does not prove rollback: inspect state before retrying.

For an authorised export diagnosis, inspect the existing direct SQL session before attempting a write:

~~~sql
SELECT CURRENT_USER(), VERSION();
SHOW GRANTS FOR CURRENT_USER();
SHOW VARIABLES LIKE 'secure_file_priv';
~~~

Grants for another account named in `mysql.user` do not establish this session's privileges. Resolve applicable roles with the server's matching rules when necessary. FILE privilege is only one condition: the server OS account must be able to create the destination, `secure_file_priv` must permit it and the path must not already exist. In MySQL, NULL disables these file operations while an empty value removes that variable's path restriction; apply the actual vendor/version rules rather than treating empty as a general denial.

`INTO OUTFILE` serializes rows with field/line delimiters and escaping. It is not a general byte-preserving file-upload command. A SQL driver's error after a no-result write does not establish that the file was never created; inspect the exact destination through an existing authorised channel before a retry. Report file creation separately from any later application interpretation/execution.

Sources: [current-account grants](https://dev.mysql.com/doc/refman/8.4/en/show-grants.html), [MariaDB OUTFILE requirements](https://mariadb.com/docs/server/reference/sql-statements/data-manipulation/selecting-data/select-into-outfile), [MySQL secure_file_priv](https://dev.mysql.com/doc/refman/8.4/en/server-system-variables.html#sysvar_secure_file_priv).

## Recognize commands processed by the client

When reviewing a wrapper or query file, separate the operating-system shell, mysql's input parser and the database server. The client's `system` / `\!` command invokes a shell on the **client host**, using that client's OS identity. It does not require the server's FILE privilege and does not by itself establish execution on a remote database host.

`-s` (silent) and `-N` (omit column names) adjust output; they do not disable client commands. Shell quoting preserves an argument boundary but does not turn supplied text into safe SQL or disable mysql's parser. Data read from a file or shared-memory segment remains input even when the wrapper's username argument was filtered.

For an existing integration, inspect its actual client version and input mode. MySQL's noninteractive `--binary-mode` disables client commands except `charset` and `delimiter`; it also changes byte handling. MySQL 8.4.3+ offers `--system-command=OFF`; 8.4.6+ adds the broader `--commands=OFF`, with documented exceptions and interactions. Do not assume these options exist in MariaDB or older clients. None makes arbitrary SQL harmless or limits server privileges. Use [client-command documentation](https://dev.mysql.com/doc/refman/8.4/en/mysql-commands.html) and the matching [option reference](https://dev.mysql.com/doc/refman/8.4/en/mysql-command-options.html) before changing a wrapper.

## Inspect acquired native provider settings

In an already authorized MariaDB metadata session, keep the actual server vendor/version and matched-account grants alongside selected global settings:

~~~sql
SELECT VERSION(), CURRENT_USER();
SHOW GRANTS FOR CURRENT_USER();
SHOW GLOBAL VARIABLES WHERE Variable_name IN ('wsrep_provider', 'wsrep_notify_cmd');
~~~

These queries inspect metadata without changing a provider or loading a library. Missing/denied rows leave that observation unresolved. A mysql-named client or compatibility banner does not make a MariaDB server Oracle MySQL; match package/build patches as well as the numeric version.

An acquired wsrep provider assignment is a server-native loading operation, distinct from mysql's local shell command and mysql.func registrations. Historical [MDEV-25179](https://jira.mariadb.org/browse/MDEV-25179) requires privileged database control and was fixed by making the variables read-only. A displayed path, account named root or version string alone does not prove that control, loaded bytes or server OS identity. Preserve the static finding and observed grants/settings; do not assign a replacement provider to test it. Finish with version/patch uncertainty and the supported execution-context distinction. See [SHOW VARIABLES scope](https://mariadb.com/docs/server/reference/sql-statements/administrative-sql-statements/show/show-variables).
