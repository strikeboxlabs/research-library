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

File mode and parent-directory permissions answer different questions. A restrictive file mode alone does not establish protection against changes to its directory entry. Sticky-bit, ACL, mount and namespace policy can further restrict operations; a permission marker is a cue for the relevant metadata reader, not a complete effective-access verdict. Preserve diagnostics and retain the exact selected paths; concurrent changes can make separate listings disagree.

See the packaged [GNU ls manual](https://manpages.debian.org/bookworm/coreutils/ls.1.en.html).
