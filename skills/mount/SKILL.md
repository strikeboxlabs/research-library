---
name: mount
description: Attach an identified block filesystem in the current Linux mount namespace for selected reads or authorized file changes. Diagnose exposed container devices, read-only journal effects, mount attribution and busy cleanup.
---

# Mount a selected filesystem

Read this entire SKILL.md before acting; reuse complete current context. Identify the source filesystem, execution/mount namespace, requested access and free mountpoint before mounting. Finish with the selected file/read/change plus actual mount/result and cleanup status; UID 0, a device name or an existing directory is insufficient evidence of host-root access.

`mount` changes the executing process's mount namespace and needs the applicable authority (normally CAP_SYS_ADMIN), device access and filesystem support. Container root can lack these; user namespaces, device cgroups, AppArmor/SELinux and seccomp can still deny the operation. A client executing through a remote container daemon operates on that daemon's context, not automatically its local workstation.

Inspect `mount --version` and existing mounts. `mount` without operands displays mounts; for precise attribution use `findmnt --kernel --output TARGET,SOURCE,FSTYPE,FSROOT,OPTIONS` or `/proc/self/mountinfo`. One device backing several file mounts does not reveal each bind source or establish the host root. A directory named `root` is not proof either. Correlate namespace, actual device/UUID/source mapping and filesystem contents before reporting that attribution.

Define `device` as the identified accessible block-device path, `fstype` as its verified filesystem, and `mountpoint` as an existing empty absolute directory with no current mount. Verify `test -b "$device"` and the exact mountpoint state before proceeding. For example, `findmnt --kernel --mountpoint "$mountpoint"` returning no match differs from a diagnostic error; inspect status/messages. Mounting on an occupied directory hides its existing contents without deleting them and can lead to modifying the wrong tree.

Choose `options` for the task:

| Purpose | Consequence |
|---|---|
| Ordinary selected read, `ro` | Denies file writes through this mount; ext3/ext4 may still replay a dirty journal. It is not a forensic no-write guarantee. |
| Compatible ext3/ext4 snapshot inspection, `ro,noload` | Avoids loading/replaying the journal; un-replayed state may be inconsistent. Prefer a coherent snapshot and retain that limitation. Do not apply filesystem-specific options to an unidentified device. |
| Explicitly authorized file change, `rw` | Allows mount-layer writes; actual permissions/identity mapping still apply. Preserve the selected file's original bytes/metadata and verify the requested change. |

Do not independently remount a live filesystem or repair its journal merely to make evidence readable. A second mount of an already active filesystem can share its superblock; choose an existing suitable view or coordinated snapshot when possible. A readonly second view does not make other writers stop.

In the established privileged context, with the chosen source/type/options:

~~~bash
mount -t "$fstype" -o "$options" -- "$device" "$mountpoint"
findmnt --kernel --mountpoint "$mountpoint" --output TARGET,SOURCE,FSTYPE,FSROOT,OPTIONS
~~~

Check mount's immediate exit status before interpretation; use `/proc/self/mountinfo` if the optional `findmnt` binary is absent. An **illustrative** row `TARGET=/mnt/selected SOURCE=/dev/vdb1 FSTYPE=ext4 FSROOT=/ OPTIONS=rw,...` shows that filesystem's root at this namespace's mountpoint; it does not establish which physical host owns it. Select the requested relative file under this verified tree. Record successful actual reading or change/read-back, not merely `ls` showing its mode. A file change can affect the source host despite the process remaining in a container.

| Failure | Useful next check |
|---|---|
| `Operation not permitted` | Effective capability, user namespace, LSM/seccomp and device policy; do not disable controls to guess. |
| Missing/not-block node | Actual exposed device and expected namespace. A device mentioned in mount output need not have an accessible node here. |
| Wrong filesystem/bad superblock | Device/type/coherent snapshot and diagnostics; do not run repair on the original as an inspection fallback. |
| Read-only/file permission denial | Actual mount options and effective identity/ACLs. `rw` metadata alone does not promise a writable file. |

After the selected task, leave the mounted tree, close owned open file handles and unmount **this created mountpoint**, not a device shared by multiple mounts:

~~~bash
cd /
umount -- "$mountpoint"
~~~

Verify the exact mount is gone and preserve errors. `busy` can mean another process's cwd/open files or submounts; identify the blocker before retrying. Lazy unmount detaches the name while references can remain, and force is not a generic busy-filesystem fix. Do not unmount pre-existing service mounts. Exiting a container shell alone need not remove a mount used by other processes.

See [mount options](https://github.com/util-linux/util-linux/blob/master/sys-utils/mount.8.adoc), [umount lifecycle](https://github.com/util-linux/util-linux/blob/master/sys-utils/umount.8.adoc) and [kernel mountinfo](https://man7.org/linux/man-pages/man5/proc_pid_mountinfo.5.html).
