---
name: setfacl
description: Apply a selected POSIX ACL change to one owned regular Linux file and verify effective rights. Use when a named-user grant, automatic mask recalculation or a partial filesystem failure changes the intended permission result.
---

# Change one selected owned file's ACL

Read this entire SKILL.md before acting. Require the actual owned regular file, authorized grantee/permission change, ACL-capable filesystem and installed setfacl/getfacl. Preserve its prior ACL, review the computed mask, apply only the selected change and verify effective rights. No conditional resources are required. Finish with before/after ACL and actual access evidence or the unresolved prerequisite.

Confirm `setfacl --version` and local help. Define `file` as the established absolute file path without unexpected symlinks in it or its parents, `grantee_uid` as the intended validated numeric UID, and `acl_before` as a fresh private backup path. Require stable owned path components; a lexical prefix or `test -f` does not establish containment when a path resolves through links. Ownership or the appropriate existing capability is needed to change an ACL.

Preserve the complete prior permission record:

~~~bash
umask 077
(set -C; unset POSIXLY_CORRECT; getfacl -p -n -- "$file" >"$acl_before")
status=$?
~~~

Stop on backup failure. The capture subshell unsets `POSIXLY_CORRECT`, which would suppress special-bit flags in getfacl's headers. Review the owner, group, named entries, mask and flags; a restore record missing flags can clear special bits. For the requested named-user read grant, preview the computed ACL:

~~~bash
setfacl --test -m "u:$grantee_uid:r" -- "$file"
status=$?
~~~

`-m` modifies entries; `--set` replaces the ACL. Default mask recalculation can broaden the effective rights of other existing named/group entries. If that exceeds the requested change, resolve the intended mask before applying rather than assuming only this user's rights change. `-n` preserves an existing mask but can leave the new grant ineffective.

After a successful preview matching the intended complete ACL:

~~~bash
setfacl -m "u:$grantee_uid:r" -- "$file"
status=$?
getfacl -p -n -e -- "$file"
~~~

Check mutation and read-back status separately. The mask limits named users and group entries, not the owner/other entries. Parent traversal, mount and security policy still matter; an ACL row alone is not proof that the grantee opened the file. Verify the requested read through the established account context when that result is required.

On a filesystem lacking suitable ACL support, a nonzero result can accompany partial mode-bit changes; inspect the resulting permissions instead of assuming rollback. Do not recursively retry or add privilege to repair an unidentified failure.

If restoring the prior state is part of the task, review this backup's exact path and current file identity first. `setfacl --test --restore="$acl_before"` previews restoration; `setfacl --restore="$acl_before"` applies it. Restore can also attempt owner/group and special-bit restoration from headers, so preserve the complete record and check every diagnostic/read-back. Do not replay a backup onto a different file or overwrite intervening legitimate changes.

References: [setfacl modification, mask and restore semantics](https://manpages.debian.org/bookworm/acl/setfacl.1.en.html), [getfacl effective-rights and backup fields](https://manpages.debian.org/bookworm/acl/getfacl.1.en.html).
