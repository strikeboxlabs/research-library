---
name: pwgen
description: Generate a bounded set of random labels with pwgen on Linux. Use when length, output count, terminal defaults or collision assumptions affect a temporary non-secret identifier.
---

# Generate a label without claiming unique allocation

Read this entire SKILL.md before acting. Require the installed pwgen and select a non-secret label's length/count before generation. No conditional resource is required. Finish with successful generation and the observed shape; a random string does not reserve a filename, create a directory or prove uniqueness.

Set `length` and `count` to the required small positive integers. Inspect local help, then request explicit one-per-line output:

~~~bash
pwgen --help
pwgen -1 "$length" "$count"
status=$?
~~~

The positional values are character length followed by number of outputs. Without explicit choices, tty versus pipe output changes defaults, including column display and count. Capture status and require the expected nonempty lines/length before using a label; missing output is not a valid empty path.

Default pronounceable generation is appropriate here only for non-secret labels. It does not provide collision-free temporary storage. Use the environment's secure temporary-directory allocator when the task needs private, atomically reserved storage, rather than checking a generated name and later assuming it is free. A failed directory creation must not silently select an existing directory.

This label task does not create a password or change an account. Secret generation has separate entropy, storage and exposure requirements; do not infer them from a ten-character directory-name example. See the [pwgen manual](https://manpages.debian.org/unstable/pwgen/pwgen.1.en.html) for the installed generation's output options.
