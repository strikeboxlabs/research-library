---
name: mount-cifs
description: Mount a selected SMB share for Linux file inspection or an intended owned write task with mount.cifs. Use for credential, timestamp and dialect failures or to distinguish local ownership/mount options from server permissions.
---

# Mount a selected SMB share

Read this entire SKILL.md before acting. Require the exact selected share, a dedicated empty mountpoint, intended authentication and Linux CIFS support/mount privileges. Follow the mount verification and unmount steps below; for a remote timestamp question, also read that section. Finish with the observed share/options and requested file evidence, then confirmed unmount, or identify the failed stage.

A mount is useful when several local programs need normal filesystem access. A large file alone does not require one: an SMB client can transfer it directly. `mount.cifs` needs the cifs-utils helper, kernel CIFS support and mount privileges; it creates host mount state.

Define `share` as the observed `//server/share`, `mountpoint` as a dedicated empty directory, and `credentials` as an existing private absolute file containing `username=`, `password=` and, when required, `domain=` on separate lines. Keep this file out of logs and repositories. For file inspection:

~~~bash
mount.cifs -V
sudo mount -t cifs "$share" "$mountpoint" -o "ro,nosuid,nodev,noexec,credentials=$credentials"
findmnt --mountpoint "$mountpoint" -o TARGET,SOURCE,FSTYPE,OPTIONS
~~~

Require successful mounting and verify the exact mountpoint, share and `ro` option before reading. Otherwise an ordinary directory underneath a failed mount can be mistaken for an empty share. Do not mount over a populated working directory.

For an intended write task on the selected owned share, replace `ro` with `rw` and verify that option instead; retain the other isolation and authentication choices. `rw` permits the client to attempt writes but does not grant server-side directory rights. A successful timestamp update on an existing file does not establish fresh-file creation or deletion permission. Use a fresh task-specific name in the selected directory, retain errors and remove only the file this task created before unmounting; do not enumerate every directory into an unquoted shell loop.

For interactive authentication, use `username=` and optional `domain=` instead of the credentials-file option; the helper prompts when no password is supplied otherwise. Commas in passwords make inline mount options ambiguous. `guest` suppresses the password prompt; the server still decides whether guest access is permitted.

`uid=` and `gid=` affect local ownership presentation when applicable, not the server's authorization. A successful share listing does not guarantee permission on every child. Diagnose authentication, share naming, kernel support and dialect negotiation separately. Set `vers=` only from known server/client compatibility; do not blindly downgrade to SMB1 or remove signing/encryption requirements.

Finish local readers and run `sudo umount "$mountpoint"`. A busy mount needs investigation of open files/current directories; lazy unmount is not proof that all users have released it. Confirm the mount is absent before removing a temporary credentials file.


## Read remote modification time without confusing it with download time

After verifying the mount above, define `remote_file` as an observed regular file beneath that mountpoint. With GNU coreutils:

~~~bash
date -u -r "$remote_file" '+%Y-%m-%dT%H:%M:%SZ'
date -r "$remote_file" '+%s'
~~~

`-r` reads last modification time, not creation time or the current clock. A downloader may preserve or replace timestamps; inspecting the acquired local copy alone does not settle the remote value. Record the share/path and acquisition time with the observation. Attribute caching and concurrent server changes mean a mount is not an immutable snapshot.

If source code seeds a generator before writing the output, output mtime supplies a candidate time, not proof of the exact seed: execution delay, timestamp precision and subsequent writes can differ. `serverino` selects server-provided file identifiers; it neither repairs timestamps nor asks the server to generate new unique identifiers. `sec=ntlmsspi` forces signing in addition to NTLMSSP authentication; it does not request SMB encryption. `vers=3.0` pins an SMB dialect, not a timestamp-preservation mode.

Resolve metadata and option differences with the [cifs-utils manual source](https://github.com/piastry/cifs-utils/blob/master/mount.cifs.rst) and [GNU date implementation/help](https://github.com/coreutils/coreutils/blob/master/src/date.c).
