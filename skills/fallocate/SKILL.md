---
name: fallocate
description: Preallocate a selected owned file with Linux util-linux fallocate. Use when logical size, allocated space, zero-filled reads or filesystem support determine a local fixture's behavior.
---

# Allocate a fresh local file

Read this entire SKILL.md before acting. Require Linux util-linux and a fresh absolute filename in a private owned directory without other writers. Select the required length and filesystem. No conditional resources are required. Finish with command status, the resulting logical size and allocation evidence; a size alone does not establish contents or physical allocation.

Check `fallocate --version` and `fallocate --help`. Define `file` as that nonexistent path. For a one-MiB local fixture:

~~~bash
umask 077
fallocate --length 1MiB -- "$file"
status=$?
~~~

Status 0 reports success; 1 reports failure. Keep diagnostics and inspect any partially created output before retrying with a fresh name. Permission, space and unsupported filesystem errors require their actual cause; do not replace allocation with a sparse-file operation while claiming the same result.

Default allocation starts at offset zero and extends the file when needed. Newly allocated regions read as zeroes, but existing data is preserved: rerunning this command on a populated file does not clear its contents or shorten a larger file. Use the private-directory prerequisite to prevent an unexpected existing file or symlink being modified.

`1M` and `1MiB` mean 1,048,576 bytes; `1MB` means 1,000,000. `--keep-size` intentionally preserves apparent length, so it changes this fixture contract. Allocation uses filesystem extents and can reserve more than the requested bytes. Zero-filled reads do not mean every data block was physically written with zeroes. Hole punching and zero-range operations change contents and are separate tasks.

Record the actual file's logical size and allocated blocks using the image's established metadata tools. A successful allocation does not demonstrate an application's read duration or provide synchronization with another process.

References: [util-linux options](https://manpages.debian.org/bookworm/util-linux/fallocate.1.en.html), [Linux allocation semantics](https://manpages.debian.org/bookworm/manpages-dev/fallocate.2.en.html).
