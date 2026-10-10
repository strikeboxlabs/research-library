---
name: cp
description: Copy a selected Linux directory with deliberate path and metadata handling, and diagnose why copied sensitive files have different permissions or ownership.
---

# Copy paths and preserve the intended metadata

This guidance targets GNU `cp`; check `cp --version`. Use it for a bounded, reviewed directory copy. A live application's files may change during traversal; cp alone does not produce a consistent database or application snapshot.

Define `source` as the selected real directory without a trailing slash and `dest` as a fresh path beneath a trusted existing parent. Keep the destination outside the source tree:

~~~bash
(
  umask 077
  mkdir -m 700 -- "$dest" && cp -a -- "$source" "$dest/"
)
~~~

The copy runs only if the destination directory was newly created. It creates `dest/basename(source)/`, including dotfiles. An existing destination is a reason to inspect the intended layout, not to remove it automatically. Copying `"$source"/.` instead places the contents directly in the destination, but archive mode can then replace that destination directory's metadata too. Keep the separate private outer directory when access containment matters.

`-a` copies recursively, retains symlinks as links and requests metadata preservation. The private outer directory limits access while preserving source modes inside it; umask alone does not override preserved modes. Review symlinks and special files before treating the result as ordinary data.

For a selected regular file, define `original_file` and `copied_file` as the corresponding paths:

~~~bash
stat -c '%n uid=%u gid=%g mode=%a type=%F' -- "$original_file" "$copied_file"
cmp -- "$original_file" "$copied_file"
~~~

`cmp` status 0 means byte equality at comparison time; 1 means different data and higher values mean an error. Ownership/mode comparisons answer a different question. Check ACLs, extended attributes or security labels separately when they govern the task. Archive mode can suppress failures to preserve xattrs/SELinux context, so status zero alone does not establish full metadata fidelity. Permission/filesystem failures can leave a partial destination; inspect diagnostics before reusing it.

## Explain a permission change

| Copy condition | Consequence and next check |
|---|---|
| `-p` | Preserves mode, ownership and timestamps; this is narrower than archive mode. Verify the actual destination attributes. |
| Default copy to a new file | Uses source permissions, subject to umask/default ACL rules; recursion alone does not imply broader access. |
| `--no-preserve=mode` to a new regular file | GNU cp uses default read/write permissions filtered by umask. Illustratively, with umask 022 and no additional access constraints, a source mode 0600 can become 0644. |
| Existing destination without preservation | Its existing permissions normally remain. `--remove-destination` unlinks it first, so recreation can change this outcome. |

Do not add `--no-preserve=mode,ownership` to a sensitive backup simply to suppress errors. Establish the intended owner and access policy, then verify both the copied object and its parent path. See the [GNU cp manual](https://www.gnu.org/software/coreutils/manual/html_node/cp-invocation.html) for preservation and platform exceptions.
