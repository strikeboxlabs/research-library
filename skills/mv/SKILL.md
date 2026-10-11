---
name: mv
description: Rename a selected owned local file with GNU mv. Use when destination handling, a skipped no-clobber move or directory permissions obscure whether the intended file actually changed names.
---

# Rename the selected local file

Read this entire SKILL.md before acting. Confirm the requested rename and select an owned regular file plus a fresh destination in the same trusted parent directory, with no competing writer. Confirm GNU mv with `mv --version`. No conditional resources are required. Finish with status, source/destination observations and file identity; a skipped or ambiguous move remains unresolved.

Define `source` and `destination` as distinct absolute paths in that directory. Inspect the selected file and parent permissions before changing names. Reject a symlink source or an existing destination, including a dangling symlink. Retain the source's device/inode and relevant owner/mode:

~~~bash
stat --printf='device=%d inode=%i mode=%a uid=%u gid=%g size=%s\n' -- "$source"
mv -nT -- "$source" "$destination"
status=$?
stat --printf='device=%d inode=%i mode=%a uid=%u gid=%g size=%s\n' -- "$destination"
~~~

`-T` treats the destination as the exact filename rather than moving the source inside an existing directory. `-n` avoids overwriting an existing destination; a skip can return zero on some releases, so status alone does not establish completion. Check that the original path is absent (including as a symlink) and that the destination identifies the original file. If either check disagrees, preserve both observations and resolve the collision or concurrent change before retrying. Do not switch to `-f` to hide the failure.

A same-filesystem rename changes the directory entry rather than copying the file's contents. The file's inode identity, owner and mode normally remain the same; status-change and parent-directory timestamps can change. Existing open handles and other hard links can still refer to that file. It is not a contents backup or a secure deletion.

Parent-directory write/search permissions govern directory-entry changes; owning the file or its inode is not the same as controlling its containing directory. Sticky-bit rules, ACLs, immutable attributes, mount policy and namespaces can restrict the operation. A denied rename therefore does not necessarily mean the file itself needs a different mode. Inspect the actual paths and applicable policy before changing permissions.

For a move across filesystems, GNU mv can copy then remove the source. Do not apply the same-inode or atomic-rename conclusion to that operation; it needs separate byte/metadata and partial-copy checks. Remote filesystems can also leave ambiguous results after a reported error, so inspect both names before retrying.

Resolve implementation differences with the [GNU mv manual](https://manpages.debian.org/bookworm/coreutils/mv.1.en.html) and [Linux rename semantics](https://manpages.debian.org/bookworm/manpages-dev/rename.2.en.html).
