---
name: stat
description: Inspect modification timestamps of a selected local artifact with GNU stat. Use when a kernel-file timestamp, symlink or rounded epoch value is mistaken for installation history or creation time.
---

# Inspect the selected object's modification time

Read this entire SKILL.md before acting. Select the existing file or symlink and decide whether the link itself or its referent is relevant; confirm GNU coreutils with `stat --version`. No conditional resources are required. Finish with the selected object, timestamp, status and interpretation limits; a failed query is not an epoch-zero timestamp.

Define `file` as that path. Inspect both integer epoch seconds and the displayed modification timestamp in UTC:

~~~bash
LC_ALL=C TZ=UTC0 stat --printf='mtime_epoch=%Y\nmtime=%y\n' -- "$file"
status=$?
~~~

Check stderr and `status`. Ordinary stat describes a symlink itself; add `-L` only for a deliberately selected referent. Preserve that choice in the result. `%Y` is modification time in integer epoch seconds; `%y` can retain fractional precision. It is not birth time or inode status-change time. Display precision does not establish filesystem or clock accuracy.

A greatest modification timestamp among matching kernel-image files identifies an observed file timestamp, not the currently running kernel, installation date or latest security update. Copies, restoration and deliberate timestamp setting can change it. Preserve the original value and compare relevant bytes/package/runtime evidence when the question concerns a change or version. A timestamp read can race with file replacement; name and time alone do not identify immutable contents.

See the packaged [GNU stat manual](https://manpages.debian.org/bookworm/coreutils/stat.1.en.html).
