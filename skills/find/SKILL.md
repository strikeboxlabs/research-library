---
name: find
description: Locate files and interpret GNU find predicates without confusing incomplete searches or executing unintended actions. Use for scoped module searches, permission predicates, empty-directory checks and safe filename handling.
---

# Separate selection from actions

Confirm GNU find with `find --version`. Define `search_root` as an existing absolute directory relevant to the task, `name_pattern` as the filename/glob to match, and `matches`/`errors` as fresh files:

~~~bash
find -P "$search_root" -xdev -type f -name "$name_pattern" -print0 > "$matches" 2> "$errors"
~~~

Check exit status and diagnostics before claiming absence. `-xdev` skips other filesystems and `-P` does not follow symlinks; both bound coverage. A `-type f` search can omit a symlink with the desired name. Inspect relevant link targets or mount boundaries deliberately instead of silently broadening to `/`. Suppressing all stderr conceals permission and traversal failures. Consume `-print0` output with a NUL-aware reader, not line splitting.

Match the predicate to the access question. `-type d -perm -o=r` selects directories with the other-read bit set; it neither lists regular files nor proves you can traverse every parent or read their contents. `-perm 004` is an exact mode match, `-perm -004` requires that bit, and `-perm /044` accepts either group-read or other-read. For files readable by the current user, use `-type f -readable` within the same scoped search and retain its diagnostics. `-readable` considers access checks including ACLs, with NFS identity-mapping limitations; it does not establish another user's access or guarantee a later open will succeed.

To test whether **one directory itself** is empty, define `directory` and use:

~~~bash
find -P "$directory" -maxdepth 0 -type d -empty -print
~~~

Without `-maxdepth 0`, find also visits descendants. Without `-type d`, `-empty` can match empty regular files. No output can mean a nonempty directory, a different file type or a failed/incomplete check; retain diagnostics. A successful find exit means the traversal succeeded, not that a match was found. Testing emptiness and subsequently acting is not an atomic lock.

Implicit AND binds more tightly than `-o`; group alternatives with escaped parentheses when combining name tests with shared conditions/actions. Quote globs so the shell does not expand them first.

`-exec` runs a command for matches. Its terminating semicolon must reach find as an argument, normally `\;` or `';'`; an unquoted shell semicolon terminates the shell command instead. The command-line display in a process listing need not preserve original shell quoting. Preview matches with printing before choosing an action; `-delete` and session-launching commands are mutations, not search flags. For deliberate file processing, pass names as arguments rather than interpolating them into shell code.

Consult the [GNU find manual](https://man7.org/linux/man-pages/man1/find.1.html) for permission predicates and access-check limits.
