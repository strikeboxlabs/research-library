---
name: mktemp
description: Create a unique temporary file or directory in a selected Linux parent and retain its exact path for use and cleanup. Use when predictable names, an unexpected TMPDIR or creation failures affect a local task.
---

# Create the selected temporary object

Read this entire SKILL.md before acting. Choose an existing trusted parent and the required file or directory, then check creation before using its returned path. Finish with the required artifact/result and cleanup status; printing a candidate filename is insufficient.

Check `mktemp --version` for GNU coreutils. Define `scratch_dir` as the intended writable absolute directory:

~~~bash
temporary_file=$(mktemp -p "$scratch_dir" 'task.XXXXXXXXXX') || exit
~~~

This creates an empty ordinary file and prints its name. The template has at least three consecutive `X` characters in its final component. Explicit `-p` selects the directory; otherwise environment/default directory rules apply. The directory must already exist. Creation failure leaves no usable path: retain the diagnostic rather than falling back to a predictable name. `-u` only prints a name and does not reserve a file.

Keep the quoted returned path for the intended operation. GNU mktemp starts file permissions at user read/write, reduced by umask; this does not establish a different namespace's identity mapping or permissions. The file persists after the creating command exits. After consuming or moving the intended artifact, remove only this recorded file:

~~~bash
rm -- "$temporary_file"
~~~

For several related artifacts, reserve a directory instead of a file:

~~~bash
temporary_dir=$(mktemp -d -p "$scratch_dir" 'task.XXXXXXXXXX') || exit
~~~

`-d` creates the directory and prints its path; starting permissions are owner read/write/search, reduced by umask. Use this exact quoted path for the task's files. It is neither an isolation boundary nor evidence that a subprocess uses this directory. After the selected artifacts have been retained or individually removed as authorized, remove the empty directory:

~~~bash
rmdir -- "$temporary_dir"
~~~

Check cleanup status; a nonempty directory remains for the explicit artifact/retention decision. Do not derive wildcard or recursive cleanup from the template. See the [GNU coreutils mktemp manual](https://manpages.debian.org/bookworm/coreutils/mktemp.1.en.html).
