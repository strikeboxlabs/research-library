---
name: sqlcmd
description: Connect to a selected SQL Server with known credentials and inspect roles or database/table metadata. Use when SQL versus integrated authentication, interactive batch submission or metadata visibility obscures the result.
---

# Verify the selected SQL connection and role

Read this entire SKILL.md before acting. Require the selected server, known authentication context and installed sqlcmd variant; no conditional files are required. Select the role query or metadata inventory below. Finish with connection/query status and observed values/coverage, or the specific failure.

Use `sqlcmd '-?'` to identify supported options. Microsoft supplies ODBC and Go implementations; TLS switches/defaults differ by version. Resolve certificate/name/trust failures against that client's documentation. Define `server` as the selected TCP endpoint and `login` as the known SQL login:

~~~bash
sqlcmd -X -S "$server" -U "$login" -l 15 -t 15 -b \
  -Q "SELECT IS_SRVROLEMEMBER('sysadmin') AS is_sysadmin;"
status=$?
~~~

Omit `-P` so the client prompts. `-X` disables startup commands and environment-derived settings; pass the intended connection explicitly. `-l` bounds login and `-t` query execution. `-Q` exits after the query; `-b` makes SQL errors above severity 10 fail.

Separate shell argument parsing from SQL parsing. An `Unexpected argument` diagnostic can mean the shell split the intended `-Q` string before any query ran. Single quotes group arguments in Bash/PowerShell but not Windows cmd.exe; switching shells changes parsing, not SQL permissions. Inspect the actual received query and keep SQL string literals single-quoted: with `QUOTED_IDENTIFIER ON`, double quotes delimit identifiers. Do not change the session setting merely to imitate an old transcript. See [quoted identifier semantics](https://learn.microsoft.com/en-us/sql/t-sql/statements/set-quoted-identifier-transact-sql).

An untrusted-domain integrated-authentication error is a failed connection, not password validation. SQL authentication is distinct from `-E` integrated authentication and requires an enabled SQL login.

For the ODBC Linux client with an existing authorized Kerberos context, replace `-U "$login"` with `-E` and select the intended cache in that process. This requires actual driver/Kerberos support, realm/time and the SQL service's FQDN/SPN; Windows integrated-authentication transcripts do not establish Linux readiness. Inspect the returned SQL identity separately from the cache filename. See [ODBC integrated authentication](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/using-integrated-authentication).

For this query, `1` means membership, `0` means nonmembership and `NULL` means unresolved/invalid input or insufficient visibility. Membership is not a complete permissions inventory or the SQL service's OS identity. Retain diagnostics separately from the returned value.

## Inspect visible databases and one selected catalogue

For a bounded database-name inventory, use the same reviewed authentication/connection with `-Q "SELECT TOP (200) name, state_desc FROM sys.databases ORDER BY name;"`. Define `database` as the requested returned database name, then select it without interpolating it into SQL:

~~~bash
sqlcmd -X -S "$server" -U "$login" -d "$database" -l 15 -t 15 -b \
  -Q "SELECT TOP (200) TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE FROM INFORMATION_SCHEMA.TABLES ORDER BY TABLE_SCHEMA, TABLE_NAME;"
status=$?
~~~

Retain schema and type: a name-only list loses identity and includes views. These are permission-filtered metadata, not proof of access to table contents; 200 rows can be the chosen bound. For feature-complete schema detail use the relevant sys catalogue views rather than assuming INFORMATION_SCHEMA contains everything. Do not follow this inventory with an unrestricted SELECT * from a credential/data table.

In interactive sqlcmd, statements are buffered until `GO` on its own line; a semicolon alone does not submit the batch. `GO` is a client command, not server T-SQL. -Q submits its specified query directly and exits; do not add GO to the query string. A prompt or buffer line count is not query execution. Finish with actual rows and errors, then exit the selected session.

References for inventory/batching: [sys.databases visibility](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-databases-transact-sql), [TABLES scope](https://learn.microsoft.com/en-us/sql/relational-databases/system-information-schema-views/tables-transact-sql) and [interactive submission](https://learn.microsoft.com/en-us/sql/tools/sqlcmd/sqlcmd-use-utility).

References: [sqlcmd options](https://learn.microsoft.com/en-us/sql/tools/sqlcmd/sqlcmd-utility?view=sql-server-ver17), [IS_SRVROLEMEMBER interpretation](https://learn.microsoft.com/en-us/sql/t-sql/functions/is-srvrolemember-transact-sql?view=sql-server-ver17).
