---
name: losetup
description: Attach a saved disk image to a Linux loop device for selected filesystem inspection and detach the owned mapping afterward. Use when an image needs a block-device view or partition discovery.
---

# Map the image and retain its identity

Read this entire SKILL.md before acting. Identify the saved image, required access and existing mappings. Finish with the backing-file/device mapping, requested inspection and cleanup status; attachment alone is not a completed filesystem read.

Check `losetup --version` and `--help`. Define `image` as the absolute working-copy path. In the context with loop-device authority:

~~~bash
losetup --list
losetup --associated "$image"
~~~

If an existing mapping is found, inspect its ownership/options before reuse; do not detach it as your own. For a new read-only mapping:

~~~bash
loop_device=$(losetup --find --show --read-only --partscan "$image")
losetup --list "$loop_device"
~~~

Check setup status before using the returned device. `--partscan` parses a partition table; a floppy-style whole-filesystem image can have no partition nodes. Sector size affects parsing. Identify the filesystem/device before mounting; do not invent a partition suffix. Use read-only filesystem options and account for journal handling.

After unmounting any mounts created for this mapping:

~~~bash
losetup --detach "$loop_device"
losetup --associated "$image"
~~~

Detachment can be deferred while references remain. Preserve unresolved cleanup. Never use detach-all for one image. No available loop device or denied capability is a missing prerequisite, not corrupt-image evidence. See the [util-linux manual](https://github.com/util-linux/util-linux/blob/master/sys-utils/losetup.8.adoc).
