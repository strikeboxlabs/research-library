---
name: npbackup-cli
description: Inspect NPBackup repositories, select exact snapshots and recover a selected file while separating backend success from wrapper policy failures. Use when alternate configurations, latest snapshots or dump output make recovery ambiguous.
---

# Inspect a selected NPBackup repository

NPBackup wraps restic with configuration, permissions and policy checks. Use a trusted installed build and a reviewed configuration for one approved repository. Define `config` as its absolute path, `repo` as one exact repository name, and `log` as a private writable log path. Retain the original configuration: newer versions may migrate it when loading. Review inherited group settings, password commands, hooks and automatic upgrade settings before consuming a copied configuration; an inspection operation can still invoke configured helpers or write logs/cache.

~~~bash
npbackup-cli --help
npbackup-cli --version --log-file "$log"
npbackup-cli -c "$config" --repo-name "$repo" --log-file "$log" --snapshots --json
~~~

Check command status and the JSON result/reason before selecting data. `--check-config-file` tests configuration loading, not repository access, snapshot integrity or safe helper behavior. An encrypted `__NPBACKUP__...` value does not itself show the destination, grant access or authenticate other plaintext fields. Avoid `--repo-group`, comma-separated names and `__all__` when investigating a single repository.

Choose `snapshot` from the observed inventory after checking host, time and saved paths:

~~~bash
npbackup-cli -c "$config" --repo-name "$repo" --log-file "$log" --ls "$snapshot" --json
~~~

`--ls` takes its own optional snapshot argument; omitting it selects `latest`. `--snapshot-id` selects the snapshot for dump/restore, so do not assume it overrides a bare `--ls`. `--list` lists backend object categories and is different from `--snapshots`. Keep the selected ID through recovery so a concurrent backup cannot silently change the source.

## Recover one observed file

Define `member` as one exact regular-file path from that snapshot and `candidate`/`errors` as fresh private local files. Confirm this build's handling of unusual path characters before passing them through its restic wrapper. Dump to a candidate, keeping stderr separate:

~~~bash
umask 077
if npbackup-cli -c "$config" --repo-name "$repo" --log-file "$log" \
    --snapshot-id "$snapshot" --dump "$member" >"$candidate" 2>"$errors"; then
  printf 'Dump command succeeded; verify candidate content and size.\n'
else
  status=$?
  printf 'Dump status %s; retain candidate as incomplete and inspect logs.\n' "$status" >&2
fi
~~~

Use dump mode without JSON/debug output when recovering bytes. A failure can print diagnostic text to stdout, so a nonempty candidate is not proof of recovered content. Version 3.0.4 fixed a dump path that interpreted output as text; do not assume earlier builds preserve arbitrary binary files. Verify format, length and any known checksum before accepting the candidate. Never execute a restored script to identify it.

## Interpret a backup failure before retrying

An **illustrative** sequence `snapshot ... saved`, backend success, then a minimum-size failure means the wrapper rejected a condition after the backend wrote a snapshot. It does not imply rollback. Inspect that exact snapshot and compare configured paths/exclusions and expected data volume before rerunning. Newer code can report the size condition as a warning, and warning severity can still affect process exit status; preserve both the detailed result and final status.

For an authorized backup, `-b` starts the configured job. `-f` bypasses the recent-backup age gate; it is not restic's own force option and does not waive every policy check. It can also bypass random delay in newer versions. `--use-fs-snapshot` is a Windows feature; its presence on Linux does not establish a consistent filesystem snapshot. Backup hooks and repository writes are separate effects from inspection. Do not turn a small-backup error into an automatic forced retry, retention-policy change or cleanup.

Use [upstream CLI definitions](https://github.com/netinvent/npbackup/blob/main/npbackup/__main__.py), [runner behavior](https://github.com/netinvent/npbackup/blob/main/npbackup/core/runner.py) and the [changelog](https://github.com/netinvent/npbackup/blob/main/CHANGELOG) to resolve installed-version differences.
