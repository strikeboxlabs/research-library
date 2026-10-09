---
name: restic
description: Inspect an existing restic backup repository and restore selected snapshot paths. Use when repository credentials, snapshot selection, password-command execution or restore filters need careful interpretation.
---

# Inspect and restore selected backup data

Define `repository` as the exact existing repository location and `password_file` as a private file holding its known repository password. Repository encryption credentials and backend transport credentials are separate. A Backrest web-login password or bcrypt verifier is not automatically the repository password.

~~~bash
restic version
restic -r "$repository" --password-file "$password_file" snapshots --json
~~~

Check inherited `RESTIC_*` configuration when results or authentication are unexpected. `--password-command` and `RESTIC_PASSWORD_COMMAND` execute a local program to obtain the password, even when the requested operation looks like inspection. Do not copy that setting from an untrusted configuration. `init` creates a repository; it does not repair access to an existing one.

Choose an exact observed snapshot ID after checking host, time and saved paths. Define `snapshot` as that ID and inspect its paths:

~~~bash
restic -r "$repository" --password-file "$password_file" ls "$snapshot"
~~~

Define `member` as an observed snapshot path and `destination` as a new absolute directory. Review a selected restore before writing files:

~~~bash
mkdir -m 700 "$destination" && restic -r "$repository" --password-file "$password_file" restore "$snapshot" --include "$member" --target "$destination" --dry-run --verbose=2
~~~

After checking the selection, repeat that restore command without `--dry-run`. Confirm installed help supports these flags. `--include` is a pattern, so inspect actual matches, especially names containing wildcard characters. The restored hierarchy is relative to the snapshot root; do not assume the file appears directly inside `destination`.

`--path` selects which snapshot to use; it does **not** restrict which files are restored. Avoid ambiguous `latest` selection across hosts or paths. Default restoration may overwrite destination files; the new directory keeps this separate from live application data. Do not add `--delete` for ordinary recovery.

Restore, including dry-run, can acquire a repository lock and use a local cache. Thus a file dry-run is not a guarantee of no repository/local metadata writes. Investigate lock ownership and active operations before considering `unlock`; do not blindly use `--no-lock`. Verify recovered file content/size and the command's final status, not only a progress line.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Artificial pp. 9–14. Sources: [credentials](https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html), [restore selection](https://restic.readthedocs.io/en/stable/050_restore.html), [restore lock implementation](https://github.com/restic/restic/blob/master/cmd/restic/cmd_restore.go).
