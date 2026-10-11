# Write a selected server file with COPY

Use this for an authorized PostgreSQL server-file write with a verified connection and exact selected server path/content. COPY runs in the database server's filesystem as its OS service account. psql's \copy instead opens client files. Require the intended file effect and a restorable original, or a verified fresh disposable destination. SQL transaction rollback cannot restore a file that COPY already truncated or wrote.

## Establish actual role and server boundaries

In the existing psql connection, inspect:

~~~sql
SELECT current_database(), session_user, current_user, version();
SELECT current_setting('is_superuser');
SELECT pg_has_role(current_user, 'pg_write_server_files', 'USAGE');
\du
~~~

The server version comes from version(), separately from psql --version. A role with pg_write_server_files can use server COPY TO permitted OS paths without being a SQL superuser. That role does not grant pg_read_server_files or pg_execute_server_program; do not infer file-read or COPY PROGRAM authority from it. The database role name need not equal the OS service user. Directory permissions, service confinement and container namespace still restrict the file operation.

## Write one selected record

Define `service` as the reviewed libpq service, `server_path` as the inspected absolute server destination and `line` as one reviewed text record. Supply variables through psql stdin; the quoted literal form escapes their SQL values:

~~~bash
psql -X -w --dbname="service=$service connect_timeout=5" --set=ON_ERROR_STOP=1 --set=server_path="$server_path" --set=line="$line" <<'SQL'
COPY (SELECT :'line') TO :'server_path' WITH (FORMAT text);
SQL
~~~

COPY 1 means one row was written, not that its content was subsequently executed. Default text format adds a row newline and escapes tabs, newlines, carriage returns and backslashes. For an exact one-line shell marker, avoid those characters in the supplied line and verify the resulting bytes separately. This is not a general binary file writer. Data/configuration with escaping requirements needs a format designed for those bytes, such as a properly reviewed large-object export.

COPY TO opens an existing file for replacement, rather than append, and new files belong to the server OS account. Verify ownership, mode and content through an independently permitted filesystem observation; the SQL write role does not itself supply a read/backup mechanism. A later SQL error does not mean the old file survived. Preserve the complete original outside this write-only operation before replacement and restore it by a method that also preserves the required ownership/mode. A successful SQL status without independent verification supports the write result only.

## Conditional shell-startup reproduction

When the task explicitly includes a service-account login/startup reproduction, require its actual home, shell, launch command and chosen startup file. For Bash --login, /etc/profile precedes the first readable .bash_profile, .bash_login or .profile; .bashrc is conditional on sourcing or a different launch mode. Writing all these files is unnecessary and can destroy unrelated behavior. Use the selected file with its original preserved.

A one-line command such as `id > /owned/private/startup-identity` is **illustrative**; select a real private writable marker destination for that service account and ensure the text-format constraints above. COPY that reviewed line to the selected startup file only within the intended experiment, then initiate or observe the already authorized login trigger. A process transcript showing the marker helper under the database OS user proves that stage; it does not prove the privileged caller ran the command. Inspect real/effective identity in the resulting marker and restore the exact startup file when done.

A legacy su session sharing its caller's terminal can provide a separate TIOCSTI input-consumer boundary; it requires actual terminal/session evidence, a permitted kernel ioctl and the higher-privilege shell later consuming the queued input. COPY, login startup and terminal injection are separate stages. File write alone does not establish a root shell or arbitrary server program permission.

See PostgreSQL [COPY 12](https://www.postgresql.org/docs/12/sql-copy.html), [default server-file roles](https://www.postgresql.org/docs/12/default-roles.html), [COPY file-open implementation](https://github.com/postgres/postgres/blob/REL_12_STABLE/src/backend/commands/copy.c), [psql quoting](https://www.postgresql.org/docs/12/app-psql.html) and [Bash startup files](https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files.html).
