---
name: rm
description: Remove one selected owned regular-file or symbolic-link entry with GNU rm on Linux. Use for exact artifact cleanup when a directory, dangling link, suppressed error or open descriptor changes what removal proves.
---

# Remove the exact owned artifact entry

Read this entire SKILL.md before acting. Require the identified disposable regular file or symlink, its verified owned parent and authority to remove that exact entry. All task instructions are inline. Finish with removal status and actual entry absence, including a dangling symlink; no recursive directory cleanup is covered.

Confirm rm --version for GNU coreutils. Define owned_path as the verified absolute artifact entry, with no trailing slash. Inspect its type and preserve any required content before removal:

~~~bash
rm -- "$owned_path"
status=$?
~~~

Keep stderr and check status. Default rm does not remove a directory; that failure is not a reason to add -r. -- ends option parsing, while quoting preserves the single selected pathname. Avoid globs or computed descendant lists for this one-entry task. A normal rm can prompt for a write-protected file under its documented terminal conditions; retain that outcome rather than treating silence as success.

Removing a symlink entry removes the link itself, not its referent. Verify that the selected entry is absent: a following existence test alone can also be false for a still-present dangling link, so include symlink metadata. A missing parent or denied inspection leaves verification unresolved. Concurrent changes require a new identity check before retrying.

A suppressed diagnostic can conceal failed removal, and -f deliberately hides missing-file failures. Removal unlinks this name; other hard links or open descriptors can keep the object alive. It is not secure erasure or proof that a process stopped. Account for an owned producer separately if it can recreate the artifact.

Reference: [GNU rm manual](https://www.gnu.org/software/coreutils/manual/html_node/rm-invocation.html).
