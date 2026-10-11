---
name: cryptsetup
description: Inspect, test a known passphrase and unlock existing LUKS image copies on Linux. Use when separating credential verification, device mapping and filesystem mounting, or avoiding journal writes during inspection.
---

# Inspect an existing encrypted image

Read this entire SKILL.md before acting. Require an intact selected image copy, a known passphrase for verification/unlocking and authority for the exact operations. Select metadata inspection, known-passphrase verification or mapped filesystem inspection below. Mapping/mounting also requires Linux device-mapper support and the listed inspection/mount tools. Finish with the selected result and any created mount/mapping cleanup; a missing prerequisite or failed step remains unresolved.

These sudo examples assume those precise commands/options are permitted. A grant for one executable/subcommand, mapper name or relative mountpoint does not authorize arbitrary status, probe, close or mount arguments. Establish an allowed recovery path before creating state; do not weaken read-only handling simply to fit a different grant.

Define `image` as an intact local working copy, not the original evidence or a guessed device. Inspect without changing keyslots:

~~~bash
cryptsetup --version
cryptsetup isLuks "$image" && cryptsetup luksDump "$image"
~~~

Retain the version, cipher, keyslot and data-offset information. `isLuks` failure may mean a whole-disk image containing partitions, a detached header, a different format or truncation; it does not identify a bad password. Resolve the actual layout before choosing offsets. `luksDump` normally reports metadata; do not add volume-key dumping options for ordinary inspection.

To verify one known passphrase without creating a mapping, after confirming the actual LUKS image:

~~~bash
cryptsetup open --type luks --test-passphrase --tries 1 "$image"
~~~

Supply that passphrase at the prompt and retain status/diagnostics. No mapping name is required for this test. LUKS2 can attempt configured tokens first: success without the passphrase prompt does not prove that particular passphrase. Retain that distinction, or use the task's existing protected key-file mechanism and matching installed options when the specific value must be tested. A successful verification does not mount a filesystem or prove its health; failure can reflect the wrong image/header or an access/format error as well as a nonmatching passphrase. A VirtualBox disk-container password does not automatically unlock a separate inner LUKS volume. Do not place the value in argv or copy a shell word-splitting loop from a walkthrough.

For a known passphrase, define `mapping` as an unused device-mapper name and `mountpoint` as a dedicated empty directory. Opening creates local mapping state, not a mounted filesystem:

~~~bash
sudo cryptsetup open --type luks --readonly "$image" "$mapping" &&
sudo cryptsetup status "$mapping" &&
sudo blkid -p "/dev/mapper/$mapping"
~~~

Enter the passphrase at the prompt. Stop on opening failure; do not accidentally inspect a pre-existing mapping with the same name. Mapper names are case-sensitive: `Volume` and `volume` are different paths. Check that status names the intended backing image and reports read-only access. Identify the inner filesystem before mounting. **Only for an identified ext4 filesystem:**

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
