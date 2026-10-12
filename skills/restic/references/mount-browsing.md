# Browse one existing repository through FUSE

Use the entrypoint's exact `repository` and `password_file`. Require Linux FUSE support and the installed mount helper expected by this restic build; missing kernel/helper support is a prerequisite gap. Inspect `restic mount --help` before selecting optional filters.

Define `mountpoint` as a new absolute private directory, outside and separate from any local repository tree. Do not mount over the repository, its parent or its descendants. Keep the serving process in a tracked foreground terminal:

~~~bash
mkdir -m 700 "$mountpoint" &&
restic -r "$repository" --password-file "$password_file" mount "$mountpoint"
~~~

Retain actual repository-open and serving/error output. A mountpoint directory alone is not a successful mount. In another terminal, inspect its actual layout and identify the snapshot by ID, host, time and paths using the entrypoint's snapshot listing. Do not assume `latest` selects the intended backup or that a path from another transcript exists in this mount. Opening a REST backend locally also requires the correctly mapped repository directory, not merely its server data root.

Browsing exposes backup content; it does not recreate the live source filesystem, execute that source or prove the preceding backup captured every requested file. Local cache/repository metadata may be written. Inspect selected data without executing scripts from the mount. Use the entrypoint's selected restore for larger recovery rather than treating a filesystem copy as complete metadata/hard-link restoration.

Finish by stopping the tracked serving process with Ctrl-C or the installed unmount procedure and confirm the mount has closed. An interrupted or busy unmount remains a cleanup gap; do not remove the mountpoint while it is serving. Keep the selected repository/snapshot and actual result attributable.

See [restic FUSE browsing and prerequisites](https://restic.readthedocs.io/en/stable/050_restore.html#restoring-using-mount) and [REST backend directory mapping](https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html#rest-server).
