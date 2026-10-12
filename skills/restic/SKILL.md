---
name: restic
description: Create a local backup of selected owned files, inspect an existing restic repository, restore selected paths or browse snapshots through FUSE. Use when credentials, partial snapshots, selection or restore filters obscure the result.
---

# Inspect and restore selected backup data

Read this entire SKILL.md before acting. Require the selected existing repository, its known encryption credential and any separate backend access. The inline task lists/selects a snapshot and restores reviewed paths into a fresh destination. For filesystem browsing, also read [FUSE repository browsing](references/mount-browsing.md) fully. Finish with repository/snapshot identity, operation status and the requested recovered data or browsing evidence; missing credentials, an incomplete restore or a failed mount remains unresolved.

For a new local repository and a backup of an ordinary owned directory, read [selected local backup](references/local-backup.md) fully first. That branch requires a fresh repository location and a prepared password file, rather than the existing repository required by the restore task.

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

Sources: [credentials](https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html), [restore selection](https://restic.readthedocs.io/en/stable/050_restore.html), [restore lock implementation](https://github.com/restic/restic/blob/master/cmd/restic/cmd_restore.go).
