---
name: mount-nfs
description: Mount a selected NFS export read-only on Linux with mount.nfs, inspect effective options and diagnose version, identity or locking failures. Use for bounded file inspection without confusing an export advertisement with access.
---

# Inspect a selected NFS export

This uses the nfs-utils `mount.nfs` helper through `mount -t nfs`, kernel NFS support and mount privileges. It creates local mount state. Define `export` as the verified `server:/export/path`, `mountpoint` as a dedicated existing empty directory with no mount on it, and `nfs_version` as the intended supported version, such as `3` or `4.1`. NFSv4 paths are relative to the server's exported namespace and may differ from its physical paths.

~~~bash
mount.nfs -V
sudo mount -t nfs "$export" "$mountpoint" -o "ro,nosuid,nodev,noexec,vers=$nfs_version"
findmnt --mountpoint "$mountpoint" -o TARGET,SOURCE,FSTYPE,OPTIONS
~~~

Require successful mounting and an exact matching source/target with `ro` before reading. A failed mount leaves the ordinary directory underneath; an empty directory is not evidence of an empty export. Inspect the effective version and security flavor too. If `vers` is omitted, Linux normally negotiates down from its highest supported version; do not assume the version from an unrelated RPC banner. A server requiring Kerberos needs the appropriate identity and `sec=` configuration; retrying with weaker security is not an authentication fix.

For one requested artifact, define `relative_file` as its selected path within the mount and `local_copy` as a new absolute destination outside it:

~~~bash
stat -- "$mountpoint/$relative_file"
cp -- "$mountpoint/$relative_file" "$local_copy"
~~~

Preserve source path, size and copy errors. An NFS mount is not a point-in-time snapshot; concurrent changes can invalidate a copied archive or database. Inspect an archive's member list locally before extraction. `noexec` does not prevent an interpreter from reading a script; mounting is not permission to execute retrieved content.

For access denied, separate mount/export policy from per-file permission, numeric UID/GID or Kerberos mapping and root squashing. Client root need not be server root: default root squashing maps UID/GID zero to an anonymous identity. A broad export advertisement does not settle those controls.

Do not copy `nolock` routinely. For NFSv2/3 it disables the NLM sideband; locks then coordinate only applications on that client. It does not grant file access, and NFSv4 integrates locking differently. Default hard mounts can keep retrying during an outage; `soft` changes failure semantics and can risk data integrity. Diagnose connectivity/version/locking before changing these options.

After local readers leave the mount, use `sudo umount "$mountpoint"` and confirm the exact mount is absent. A busy mount needs open-file/current-directory investigation; lazy detachment is not proof all references are released.

Consult [mount.nfs](https://man7.org/linux/man-pages/man8/mount.nfs.8.html), [NFS version and locking options](https://man7.org/linux/man-pages/man5/nfs.5.html), and [export identity mapping](https://man7.org/linux/man-pages/man5/exports.5.html) for the failing layer.
