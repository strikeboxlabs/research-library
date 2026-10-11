---
name: veracrypt
description: Inspect and mount one owned VeraCrypt file container read-only using known credentials. Use when GUI defaults, mount identity or an unavailable filesystem obscures selected backup access.
---

# Read the selected owned container

Read this entire SKILL.md before acting. Require trusted installed VeraCrypt, one complete owned container copy, known password/PIM/keyfiles and the host's existing mounting capability. Select one fresh empty mount directory and preserve container identity. No conditional resources are required. Finish with observed volume/device/mount, selected-file access and unmount evidence or the specific unresolved prerequisite.

Check `veracrypt -t --version` and `veracrypt -t --help`; text mode must be the first option. Define `container` as its established absolute regular-file path and `mount_dir` as the intended empty directory outside executable search paths. Inspect existing mounts first:

~~~bash
veracrypt -t --list
~~~

Do not mount an already active copy again. For the selected read-only access:

~~~bash
veracrypt -t --mount --mount-options=ro "$container" "$mount_dir"
status=$?
veracrypt -t --verbose --list "$container"
~~~

Supply known sensitive values through prompts. Do not assume PIM0 or no keyfiles from a filename, and do not place passwords in argv. Check mutation/query statuses separately and confirm the listed container, virtual device, mount directory and protection. Inspect only intended files; mounting does not establish complete backup consistency or trust in its contents. Do not execute restored scripts.

A mapped volume with no mounted filesystem differs from failed password/header validation. Missing filesystem support, permissions and wrong PIM/keyfiles need their own diagnostics; do not reformat, restore headers or force a mount as routine repair.

Close selected readers and leave the mount directory, then unmount this volume only:

~~~bash
veracrypt -t --unmount "$container"
status=$?
veracrypt -t --list
~~~

Without a selected volume, unmount can affect every VeraCrypt mount. A busy failure leaves cleanup incomplete; confirm the selected mapping disappears rather than forcing unrelated users' mounts closed.

References: [Unix CLI](https://veracrypt.io/en/Command%20Line%20Usage%20for%20Unix.html), [option/selection implementation](https://github.com/veracrypt/VeraCrypt/blob/master/src/Main/CommandLineInterface.cpp).
