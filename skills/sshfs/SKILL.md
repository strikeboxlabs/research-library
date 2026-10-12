---
name: sshfs
description: Mount an owned SFTP directory for Linux file inspection with SSHFS and verify cleanup. Use when SSH login, FUSE access, local UID presentation and the remote account's file permissions are being confused.
---

# Inspect a selected SFTP directory through a mount

Read this entire SKILL.md before acting. Require trusted installed SSHFS/FUSE support, the exact owned SSH/SFTP account and directory, verified host key and an empty owned mountpoint. Follow connection, mount verification and unmount steps below. No conditional resources are required. Finish with the selected remote path, requested file evidence and confirmed unmount, or the failed stage.

Define `remote_spec` as the exact `user@host:/absolute/remote/path`, `ssh_port` as the intended port and `mountpoint` as a dedicated empty absolute directory owned by the mounting user. A shell login alone does not establish SFTP subsystem availability. Review the intended SSH client configuration/authentication; inherited ProxyCommand or other helpers can execute locally.

~~~bash
sshfs --version
sshfs -p "$ssh_port" "$remote_spec" "$mountpoint" -o ro,default_permissions,StrictHostKeyChecking=yes
findmnt --mountpoint "$mountpoint" -o TARGET,SOURCE,FSTYPE,OPTIONS
~~~

Use the intended credential prompt/agent and preserve connection diagnostics. Require the exact mount/source and read-only option before reading: after a failed mount, the underlying local directory is still present. The filesystem type is normally fuse.sshfs. Do not mount over existing work or infer success from directory existence. Foreground `-f` keeps the process in its tracked terminal; use another terminal for inspection and unmount. `-d` adds debugging and should have private bounded capture when needed.

SFTP operations use the remote authenticated account. Local UID zero does not make that connection a remote-root session. `default_permissions` adds local kernel permission checks; it does not grant remote rights. Without it, remote server policy still applies. `allow_other` admits additional local users to this connection and depends on FUSE policy; it is unnecessary for single-user inspection. Do not change `/etc/fuse.conf` merely to retry this task.

Ownership displayed locally can depend on mapping options. A file created through an intended writable SFTP mount is created through that authenticated remote account, rather than inheriting arbitrary remote privileges from a local writer's UID. `ro` prevents the writes in this inspection task. Preserve local metadata, remote account and operation context separately when investigating an ownership discrepancy; a local name is not proof of the original creator.

After closing readers and leaving the mounted directory:

~~~bash
fusermount3 -u "$mountpoint"
findmnt --mountpoint "$mountpoint" -o TARGET,SOURCE,FSTYPE,OPTIONS
~~~

Confirm successful unmount and absence of that exact mount before reusing the directory. Busy mount errors need open-file/current-directory investigation; lazy detach is not evidence that all users released it. A reconnect can invalidate existing file handles, so interrupted reads remain incomplete until reopened and checked.

References: [SSHFS manual/source](https://github.com/libfuse/sshfs/blob/master/sshfs.rst), [FUSE access model](https://github.com/torvalds/linux/blob/master/Documentation/filesystems/fuse/fuse.rst), and [SSH client configuration](https://man.openbsd.org/ssh_config.5).
