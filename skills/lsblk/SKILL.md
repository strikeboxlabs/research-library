---
name: lsblk
description: Inspect Linux block-device relationships and mountpoint metadata with util-linux lsblk. Use when a disk, partition or alternate mount view is being confused with the filesystem currently visible at a path.
---

# Inspect block devices and their mount views

Read this entire SKILL.md before acting. Confirm `lsblk --version` and supported columns in `lsblk --help`; retain status, device relationships and mount context. No conditional resources are required. This read-only inventory does not mount devices or establish host/container provenance.

~~~bash
lsblk --json --bytes --output NAME,TYPE,MAJ:MIN,SIZE,FSTYPE,MOUNTPOINTS
status=$?
~~~

Use `TYPE` and parent/child relationships to distinguish a whole disk from its partition; do not substitute the parent's name for the observed mounted child. Explicit columns avoid relying on changing defaults. `SIZE` is device capacity, not free filesystem space. `MOUNTPOINTS` can contain several views; older implementations may only support `MOUNTPOINT`, which loses that coverage.

Missing filesystem fields can reflect incomplete udev/access data. Retain that gap rather than inferring an unformatted device. Mount associations describe the observer's context and can change; visible devices alone do not prove escape into another host namespace. Before an authorized mount decision, establish the exact filesystem/device and existing mount view separately. Finish with the supported relationship and unresolved context.

Reference: [util-linux lsblk manual](https://manpages.debian.org/bookworm/util-linux/lsblk.8.en.html).
