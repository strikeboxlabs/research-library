---
name: rsync
description: Inspect a scoped rsync daemon module, retrieve one selected file or push a selected backup over SSH. Use to distinguish transport, filename scope and skipped or partial copies from completed transfers.
---

# Inspect a module before retrieving a file

Read this entire SKILL.md before acting. Establish the intended endpoint, existing access and selected file. For a local backup pushed over SSH, read [selected backup transfer](references/backup-transfer.md) fully first; otherwise use the daemon inspection/retrieval below. Finish with actual transferred or skipped files, status and destination verification. Missing access or an incomplete source leaves that step unresolved.

Check `rsync --version`. Define `daemon_url` as the authorized `rsync://host:port` endpoint, without a trailing slash:

~~~bash
rsync --list-only "$daemon_url/"
~~~

The result lists advertised modules, not filesystem roots. A module can be hidden from listings; a listed module can still require authentication or restrict files. A password challenge or access denial is not permission to guess credentials. Daemon users need not be system accounts.

Define `module_url` from an observed module name. List its top level without archive mode or recursion:

~~~bash
rsync --list-only "$module_url/"
~~~

An **illustrative** `-rw-r--r-- 12544 ... config-backup.tar.gz` identifies a regular-file candidate and size; it does not prove download permission or completeness. Descend into a relevant observed subdirectory explicitly.

For a selected regular file, define `source_url` as its complete module URL with no wildcard, and `dest` as a new absolute directory under the private case workspace:

~~~bash
umask 077
mkdir -- "$dest" && rsync --dry-run --itemize-changes --ignore-existing "$source_url" "$dest/"
~~~

Review that the plan contains only the intended file. When retrieval is intended, use the same arguments without the dry-run flag:

~~~bash
rsync --itemize-changes --ignore-existing "$source_url" "$dest/"
~~~

Check status, diagnostics and the actual expected file. `--ignore-existing` skips an existing file, including an incomplete one; it does not skip existing directories. Success alone does not prove a new copy. Use another fresh destination after resolving a partial transfer. Compare size and an independently available digest; keep archive extraction separate.

`rsync://host/module/path` and `host::module/path` use the daemon protocol; `host:path` uses a remote shell, normally SSH. Direct daemon traffic is not automatically encrypted. A source-directory trailing slash changes directory-copy layout, and `-a` adds recursion and metadata/link preservation: neither is needed for this single-file task. Do not add deletion or source-removal flags to retrieval.

See the [rsync manual](https://download.samba.org/pub/rsync/rsync.1) and [module access configuration](https://download.samba.org/pub/rsync/rsyncd.conf.5).
