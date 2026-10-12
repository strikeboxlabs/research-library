---
name: wimmount
description: Mount one acquired WIM image read-only on Linux with wimlib, inspect selected nonsecret files and unmount the owned view. Use when image indexes, FUSE support or Windows metadata make archive contents ambiguous.
---

# Open one WIM image as a read-only view

Read this entire SKILL.md before acting. Require the acquired WIM, selected image index, Linux wimlib with FUSE support and an empty private owned mount directory. Finish with the selected image/path evidence, mount result and verified unmount; missing resources or failed reads leave that evidence incomplete. No conditional resources are required.

Inspect installed `wimmount --help`, `wiminfo --help` and `wimunmount --help`; installations may instead expose `wimlib-imagex mount/info/unmount`. These are different subcommands of the same library, not generic disk mounts. Define `wim_file` as the absolute intact acquired file:

~~~bash
wiminfo "$wim_file"
~~~

Without rename/property/boot options this displays metadata rather than changing the WIM. Select an actual 1-based `image_index` from that inventory; omission works only for a single-image WIM. A `.wim` filename alone does not identify its image, Windows installation or acquisition date. WIM is a file-based image archive, not necessarily an entire disk with partitions.

Define `mount_dir` as an existing empty private directory with no active mount. Preserve the acquired file's identity/digest before mounting:

~~~bash
wimmount "$wim_file" "$image_index" "$mount_dir" --check
status=$?
~~~

`wimmount` is read-only; `wimmountrw` is a separate write workflow. `--check` verifies extra integrity information if present, not independent provenance or absence of corruption when it is absent. Check status/diagnostics and the actual mounted image before inspecting selected nonsecret files. Default mounting backgrounds a FUSE process; a quiet terminal does not identify its lifetime. Linux/FUSE availability, device access and mount permissions are prerequisites; do not repair failure by editing global FUSE settings or automatically adding sudo/allow-other.

The mounted Unix modes/owner are not the original Windows ACL: by default wimlib exposes files under the mounter with synthetic modes and limits other-user access. Windows security descriptors and some metadata are not exposed; EFS files can be visible without readable data. Named streams use a distinct interface. Symlinks/junctions can be translated, so inspect selected paths before following links. A denied/unavailable stream is not proof the archive lacks it. Do not execute acquired programs to identify them.

For an actual split WIM, select its first part and define `part_glob` for the known complete sibling parts; quote `--ref="$part_glob"` so wimlib performs its resource matching. Similarly numbered `.wim` files are not automatically split parts. Missing referenced resources leave selected file reads incomplete.

Close files and move working directories outside the owned view, then:

~~~bash
wimunmount "$mount_dir"
~~~

Verify the mount and its owned FUSE process are gone and the original WIM digest is unchanged. Busy/unmount errors require closing the identified handles; do not force an unrelated mount or add --commit. Unmounting this read-only view does not delete acquired files.

References: [wimlib mounting, metadata and cleanup](https://wimlib.net/man1/wimmount.html), [image inventory versus modification](https://wimlib.net/man1/wiminfo.html).
