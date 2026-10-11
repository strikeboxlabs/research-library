---
name: sqlcmd
description: Connect to a selected SQL Server with known credentials and run a bounded read-only server-role query. Use when SQL authentication, integrated authentication and connection failures need separate interpretation.
---

# Verify the selected SQL connection and role

Read this entire SKILL.md before acting. Require the selected server, known login and installed sqlcmd variant; no conditional files are required. Finish with connection/query status and the returned membership value, or the specific connection failure.

Use `sqlcmd '-?'` to identify supported options. Microsoft supplies ODBC and Go implementations; TLS switches/defaults differ by version. Resolve certificate/name/trust failures against that client's documentation. Define `server` as the selected TCP endpoint and `login` as the known SQL login:

~~~bash
sqlcmd -X -S "$server" -U "$login" -l 15 -t 15 -b \
  -Q "SELECT IS_SRVROLEMEMBER('sysadmin') AS is_sysadmin;"
status=$?
~~~

Omit `-P` so the client prompts. `-X` disables startup commands and environment-derived settings; pass the intended connection explicitly. `-l` bounds login and `-t` query execution. `-Q` exits after the query; `-b` makes SQL errors above severity 10 fail.

An untrusted-domain integrated-authentication error is a failed connection, not password validation. SQL authentication is distinct from `-E` integrated authentication and requires an enabled SQL login.

For this query, `1` means membership, `0` means nonmembership and `NULL` means unresolved/invalid input or insufficient visibility. Membership is not a complete permissions inventory or the SQL service's OS identity. Retain diagnostics separately from the returned value.

References: [sqlcmd options](https://learn.microsoft.com/en-us/sql/tools/sqlcmd/sqlcmd-utility?view=sql-server-ver17), [IS_SRVROLEMEMBER interpretation](https://learn.microsoft.com/en-us/sql/t-sql/functions/is-srvrolemember-transact-sql?view=sql-server-ver17).
