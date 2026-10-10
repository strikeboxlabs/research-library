---
name: mysqldump
description: Create a selected MySQL logical backup and diagnose incomplete compressed dumps. Use when a wrapper prints success despite SQL errors, force mode skips failures, or a gzip file is mistaken for a restorable backup.
---

# Check the dump, compression and recovery separately

Inspect `mysqldump --version` and `--help`, the server version and the job's existing option files. MariaDB may provide `mariadb-dump` or a compatibility name; verify its options independently. The procedure below covers an explicitly selected MySQL database, not full-server disaster recovery.

For an authorized InnoDB backup, define `db_host`, `db_port`, `db_user` and `database` from the intended connection, plus fresh absolute paths `archive` and `dump_log`. Preserve the required TLS options. `--single-transaction` does not make changing MyISAM/MEMORY tables consistent; concurrent DDL can invalidate the dump. Establish engine and change-window conditions first.

Run in Bash with a terminal available for the password prompt:

~~~bash
(
  umask 077
  set +e
  set -o noclobber
  mysqldump --protocol=TCP --host="$db_host" --port="$db_port" \
    --user="$db_user" --password --single-transaction --quick \
    --log-error="$dump_log" --databases "$database" |
    gzip >"$archive"
  stages=("${PIPESTATUS[@]}")
  printf 'mysqldump=%s gzip=%s\n' "${stages[0]}" "${stages[1]}"
  if (( stages[0] != 0 || stages[1] != 0 )); then
    printf 'Incomplete candidate; inspect dump diagnostics\n' >&2
    exit 1
  fi
  gzip -t -- "$archive"
)
~~~

Copy `PIPESTATUS` immediately; even a subsequent assignment or diagnostic command replaces it. The isolated subshell disables inherited `errexit` so both statuses can be reported. In an ordinary pipeline, `$?` alone normally reports the last stage: gzip can successfully compress partial input after the producer fails. `noclobber` protects an existing archive; `--log-error` appends, so choose a fresh log for this attempt. Keep failed candidates and diagnostics separate from accepted backups.

An **illustrative** result `mysqldump=2 gzip=0` means compression succeeded after the dump failed. A successful `gzip -t` proves compressed-stream integrity, not complete SQL, selected-object coverage or restorability. Likewise, an unconditional shell `echo` announcing completion proves nothing about earlier stages.

| Evidence | Next decision |
|---|---|
| SQL errors with `--force` | Treat the output as potentially incomplete. That flag continues past errors; identify omitted objects before considering a backup valid. |
| `LOCK TABLES` or privilege error | Check the selected objects, engine and account privileges. Do not silently exclude failed tables or assume adding force repairs consistency. |
| Column-statistics warning | Compare client/server capabilities and the actual fatal error separately; a warning does not explain every failure. |
| Both stages succeed, compression verifies | Review diagnostics and required object coverage, then validate recovery in an approved isolated database. |

Decide whether routines and events belong in scope; they need explicit options. `--databases` includes database-selection/creation statements, so restoring can affect names embedded in the SQL. Never test restoration against the source server. A tested restore should verify the required tables, rows and application checks, with target/version recorded.

Use the matching [mysqldump option reference](https://dev.mysql.com/doc/refman/8.4/en/mysqldump.html) and [backup/reload guidance](https://dev.mysql.com/doc/refman/8.4/en/using-mysqldump.html). Do not pass credentials in command-line values merely to automate the prompt; use an existing protected credential configuration for unattended operation.
