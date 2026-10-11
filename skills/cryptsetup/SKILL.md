---
name: cryptsetup
description: Inspect and unlock existing LUKS image copies on Linux. Use when identifying LUKS versions, separating decryption from filesystem mounting, or avoiding journal writes during inspection.
---

# Inspect an existing encrypted image

Read this entire SKILL.md before acting. Require an intact selected image copy, known passphrase for unlocking, Linux device-mapper support, the inspection/mount tools below and authority for the exact operations. Inspect the layout, open a fresh mapping, verify its backing/access and inner filesystem, then perform the selected read and cleanup. Finish with read/result evidence plus actual mount/mapping cleanup; a missing prerequisite or failed opening remains unresolved.

These sudo examples assume those precise commands/options are permitted. A grant for one executable/subcommand, mapper name or relative mountpoint does not authorize arbitrary status, probe, close or mount arguments. Establish an allowed recovery path before creating state; do not weaken read-only handling simply to fit a different grant.

Define `image` as an intact local working copy, not the original evidence or a guessed device. Inspect without changing keyslots:

~~~bash
cryptsetup --version
cryptsetup isLuks "$image" && cryptsetup luksDump "$image"
~~~

Retain the version, cipher, keyslot and data-offset information. `isLuks` failure may mean a whole-disk image containing partitions, a detached header, a different format or truncation; it does not identify a bad password. Resolve the actual layout before choosing offsets. `luksDump` normally reports metadata; do not add volume-key dumping options for ordinary inspection.

For a known passphrase, define `mapping` as an unused device-mapper name and `mountpoint` as a dedicated empty directory. Opening creates local mapping state, not a mounted filesystem:

~~~bash
sudo cryptsetup open --type luks --readonly "$image" "$mapping" &&
sudo cryptsetup status "$mapping" &&
sudo blkid -p "/dev/mapper/$mapping"
~~~

Enter the passphrase at the prompt. Stop on opening failure; do not accidentally inspect a pre-existing mapping with the same name. Check that status names the intended backing image and reports read-only access. Identify the inner filesystem before mounting. **Only for an identified ext4 filesystem:**

~~~bash
sudo mount -t ext4 -o ro,noload,nosuid,nodev,noexec "/dev/mapper/$mapping" "$mountpoint" &&
findmnt --mountpoint "$mountpoint"
~~~

Plain `mount -o ro` can still replay an ext3/ext4 journal. `noload` avoids that replay; a dirty filesystem may consequently present inconsistent data. Other filesystems need their own options. A filesystem error after successful unlocking is not automatically a wrong passphrase; do not repair the original to make the error disappear.

After readers leave the mount, unmount successfully before closing the mapping:

~~~bash
sudo umount "$mountpoint" && sudo cryptsetup close "$mapping"
~~~

Check busy-mount errors instead of forcing cleanup. `luksFormat`, key changes and header restoration are separate modifying operations.

See upstream [open](https://gitlab.com/cryptsetup/cryptsetup/-/blob/main/man/cryptsetup-open.8.adoc), [luksDump](https://gitlab.com/cryptsetup/cryptsetup/-/blob/main/man/cryptsetup-luksDump.8.adoc) and [mount read-only semantics](https://github.com/util-linux/util-linux/blob/master/sys-utils/mount.8.adoc).
