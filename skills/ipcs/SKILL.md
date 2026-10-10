---
name: ipcs
description: Inspect Linux System V shared-memory metadata and distinguish keys, segment IDs, permissions, process context and incomplete namespace visibility during a local audit.
---

# Inspect shared-memory metadata

Use util-linux `ipcs` when a reviewed program calls `shmget`/`shmat`, or logs a System V shared-memory key. This inspects metadata; it does not read or modify segment contents. Check `ipcs --version` because other implementations differ.

~~~bash
ipcs -m
~~~

Find the relevant row using the observed key and capture time. A key is the lookup input to `shmget`; the returned `shmid` is the segment identifier. Neither is the attached virtual address. Define `shmid` from the current table's ID column, then inspect:

~~~bash
ipcs -m -i "$shmid"
ipcs -m -c
ipcs -m -p
ipcs -m -t
~~~

Keep creator/owner, PID and time views separate: only the last output-format option takes effect. Correlate the selected ID across them, accounting for removal and recreation between calls. For shared memory, the last-operation PID concerns attach/detach, not necessarily the last writer. PIDs can be reused; metadata alone cannot prove which process changed a value.

## Interpret permissions and missing results

An **illustrative** row with owner `root`, permissions `666` and size `1024` describes a root-owned 1 KiB segment whose mode grants read/write to owner, group and others. Root ownership does not restrict the other permission classes. Namespace, process credentials and additional security controls still affect actual access.

When reviewing `shmget(key, size, flags)`, separate creation flags from the low nine permission bits. On Linux, `0x3b6` is `IPC_CREAT | 0666`; it is not a file's sticky-bit mode. Without `IPC_EXCL`, an existing segment for that key can be reused. A random key provides no substitute for access control. Check observed metadata before assuming a newly created segment or inferring its current mode from source alone.

An empty table applies to the current IPC namespace at that moment. Containers can have a different namespace. If `/proc/sysvipc` is unavailable, ipcs falls back to calls that omit objects the caller cannot read. POSIX shared-memory files are a different facility. Zero attachments or a deletion marker is lifecycle evidence, not permission to remove an object; this workflow does not call `ipcrm` or attach to a segment.

Resolve platform details with [ipcs](https://man7.org/linux/man-pages/man1/ipcs.1.html), [shmget](https://man7.org/linux/man-pages/man2/shmget.2.html) and [IPC namespaces](https://man7.org/linux/man-pages/man7/ipc_namespaces.7.html).
