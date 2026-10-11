---
name: touch
description: Create a selected empty local marker or update access/modification timestamps with GNU touch. Use when file existence, symlink handling or displayed times could be mistaken for content or writer evidence.
---

# Establish what the marker or timestamp means

Read this entire SKILL.md before acting. Choose creation versus timestamp update, establish the exact owned path and preserve prior metadata when restoration matters. No conditional resources are required. Finish with status, observed file type/size/timestamps and the intended result; a name or timestamp alone does not establish file provenance or a shared host namespace.

Check `touch --version` for GNU coreutils. Define `marker` as a fresh selected absolute path in an existing owned directory; inspect the parent and confirm no file or symbolic link already occupies that name. For an ordinary empty marker:

~~~bash
umask 077
touch -- "$marker"
status=$?
stat --format='%F %s %u:%g %n' -- "$marker"
~~~

Check touch's saved status and stat's own result. Expect the intended regular file with zero bytes and observed ownership; a failed touch or stat is not a successful marker. Touch creates a missing file but does **not** truncate an existing one: it normally updates access and modification times instead. A pre-check and creation are not atomic; use an exclusive-creation mechanism when another writer can race for that path. Do not use touch as a lock acquisition primitive.

Touch normally follows a symbolic link and updates its target. `-h` deliberately updates the link's own timestamps where supported; it does not make an unexpected link acceptable for file creation. `-c` suppresses creation of missing paths and can succeed without changing any file, so it is not an existence test.

For an explicitly intended timestamp update to an existing selected file, define `file` from the inspected path and use `touch -c -- "$file"`. Choose `-a` or `-m` when only access or modification time should change. Record before/after metadata and inspect errors. The inode status-change time can change as a consequence; touch cannot set a filesystem's creation time or arbitrarily choose ctime. Timestamp precision and access behavior depend on the filesystem.

An **illustrative** zero-byte marker seen through two established filesystem views supports a specific path correlation at that time. A basename, root-looking owner name or shared source device alone does not establish that both views belong to the same host or that a particular actor created it. Keep namespace/path mapping and numeric identity evidence separate. Remove only the owned marker when the task requires cleanup, then verify its absence; timestamp updates need their own agreed restoration evidence.

Reference: [GNU touch packaged manual](https://manpages.debian.org/bookworm/coreutils/touch.1.en.html).
