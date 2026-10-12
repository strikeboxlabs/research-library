# Back up one owned directory locally

Require an installed restic and a selected ordinary directory owned/readable by the invoking account. Define `source_dir` as its absolute path, `repository` as a fresh absolute local repository path, and `password_file` as an existing private file containing the chosen repository password. Resolve their parent paths and keep the repository, password file and diagnostic outputs outside the source tree. Review nested mounts and links before choosing the input; avoid changing files during this small backup/recovery check.

Inspect `restic version`, `restic backup --help` and inherited `RESTIC_*` settings. Password-command settings execute programs. Preserve the password through the established credential process; losing it can make the backup unrecoverable. Require free space and an owned destination parent. Stop if the repository path already exists, including a symlink:

~~~bash
umask 077
test ! -e "$repository" && test ! -L "$repository" &&
restic -r "$repository" --password-file "$password_file" init
~~~

Check status and the created repository identity before continuing. Initialization creates encrypted repository structures; it does not back up the source. For an existing repository, use its known identity/password instead of initializing over it.

Preview the selected directory, then run the same backup after reviewing the proposed scope:

~~~bash
restic -r "$repository" --password-file "$password_file" backup --dry-run --verbose=2 "$source_dir"
~~~

~~~bash
restic -r "$repository" --password-file "$password_file" backup --verbose "$source_dir"
backup_status=$?
~~~

Retain the final status, diagnostics and saved snapshot ID. Status3 means an incomplete snapshot with unreadable source files; a saved ID alone is insufficient. Status0 reports success for the selected input, while fatal/other errors require their actual diagnostic. Do not widen filesystem privileges to hide a read failure.

Inspect that exact snapshot with the entrypoint's listing, then restore a selected ordinary member to a fresh directory and compare its bytes with the unchanged original. Preserve the stored hierarchy: an absolute source path includes its parent structure. Finish with repository/snapshot identity, input scope, backup status and the separate restore/comparison result. Storage success does not establish application consistency for changing databases or live services. Keep the repository until its agreed retention decision; no pruning or deletion is part of this task.

References: [repository creation and credentials](https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html), [backup scope, dry runs and exit status](https://restic.readthedocs.io/en/stable/040_backup.html).
