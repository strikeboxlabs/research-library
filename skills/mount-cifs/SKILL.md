---
name: mount-cifs
description: Mount an SMB share for read-only Linux file inspection with mount.cifs. Use when choosing a kernel mount, handling credentials and dialect failures, or distinguishing local ownership from server permissions.
---

# Mount a selected SMB share

A mount is useful when several local programs need normal filesystem access. A large file alone does not require one: an SMB client can transfer it directly. `mount.cifs` needs the cifs-utils helper, kernel CIFS support and mount privileges; it creates host mount state.

Define `share` as the observed `//server/share`, `mountpoint` as a dedicated empty directory, and `credentials` as an existing private absolute file containing `username=`, `password=` and, when required, `domain=` on separate lines. Keep this file out of logs and repositories. For file inspection:

~~~bash
mount.cifs -V
sudo mount -t cifs "$share" "$mountpoint" -o "ro,nosuid,nodev,noexec,credentials=$credentials"
findmnt --mountpoint "$mountpoint" -o TARGET,SOURCE,FSTYPE,OPTIONS
~~~

Require successful mounting and verify the exact mountpoint, share and `ro` option before reading. Otherwise an ordinary directory underneath a failed mount can be mistaken for an empty share. Do not mount over a populated working directory.

For interactive authentication, use `username=` and optional `domain=` instead of the credentials-file option; the helper prompts when no password is supplied otherwise. Commas in passwords make inline mount options ambiguous. `guest` suppresses the password prompt; the server still decides whether guest access is permitted.

`uid=` and `gid=` affect local ownership presentation when applicable, not the server's authorization. A successful share listing does not guarantee permission on every child. Diagnose authentication, share naming, kernel support and dialect negotiation separately. Set `vers=` only from known server/client compatibility; do not blindly downgrade to SMB1 or remove signing/encryption requirements.

Finish local readers and run `sudo umount "$mountpoint"`. A busy mount needs investigation of open files/current directories; lazy unmount is not proof that all users have released it. Confirm the mount is absent before removing a temporary credentials file.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Arkham p. 4. Sources: [cifs-utils mount.cifs manual](https://man7.org/linux/man-pages/man8/mount.cifs.8.html), [util-linux mount manual](https://github.com/util-linux/util-linux/blob/master/sys-utils/mount.8.adoc).
