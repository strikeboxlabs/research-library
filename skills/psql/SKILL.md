---
name: psql
description: Connect to a known PostgreSQL database, inspect schema, export bounded results and administer selected server files/WAL archiving with psql. Use when socket versus TCP authentication, SQL role, startup files, quoting or partial output obscures a result.
---

# Establish the PostgreSQL connection

Read this entire SKILL.md before acting; reuse complete current context. Establish the actual server/database/role, inspect the selected schema and retain query status with bounded results. A failed reconnect or export remains incomplete; do not infer permissions or database identity from a prompt alone.

For an explicitly approved server-file/configuration operation or WAL archive hook, read [large objects and archive configuration](references/server-files-and-archiving.md) fully first. These are server-side effects, separate from ordinary query export.

Check `psql --version` separately from the server version. Define `service` as an existing reviewed libpq service name with the intended host, port, database, role and TLS policy. Use known credentials through its protected password file; on Linux, a password file with group/world access is ignored.

~~~bash
psql -X -w --dbname="service=$service connect_timeout=5" --set=ON_ERROR_STOP=1 --pset=pager=off -c '\conninfo' -c 'SELECT current_database(), session_user, current_user, version();'
~~~

`-X` skips system/user psql startup files. `-w` suppresses password prompts; it does not bypass authentication. For an interactive known-password login, replace it with `-W`. The latter forces a prompt, not password authentication at the server. Keep passwords out of command arguments.

Explicit `host=localhost` uses TCP in the client's network namespace; omitting host normally selects a Unix socket on Linux. These can match different server authentication rules. A connection refusal, authentication rejection and SQL permission error belong to different stages. Do not cycle credentials to diagnose the wrong endpoint. `current_user` is the effective SQL role, not the client's OS user; TLS encryption alone does not prove server identity without the appropriate verification policy.

## Inspect before selecting rows

For an interactive session, reuse the connection options without `-c`. `\list` lists databases, not their tables or permission to use them. If the selected database differs, use `\connect` with its exact observed name, then recheck `\conninfo` and `SELECT current_database(), current_user;`. A failed interactive reconnect can leave the old connection active; a noninteractive reconnect failure closes the old connection. Then inspect the relevant schema with metadata commands. The following `public.users` name is **illustrative**; replace it with the observed relation:

~~~text
\conninfo
\dt public.*
\d public.users
~~~

Bare `\dt` is limited to tables visible through the current schema search path; it is not a complete database inventory. `\dt public.*` explicitly selects that schema; `\dt *.*` broadens the metadata listing across schemas when needed. These are psql patterns, not shell globs. The table list and description establish names/types, not permission to read every row. Schema-qualify queries: an unqualified name depends on `search_path`. A missing relation can mean the wrong database/schema/case; permission denial does not mean an empty table. Preserve account-to-record mappings when extracting selected application fields; a column named `password` does not establish its hash format.

## Export one bounded, reviewed selection

After verifying the illustrative schema and columns below, define `account_label` as the selected non-secret lookup value and `output` as a fresh private CSV path. Adapt the fixed identifiers and required columns first:

~~~bash
umask 077
psql -X -w --dbname="service=$service connect_timeout=5" --set=ON_ERROR_STOP=1 --set=account_label="$account_label" --quiet --csv --pset=pager=off >"$output" <<'SQL'
BEGIN READ ONLY;
SET LOCAL statement_timeout = '5s';
SELECT id, username
FROM public.users
WHERE username = :'account_label'
ORDER BY id
LIMIT 50;
COMMIT;
SQL
~~~

Check exit status immediately and preserve stderr. With `ON_ERROR_STOP`, a script error returns 3; fatal client errors return 1 and a failed/lost noninteractive connection returns 2. Output may already contain rows on failure, so keep it marked incomplete. Successful zero-row output establishes only that this role/query saw no matches. A row limit bounds output, not necessarily work; the statement timeout bounds each server statement.

The quoted heredoc lets psql handle `:'account_label'` as an escaped SQL literal. `:"name"` quotes one identifier; `:name` inserts raw text. Do not interpolate shell values into SQL source. These psql substitutions belong in stdin or a script; `-c` SQL is sent directly to the server. `--csv` needs psql 12+ and preserves CSV quoting; plain unaligned separators are ambiguous when fields contain them.

`READ ONLY` constrains the database transaction, not every possible effect of an unreviewed script or function. Review SQL and backslash commands before execution. `\copy` accesses files as the client user; server `COPY ... TO 'file'` uses the server filesystem/privileges, and program forms can execute commands. Neither is a passive alternate spelling of display output.

See the [psql manual](https://www.postgresql.org/docs/current/app-psql.html), [connection services](https://www.postgresql.org/docs/current/libpq-pgservice.html), [password files](https://www.postgresql.org/docs/current/libpq-pgpass.html), [transaction limits](https://www.postgresql.org/docs/current/sql-set-transaction.html) and [statement timeouts](https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-STATEMENT-TIMEOUT).
