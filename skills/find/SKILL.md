---
name: find
description: Locate files and interpret GNU find predicates without confusing incomplete searches or executing unintended actions. Use for scoped module searches, empty-directory checks and safe filename handling.
---

# Separate selection from actions

Confirm GNU find with `find --version`. Define `search_root` as an existing absolute directory relevant to the task, `name_pattern` as the filename/glob to match, and `matches`/`errors` as fresh files:

~~~bash
find -P "$search_root" -xdev -type f -name "$name_pattern" -print0 > "$matches" 2> "$errors"
~~~

Check exit status and diagnostics before claiming absence. `-xdev` skips other filesystems and `-P` does not follow symlinks; both bound coverage. A `-type f` search can omit a symlink with the desired name. Inspect relevant link targets or mount boundaries deliberately instead of silently broadening to `/`. Suppressing all stderr, as in the writeup, conceals permission and traversal failures. Consume `-print0` output with a NUL-aware reader, not line splitting.

To test whether **one directory itself** is empty, define `directory` and use:

~~~bash
find -P "$directory" -maxdepth 0 -type d -empty -print
~~~

Without `-maxdepth 0`, find also visits descendants. Without `-type d`, `-empty` can match empty regular files. No output can mean a nonempty directory, a different file type or a failed/incomplete check; retain diagnostics. A successful find exit means the traversal succeeded, not that a match was found. Testing emptiness and subsequently acting is not an atomic lock.

Implicit AND binds more tightly than `-o`; group alternatives with escaped parentheses when combining name tests with shared conditions/actions. Quote globs so the shell does not expand them first.

`-exec` runs a command for matches. Its terminating semicolon must reach find as an argument, normally `\;` or `';'`; an unquoted shell semicolon terminates the shell command instead. The command-line display in a process listing need not preserve original shell quoting. Preview matches with printing before choosing an action; `-delete` and session-launching commands are mutations, not search flags. For deliberate file processing, pass names as arguments rather than interpolating them into shell code.

Documentation reviewed 2026-10-09; Linux execution untested. Cases: Backdoor pp. 12–14; BackendTwo p. 18. Source: [GNU find manual](https://man7.org/linux/man-pages/man1/find.1.html).
