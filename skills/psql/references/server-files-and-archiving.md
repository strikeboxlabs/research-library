# Server files, large objects and WAL archiving

Use this for approved PostgreSQL server-file recovery or configuration changes with the actual SQL role and server identity established. A SQL-injection writeup can demonstrate these SQL functions without ever invoking psql; here psql is a direct, authenticated carrier for the same documented operations. SQL injection syntax depends on the application's statement context and is not a universal psql prefix.

Inspect the effective role and existing settings before deciding whether a file operation is possible:

~~~sql
SELECT current_user, current_setting('is_superuser'), version();
SHOW config_file;
SHOW data_directory;
SHOW archive_mode;
SHOW archive_command;
SHOW archive_library;
SHOW wal_level;
SELECT name, setting, context, source, pending_restart
FROM pg_settings
WHERE name IN ('archive_mode','archive_command','archive_library','archive_timeout','wal_level');
~~~

`archive_library` is present in PostgreSQL 15+, so adapt for an older server rather than interpreting an unknown setting as an absent archive. The client version is not the server version. A displayed database hostname/role does not establish root on that OS.

## Recover one server file

Server `lo_import`/`lo_export` access the **server's** filesystem as the database service OS user; they are not the client's `\copy`. Defaults restrict these file functions to SQL superusers, but explicit grants can change that. File ACLs, service confinement and directories still matter. An ordinary large object capability is not proof of unrestricted server-file access.

With `service` selecting the already reviewed connection and `file_path` one selected absolute **server** path, use a fresh private output destination and retain errors separately. In a connected psql session:

~~~sql
\set ON_ERROR_STOP on
BEGIN;
SELECT lo_import(:'file_path') AS owned_oid \gset
SELECT encode(lo_get(:owned_oid), 'base64');
SELECT lo_unlink(:owned_oid);
COMMIT;
~~~

Supply the variable through `--set=file_path="$file_path"` on the psql invocation; `:'file_path'` quotes an SQL literal. The base64 represents file bytes. Preserve the result without wrapped HTML/table markup; decode one transport layer at a time into a working file. A SQL result rendered by a web UI may require HTML decoding, but replacing every entity or backslash globally can corrupt the file. Keep evidence of the exact byte length/digest before a later write. A `COPY ... FROM stdin` section in a recovered dump is input data associated with its table/columns; do not execute the whole dump merely to inspect account records.

These operations create/delete an owned database large object. Do not hardcode a frequently reused OID from a walkthrough or delete an unrelated object. A failed transaction can leave subsequent commands ignored until rollback; establish which effects committed.

## Replace a selected configuration file and apply reloadable settings

Require an exact restorable copy, file ownership/path, existing configuration/includes, and an approved change to the particular cluster. Replacing the whole file with a short fragment can discard unrelated settings. Keep the original bytes and verify only the intended differences in a complete replacement. Do not overwrite an active production archive chain as a diagnostic.

For an owned disposable archive test whose archiving is already enabled, an **illustrative configuration fragment** is:

~~~text
archive_command = 'test ! -f /private/archive/"%f" && cp -- "%p" /private/archive/"%f"'
~~~

The directory is illustrative, must exist and be writable by this database service, and the programs must match its execution environment. `%p` is the server WAL path; `%f` is its segment filename. This runs an OS command as the database service. The example avoids overwriting an existing archive file but is not a production idempotence/error policy; a real archive command must handle retries and an already successfully archived segment correctly. Preserve functioning backups and their destination/security policy. A marker-only command returning zero can falsely acknowledge archiving and destroy the usable archive chain.

`archive_mode` and `wal_level` require server startup/restart changes. A reload cannot turn an initially disabled mode into `always`; do not claim this from a true reload result. With the required mode already active and `archive_library` empty, `archive_command` can be reloaded. A tiny `archive_timeout` does not guarantee immediate invocation without WAL activity/segment completion and can bloat archives.

Define `config_path` as the selected server configuration file and `config_b64` as base64 of the reviewed **complete replacement bytes**, not a shell-command payload. With the existing connection and those psql variables:

~~~sql
\set ON_ERROR_STOP on
SELECT lo_from_bytea(0, decode(:'config_b64', 'base64')) AS owned_oid \gset
SELECT lo_export(:owned_oid, :'config_path');
SELECT lo_unlink(:owned_oid);
SELECT pg_reload_conf();
SELECT sourcefile, sourceline, name, applied, error
FROM pg_file_settings
WHERE error IS NOT NULL OR name IN ('archive_mode','archive_command','archive_library','archive_timeout','wal_level');
SELECT name, setting, pending_restart
FROM pg_settings
WHERE name IN ('archive_mode','archive_command','archive_library','archive_timeout','wal_level');
~~~

`0` requests a new object identifier; a supplied nonzero OID must not already exist. Export overwrites the selected file, including effects that a later database rollback cannot undo. `pg_reload_conf()` returning true means the signal was sent, not that every setting applied or that a command executed. Read configuration errors, effective settings and server logs. Complete with the selected WAL archive result and checksum where applicable; a delayed/missing file remains unestablished. If settings require restart, report that prerequisite rather than silently restarting the cluster.

Restore the original complete configuration bytes through the same owned-file procedure when the temporary test ends, reload if appropriate, then verify settings/errors and normal archiving. Account for only your own large objects and temporary artifacts. See PostgreSQL [large-object functions](https://www.postgresql.org/docs/15/lo-funcs.html), [WAL configuration](https://www.postgresql.org/docs/15/runtime-config-wal.html) and [reload/configuration inspection](https://www.postgresql.org/docs/15/functions-admin.html).
