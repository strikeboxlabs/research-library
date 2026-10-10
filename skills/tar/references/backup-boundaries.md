# Diagnose missing content across filesystem boundaries

First list the complete outer archive and check status. A backup bundle can contain separate archives for the ordinary configuration tree, mounted configuration, packages and other paths. List each relevant inner archive independently; absence from the first inner archive does not establish absence from the whole backup set.

GNU tar's `--one-file-system` limits recursive traversal during archive creation. Files explicitly named as source operands can still be included even if they reside on another filesystem. It does not filter an extraction, and removing it during extraction cannot recreate missing members.

If source-side inspection is available, define `source_path` as the original absolute directory in the backup process's namespace:

~~~bash
findmnt --kernel --target "$source_path" --output TARGET,SOURCE,FSTYPE,FSROOT,OPTIONS
findmnt --kernel --mountpoint "$source_path" --output TARGET,SOURCE,FSTYPE,FSROOT,OPTIONS
~~~

**Illustrative:** a backup recursively archives `/etc/.` with `--one-file-system`, while `/etc/pve` is a separate FUSE filesystem. The archive may retain the directory entry without its mounted contents. Proxmox pmxcfs uses this mount; inspect a separately captured pmxcfs archive or the backup design before inferring that the directory was empty on the live server. Do not run a restore script merely to inspect the bundle.

An empty extracted directory could also reflect exclusions, an unmounted source, permission errors, truncation or acquisition timing. Compare the actual creation command, logs/status, complete member list and source mount evidence. Current mount state cannot by itself prove a historical backup's state. Record “not present in this archive” separately from “did not exist”. Keep private configuration/key material in controlled working output, not runtime skill examples.

References: [GNU tar filesystem boundaries](https://www.gnu.org/software/tar/manual/html_node/one.html), [Proxmox cluster filesystem](https://pve.proxmox.com/pve-docs-9-beta/chapter-pmxcfs.html).
