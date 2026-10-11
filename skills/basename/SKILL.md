---
name: basename
description: Extract a pathname's final component or remove an exact selected suffix with GNU basename. Use when a script derives a label/type from a directory name and quoting or output delimiters affect the result.
---

# Derive the selected path component

Read this entire SKILL.md before acting. Require GNU basename and a selected pathname string; no conditional resources are required. Finish with the derived component and its intended mapping, separately from filesystem existence or access.

Define `path` as the complete path value and preserve it as one argument:

~~~bash
basename -- "$path"
status=$?
~~~

This removes directory components and trailing separators for display. It does not resolve symlinks, normalize the complete path or verify that anything exists. An **illustrative** `/srv/import/type with spaces/` yields `type with spaces`; the unquoted form can split it into multiple arguments or expand globs. A resulting label is not proof that an application's allowlist accepts it.

For an explicitly selected suffix, define `suffix` as the exact text and use `basename --suffix="$suffix" -- "$path"`. It removes that trailing suffix when present, rather than any arbitrary extension. This GNU option also enables multiple-name handling, so preserve the intended argument set.

Ordinary output is newline-terminated. Shell command substitution strips trailing newlines, including any that belong to the component itself. For exact filename processing, GNU `basename --zero -- "$path"` emits a NUL terminator; use a NUL-preserving consumer instead of a shell variable or line-splitting parser. Retain status and the original path if the transformation fails.

Reference: [GNU basename options](https://manpages.debian.org/bookworm/coreutils/basename.1.en.html).
