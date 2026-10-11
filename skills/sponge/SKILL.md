---
name: sponge
description: Replace one owned text file from a fully staged transformation using moreutils sponge, without input truncation or treating pipeline error detection as rollback.
---

# Commit a staged text transformation

Read this entire SKILL.md before acting. Require an owned ordinary regular file, preserved original backup, stable source and fresh staging file. Confirm the installed moreutils implementation. Finish with both transformation and replacement status and the verified output.

Define `input` as the selected absolute path, `stage` as a fresh file outside the input, and `backup` as the separately preserved original. For an explicitly requested lexical sort:

~~~bash
LC_ALL=C sort -- "$input" > "$stage"
transform_status=$?
if [ "$transform_status" -eq 0 ]; then
  sponge "$input" < "$stage"
  replace_status=$?
fi
~~~

Check the staged result before replacement when the requested transformation has additional correctness conditions. `sponge` consumes stdin before opening its output, avoiding immediate truncation from `command < file > file`. A direct `sort file | sponge file` still replaces the file with whatever data arrives if the producer fails; Bash pipefail reports failure but cannot roll back that write. Staging separates these decisions.

Sponge preserves an existing file's permissions and uses atomic replacement when possible. Atomic replacement depends on temporary/output filesystem placement; symlinks and special files are written nonatomically, so they are outside this procedure. Set TMPDIR to an approved directory on the output filesystem if that guarantee matters, and verify the installed behavior.

On failure preserve stage, diagnostics and backup, then inspect the actual destination. File existence alone is insufficient. `-a` changes this to append behavior and is not part of this replacement task.

See the [moreutils sponge manual](https://manpages.debian.org/bookworm/moreutils/sponge.1.en.html).
