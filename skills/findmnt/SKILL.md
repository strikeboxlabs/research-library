---
name: findmnt
description: Identify the filesystem backing a path and inspect mount roots in the current Linux namespace. Use when a container path, shared device name or read-write mount is being mistaken for proof of a host path or effective file access.
---

# Distinguish a path's filesystem from an exact mountpoint

Check `findmnt --version` and the available columns in `findmnt --help`. Define `path` as an existing absolute path in the namespace being examined:

~~~bash
findmnt --kernel --target "$path" --output TARGET,SOURCE,FSTYPE,FSROOT,OPTIONS
~~~

`--target` finds the covering filesystem, searching parent paths when necessary. It does not prove the selected path is itself a mountpoint. For that question, use an exact mountpoint query:

~~~bash
findmnt --kernel --mountpoint "$path" --output TARGET,SOURCE,FSTYPE,FSROOT,OPTIONS
~~~

No match can produce status 1, which also covers errors; inspect diagnostics before deciding the path has no separate mount. An unsupported column is a compatibility error, not absence of a mount. Explicit columns avoid relying on changing default output.

In an **illustrative** row with `TARGET=/root`, `SOURCE=/dev/vda1[/srv/worker-home]` and `FSROOT=/srv/worker-home`, the mount exposes a subtree of that filesystem at `/root` in this namespace. It does not establish that the host's own `/root` is exposed. Several mounts with the same source device can expose different subtrees.

Kernel mount information describes the process's view. `/proc/self/mountinfo` records the filesystem root and namespace-relative mountpoint separately; it is useful when formatted output omits needed detail. Filesystem-root paths are not automatically absolute paths in the daemon host's namespace. To establish a Docker bind source, correlate with the selected container's `Mounts` metadata from the correct daemon, when that access is already available. Without it, retain the source-path uncertainty.

`rw` permits writes at the mount layer; file permissions, ACLs, identity mappings and other controls still apply. This inspection neither mounts/remounts anything nor proves that a particular user can modify a file.

See [findmnt options](https://man7.org/linux/man-pages/man8/findmnt.8.html), [mountinfo fields](https://man7.org/linux/man-pages/man5/proc_pid_mountinfo.5.html) and the [FSROOT implementation](https://github.com/util-linux/util-linux/blob/master/misc-utils/findmnt.c).
