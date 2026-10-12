# Copy a selected owned directory locally

Require a stable reviewed source tree containing only the intended regular files/directories and a separate fresh owned destination directory. Both paths and their parents must be established; the destination must not lie inside the source. This workflow deliberately retains neither source ownership nor exact permissions. Exclude unrelated account/configuration files during source selection rather than allowing a privileged consumer to trust an unreviewed tree.

Set `source_dir` and `destination_dir` to the verified absolute directories. Inspect the plan:

~~~bash
rsync -a --no-perms --no-owner --no-group --dry-run --itemize-changes -- "$source_dir/" "$destination_dir/"
~~~

After confirming its selected entries, perform the intended copy:

~~~bash
rsync -a --no-perms --no-owner --no-group --itemize-changes -- "$source_dir/" "$destination_dir/"
copy_status=$?
~~~

The source slash selects directory contents, including dotfiles; it differs from a shell `*` operand. Archive mode enables recursion and time/link handling; the later no-options override selected metadata preservation. New permissions depend on source bits and destination creation rules, while existing files normally retain permissions. Verify effective output access instead of assuming no-perms means private.

Inspect status, diagnostics, expected filenames and bytes. Partial/vanished-source errors leave an incomplete copy, and a live tree is not a coordinated snapshot. Successful copying does not prove a later archive or cleanup succeeded. This procedure performs neither deletion nor source removal.

Reference: [rsync directory and permission semantics](https://download.samba.org/pub/rsync/rsync.1).
