---
name: mknod
description: Create one fresh owned Linux FIFO with GNU mknod. Use when a named pipe is being confused with a regular file, device node or persisted data, and identify blocking/cleanup prerequisites.
---

# Create the intended FIFO entry

Read this entire SKILL.md before acting. Require a trusted owned parent directory, a fresh exact absolute pathname and a separately selected local reader/writer task. All instructions are inline. Finish with creation status, observed FIFO type/mode and its tracked disposition; creating it does not start a producer or consumer.

Confirm GNU mknod with mknod --version; shell implementations can differ. Define fifo as a new pathname beneath that parent, without a trailing slash or any existing entry, including a dangling link. For a private FIFO:

~~~bash
umask 077
mknod --mode=600 -- "$fifo" p
status=$?
~~~

Check status/stderr and inspect the exact entry's type, owner and mode with the selected filesystem metadata reader. Type p creates a FIFO and takes no major/minor operands. Types b/c/u create device nodes and are different tasks; do not add them or escalate privileges to repair an ordinary FIFO failure. An existing name remains a collision to resolve, not permission to replace it.

A FIFO has no persisted file contents; the entry names a kernel pipe used by open processes. Ordinary opening can wait for the other end, and writes can receive SIGPIPE when no reader remains. Choose both owned endpoints and their lifetime budget before using it. A path's existence or zero reported size does not establish completed transfer. Do not read an unknown FIFO with a regular-file checksum/cat procedure to discover its contents.

When the selected exchange ends, stop/close its tracked endpoints and remove only the verified owned FIFO entry. Unlinking a name is separate from closing handles already held by processes. Do not reuse a service/script pathname or replace another process's entry as part of this creation task.

References: [GNU mknod options](https://manpages.debian.org/bookworm/coreutils/mknod.1.en.html) and [Linux FIFO semantics](https://manpages.debian.org/bookworm/manpages/fifo.7.en.html).
