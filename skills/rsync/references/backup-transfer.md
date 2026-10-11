# Push one completed backup over SSH

Require a stable completed regular file, authorized existing SSH access, matching rsync availability at both ends and a known destination directory. Define `source_file` as the selected absolute local path and `destination` as `user@host:/absolute/directory/`, retaining the trailing slash. Review any configured transport wrapper before use.

~~~bash
rsync --dry-run --itemize-changes --ignore-existing -t -- "$source_file" "$destination"
~~~

After reviewing the plan, repeat without `--dry-run` when transfer is intended. Retain status/diagnostics and verify the destination bytes against the source. A dry run may contact/authenticate to the remote endpoint; it makes no transfer changes.

`-t` preserves modification times, not ownership or every archive attribute. `--ignore-existing` can skip an incomplete destination file; choose a fresh destination after resolving the failed attempt. Successful transfer does not validate the database dump inside it.

For an acquired job, inspect its actual working directory, shell expansion and argv without running it. `*.*` selects names containing a dot, normally omitting hidden names. Prefer one explicit absolute operand and the end-of-options delimiter over unreviewed wildcard inputs. Missing source, failed `cd`, skipped output or an earlier dump error needs its own result before declaring the backup complete.

Reference: [rsync manual](https://download.samba.org/pub/rsync/rsync.1).
