---
name: ls
description: Inspect selected Linux directory entries and permission metadata with GNU ls. Use when hidden entries, directory versus file modes, numeric owners or misleading timestamps obscure local filesystem evidence.
---

# Inspect a selected directory and its entries

Read this entire SKILL.md before acting. Select the existing directory and current namespace; confirm GNU coreutils with `ls --version`. No conditional resources are required. Finish with the listing, errors, observation time and relevant metadata limits; a failed listing is not an empty directory.

Define `directory` as the selected path. Inspect that directory's own metadata separately from its entries:

~~~bash
LC_ALL=C ls -ld --quoting-style=escape -- "$directory"
LC_ALL=C ls -la --quoting-style=escape -- "$directory"
~~~

`-d` lists the directory itself; without it the directory's contents are listed. `-a` includes dot-prefixed entries, including `.` and `..`. Escape quoting makes unusual filename bytes visible; displayed wrapping or escapes are not literal filename separators. Do not parse long-listing columns to build executable commands.

Read type, mode, owner/group and timestamp together. A numeric owner can mean name lookup failed; it does not identify a host mount. Add `-n` when numeric IDs are needed. A directory's reported size is not its children's total size. Ordinary long format shows modification time, not creation time or the identity of the last writer.

File mode and parent-directory permissions answer different questions. Directory read permission can allow entry names to be enumerated while missing search/execute permission prevents resolving those entries for stat or file access. Names followed by question-mark metadata and permission errors are neither an empty directory nor proof of readable content. Conversely, directory write plus search can permit creating/removing known names even when missing read prevents listing the directory; read permission on an individual file remains separate. A failed listing therefore does not establish an unwritable directory. A restrictive file mode alone does not establish protection against changes to its directory entry. Sticky-bit, ACL, mount and namespace policy can further restrict operations; a permission marker is a cue for the relevant metadata reader, not a complete effective-access verdict. On mounted filesystems, displayed owner names come from the client's name resolution; preserve numeric IDs before claiming an identity or ownership changed. Preserve diagnostics and retain the exact selected paths; concurrent changes can make separate listings disagree. See [GNU's directory-mode model](https://github.com/coreutils/coreutils/blob/master/doc/perm.texi) when distinguishing these operations.

See the packaged [GNU ls manual](https://manpages.debian.org/bookworm/coreutils/ls.1.en.html).
