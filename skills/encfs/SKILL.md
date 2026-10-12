---
name: encfs
description: Mount an existing owned EncFS backup with its matching configuration and a known password, read the plaintext view and unmount it. Use when configuration selection, FUSE support or an unexpected creation prompt obscures recovery.
---

# Read an existing EncFS backup

Read this entire SKILL.md before acting. Require trusted EncFS/FUSE support, an existing owned ciphertext working copy, its complete matching configuration, the known password and a fresh empty owned mountpoint. Finish with observed mount/read results and verified unmounting. Missing configuration, password or FUSE support leaves recovery unresolved.

Check the installed version/help. Set `encfs_bin` to the verified executable, `encrypted_dir` and `config` to absolute matching paths, and `mountpoint` to an established empty unmounted directory. On a version supporting these options:

~~~bash
"$encfs_bin" --config "$config" "$encrypted_dir" "$mountpoint" -- -o ro
~~~

Supply the known password at the prompt, keeping it out of arguments and logs. Stop if prompted to create a new filesystem: missing configuration or wrong paths must not be repaired by initializing over the backup. The configuration contains the encrypted master key; reconstructing settings alone cannot replace it.

EncFS v6 configuration selection uses `ENCFS6_CONFIG`, not `ENCFS5_CONFIG`; prefer the explicit supported config option. Confirm the actual mount in the current namespace and read a selected ordinary file before claiming plaintext recovery. A read-only FUSE view does not make the backing ciphertext immutable or establish archival completeness or authenticity. Avoid sharing the mount with `allow_other`.

After readers have finished:

~~~bash
"$encfs_bin" --unmount "$mountpoint"
~~~

Check status and that this mount disappeared. Busy or failed cleanup remains unresolved; target only the mount established for this task.

References: [EncFS options and configuration](https://manpages.debian.org/bookworm/encfs/encfs.1.en.html), [FUSE mount options](https://manpages.debian.org/bookworm/fuse/mount.fuse.8.en.html).
