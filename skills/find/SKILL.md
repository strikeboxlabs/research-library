---
name: find
description: Locate files and interpret GNU find predicates without confusing incomplete searches or executing unintended actions. Use for scoped module searches, permission predicates, empty-directory checks, timestamp inventories and safe filename handling.
---

# Separate selection from actions

Read this entire SKILL.md before acting. Choose the search, emptiness or timestamp check, establish its root and coverage, then retain matches, status and diagnostics; a failed or bounded traversal cannot establish global absence.

Confirm GNU find with `find --version`. Define `search_root` as an existing absolute directory relevant to the task, `name_pattern` as the filename/glob to match, and `matches`/`errors` as fresh files:

~~~bash
find -P "$search_root" -xdev -type f -name "$name_pattern" -print0 > "$matches" 2> "$errors"
~~~

Check exit status and diagnostics before claiming absence. `-xdev` skips other filesystems and `-P` does not follow symlinks; both bound coverage. A `-type f` search can omit a symlink with the desired name. Inspect relevant link targets or mount boundaries deliberately instead of silently broadening to `/`. Suppressing all stderr conceals permission and traversal failures. Consume `-print0` output with a NUL-aware reader, not line splitting.

Match the predicate to the access question. `-type d -perm -o=r` selects directories with the other-read bit set; it neither lists regular files nor proves you can traverse every parent or read their contents. `-type d -perm -0001` instead selects directories with the other-search (execute) bit; it does not mean world-readable files. Directory search and directory listing are different access questions. `-perm 004` is an exact mode match, `-perm -004` requires that bit, and `-perm /044` accepts either group-read or other-read. For files readable by the current user, use `-type f -readable` within the same scoped search and retain its diagnostics. `-readable` considers access checks including ACLs, with NFS identity-mapping limitations; it does not establish another user's access or guarantee a later open will succeed.

For a selected owner search, use `-user "$owner"` with an established account name or numeric UID, keeping the same scoped root, regular-file selection and NUL output. This selects ownership, not effective write access, filesystem attributes or whether a service executes the file. Resolve the account mapping in the observed namespace; a name from another host can refer to a different numeric owner.

For a selected group-owned-file search, define `group_name` from the target's actual group mapping and keep the same scoped root/diagnostics:

~~~bash
find -P "$search_root" -xdev -type f -group "$group_name" -print0 > "$matches" 2> "$errors"
~~~

`-group` selects ownership, not membership or current access. Add `-perm -020` to select group-owned regular files whose group-write bit is set; the leading minus requires that bit while allowing other mode bits. A match does not establish effective write access: inspect the current identity, parent traversal, ACLs and filesystem policy before drawing that conclusion. Add `-perm -4000` only when set-user-ID files are the intended subset; inspect actual owner/mode, mount policy and execution context before claiming a privilege effect. A permission-denied path or a suppressed diagnostic leaves coverage incomplete. GNU find's `-ls` is a human listing, not the NUL-delimited evidence above.

To test whether **one directory itself** is empty, define `directory` and use:

~~~bash
find -P "$directory" -maxdepth 0 -type d -empty -print
~~~

Without `-maxdepth 0`, find also visits descendants. Without `-type d`, `-empty` can match empty regular files. No output can mean a nonempty directory, a different file type or a failed/incomplete check; retain diagnostics. A successful find exit means the traversal succeeded, not that a match was found. Testing emptiness and subsequently acting is not an atomic lock.

Implicit AND binds more tightly than `-o`; group alternatives with escaped parentheses when combining name tests with shared conditions/actions. Quote globs so the shell does not expand them first.

`-exec` runs a command for matches. Its terminating semicolon must reach find as an argument, normally `\;` or `';'`; an unquoted shell semicolon terminates the shell command instead. The command-line display in a process listing need not preserve original shell quoting. Preview matches with printing before choosing an action; `-delete` and session-launching commands are mutations, not search flags. For deliberate file processing, pass names as arguments rather than interpolating them into shell code.

## Inventory timestamps without inferring their cause

For an acquired tree, define `inventory` and `time_errors` as fresh output files outside `search_root`:

~~~bash
LC_ALL=C find -P "$search_root" -xdev -type f -printf '%T@\0%C@\0%p\0' > "$inventory" 2> "$time_errors"
~~~

Consume groups of three NUL-terminated fields: modification time, inode status-change time and pathname. Retain the raw epoch fractions when comparing; floating-point conversion may round them. `ctime` is not creation time. Check status/errors and the earlier symlink/mount limits before treating this as a complete inventory.

Zero versus nonzero fractions do not distinguish installed packages from modified files. Printed decimal length is not a promise of clock or filesystem precision, and copying, archive restoration or timestamp setting can affect values. Use timestamps to choose files for content comparison against an appropriate baseline; establish changes from bytes and metadata in context, not a fractional-time filter alone.

Consult the [GNU find manual](https://man7.org/linux/man-pages/man1/find.1.html) for permission predicates and access-check limits.
