# Mattermost connection context and selected account records

Use for authorized inspection of a Mattermost MySQL/MariaDB database whose configuration and selected user records are available. Read the configuration as JSON, not a password-looking line from a grep result. Locate the actual active config from this deployment; a familiar installation path is only a lead. Environment/config-store overrides or a stale copied file can make its contents differ from the running service.

`SqlSettings.DriverName` determines the database driver. For mysql, `SqlSettings.DataSource` uses the Go MySQL driver's DSN, carrying user/password, protocol/address, database and query parameters. Decode JSON escapes such as `\u0026` into their literal value before interpreting the DSN; do not copy PDF wrapping into a credential or split every colon in a password. `AtRestEncryptKey` is a separate application configuration value, not the SQL login password or a user-password salt. Keep the acquired configuration private.

Extract the intended endpoint/account/database with a DSN-aware method or careful review of the actual format. For `tcp(host:port)`, define `db_host`, `db_port`, `db_user` and `database` from that selected endpoint and connect explicitly:

~~~bash
mysql --protocol=TCP --host="$db_host" --port="$db_port" --user="$db_user" --password --database="$database"
~~~

Enter the known database password at the prompt; keep required TLS policy. A bare `mysql -u user -p` on Unix can choose a socket even when the application's DSN names TCP. A refused endpoint, denied login and missing database require different recovery. A PostgreSQL driver needs its corresponding client/query dialect, not a forced mysql invocation.

At the SQL prompt, establish context and inspect the actual table/columns before requesting selected records:

~~~sql
SELECT USER(), CURRENT_USER(), DATABASE(), VERSION();
SHOW TABLES;
SHOW COLUMNS FROM `Users`;
~~~

When the observed schema has these columns, a bounded **illustrative** account lookup is:

~~~sql
SELECT Id, Username, Password, AuthService, AuthData
FROM `Users`
WHERE Username = 'reviewed-account'
ORDER BY Id
LIMIT 2;
~~~

Replace that literal with the selected account using proper SQL quoting/parameter handling. Do not acquire all users with `SELECT *` to answer a one-account question. Two results require resolving identity/collation ambiguity; no rows can mean a different database or account rather than an empty Users table. Preserve the selected row's unique ID and authentication-service mapping with the password value.

For a known unique ID and confirmed schema, define `query` as a reviewed one-row `SELECT Password FROM Users WHERE Id = ... LIMIT 1` and `record_file` as a fresh private output:

~~~bash
umask 077
mysql --protocol=TCP --host="$db_host" --port="$db_port" --user="$db_user" --password --database="$database" \
  --batch --skip-column-names --execute="$query" > "$record_file"
status=$?
~~~

Require success and the expected one complete record. Batch output escapes certain bytes; bcrypt's ordinary alphabet needs no unescaping, but do not apply that assumption to arbitrary future formats. Keep the account/ID mapping separately; export headers, wrapping, quotes or a username prefix are not part of a standalone bcrypt record.

Historical Mattermost used bcrypt: the v5.30.0 model calls its generator with cost 10. A complete `$2a$10$...` value carries its prefix, cost, salt and checksum; preserve the whole record for a compatible checker. Determine the format from the acquired value and producing version. Current vendor documentation describes progressive PBKDF2 migration from v11.0, so an upgraded database can contain records from different states. Do not select bcrypt merely because the table belongs to Mattermost.

`AuthService`/`AuthData` can indicate external authentication rather than a local password; a blank password is not a recoverable empty-password assertion. Email verification proves that account's verification state, not employment. An application username root or a system-admin role is separate from the SQL login and OS UID 0. Recovery against the selected application verifier proves a candidate for that verifier; an authorized OS/session check is separate evidence of reuse.

Finish with the actual endpoint/version/query, selected account/format and any missing or ambiguous record. No database modification or password reset is needed for inspection/export. See [Mattermost configuration](https://docs.mattermost.com/administration-guide/configure/environment-configuration-settings), the [Go driver DSN](https://github.com/go-sql-driver/mysql#dsn-data-source-name), [historical user model](https://github.com/mattermost/mattermost/blob/v5.30.0/model/user.go) and [current authentication settings](https://docs.mattermost.com/administration-guide/configure/authentication-configuration-settings).
