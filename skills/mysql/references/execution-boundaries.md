# Distinguish server and client file access

`LOAD DATA INFILE` reads on the database server. `LOAD DATA LOCAL INFILE` reads through the client process; for Adminer, that client is the web application host. It also loads data into a table. Enabling local-infile changes file-access exposure and is not required for normal SELECT queries or an authentication repair.

`LOAD_FILE()` instead returns a server-side file as a value. It needs FILE privilege, a readable absolute server path, applicable `secure_file_priv` permission and size below `max_allowed_packet`; NULL can mean any unmet condition. Successful reading does not establish write access to that directory. `SELECT ... INTO OUTFILE` creates a server-side file and refuses an existing path; it is a write operation despite beginning with SELECT. An application's HTTP 500 after a database write does not prove rollback: inspect state before retrying.

## Recognize commands processed by the client

When reviewing a wrapper or query file, separate the operating-system shell, mysql's input parser and the database server. The client's `system` / `\!` command invokes a shell on the **client host**, using that client's OS identity. It does not require the server's FILE privilege and does not by itself establish execution on a remote database host.

`-s` (silent) and `-N` (omit column names) adjust output; they do not disable client commands. Shell quoting preserves an argument boundary but does not turn supplied text into safe SQL or disable mysql's parser. Data read from a file or shared-memory segment remains input even when the wrapper's username argument was filtered.

For an existing integration, inspect its actual client version and input mode. MySQL's noninteractive `--binary-mode` disables client commands except `charset` and `delimiter`; it also changes byte handling. MySQL 8.4.3+ offers `--system-command=OFF`; 8.4.6+ adds the broader `--commands=OFF`, with documented exceptions and interactions. Do not assume these options exist in MariaDB or older clients. None makes arbitrary SQL harmless or limits server privileges. Use [client-command documentation](https://dev.mysql.com/doc/refman/8.4/en/mysql-commands.html) and the matching [option reference](https://dev.mysql.com/doc/refman/8.4/en/mysql-command-options.html) before changing a wrapper.
