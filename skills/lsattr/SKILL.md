---
name: lsattr
description: Inspect a selected Linux file's filesystem attributes with lsattr. Use when owner/write mode differs from actual write behavior, especially append-only or immutable files, without changing those attributes.
---

# Inspect attributes of the selected object

Read this entire SKILL.md before acting. Select an existing regular file or directory in the intended mount/namespace and require an installed compatible e2fsprogs lsattr. No conditional resources are required. Finish with the exact path, returned flags, diagnostics and access limits; an unsupported query is not evidence that no attributes exist.

Define `artifact` as that absolute path. Inspect this object without recursively listing a directory's contents:

~~~bash
lsattr -V -d -- "$artifact"
status=$?
~~~

`-V` reports the tool version as part of the invocation; `-d` selects the directory itself when the input is a directory. Check status and stderr, preserving the selected object's flag row separately from the version banner. Use an explicit non-symlink object; path resolution and concurrent replacement can otherwise change what was inspected. `-R` would broaden the traversal and is unnecessary for this task.

| Flag | Meaning for the selected object |
|---|---|
| `a` | Append-only: a file can be opened for writing only in append mode. Ordinary write permissions still matter. |
| `i` | Immutable: ordinary modification, deletion, rename and link creation are restricted. |
| `e` | Extent-based block mapping; this is not append-only or immutability. |

These are filesystem attributes, distinct from owner/group mode bits and POSIX ACLs. An owner-write mode does not override an append-only or immutable flag. Attribute support and enforcement depend on the filesystem and kernel; an ioctl/unsupported-operation error leaves this reader's result unavailable. The row is a snapshot, not a complete access verdict or proof about previously opened handles. Keep mount/access policy in the interpretation rather than testing a denial by modifying the selected file.

The flags do not identify who set them, prove that a service executes this pathname or grant authority to remove them. Correlate any service/process question with separate configuration and execution evidence. Resolve the installed flag meanings using [lsattr](https://manpages.debian.org/bookworm/e2fsprogs/lsattr.1.en.html) and the attribute descriptions in [chattr](https://manpages.debian.org/bookworm/e2fsprogs/chattr.1.en.html).
