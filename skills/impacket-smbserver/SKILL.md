---
name: impacket-smbserver
description: Expose a temporary, explicitly bound SMB share from Linux for selected lab file transfers. Use when guest policy, SMB dialect, share direction or listener permissions cause transfer failures.
---

# Temporary Impacket SMB share

Read this entire SKILL.md before acting; reuse complete current context. This task requires the installed Impacket server, an approved interface/port, a dedicated transfer directory and the needed listener/filesystem permissions. Select share direction and client authentication/dialect policy before starting. Finish with received-file integrity and a stopped listener; missing bind privileges, client policy or write access remains a prerequisite gap. There are no conditional resources for this task.

Inspect `impacket-smbserver -h`; upstream may install `smbserver.py`. Use a dedicated directory containing only intended transfer files, with no symlinks into unrelated data. The server's OS identity and directory permissions determine its file access. Upload destinations require a writable share; downloads need only reads.

Define `bind_ip` as the lab interface reachable by the client, `share_dir` as the absolute dedicated directory, and `share_user` as a temporary transfer username:

~~~bash
impacket-smbserver -ip "$bind_ip" -port 445 -smb2support -username "$share_user" TRANSFER "$share_dir"
~~~

The reviewed implementation prompts for a password when `-username` is supplied without `-password`/`-hashes`. Confirm that behavior locally instead of putting a reusable secret into argv. No username means anonymous access. Where supported, add `-readonly` for downloads; that option is version-dependent. The default share is writable subject to filesystem permissions.

Port 445 normally needs appropriate Linux bind privileges/capabilities. Check for an existing SMB service before starting; do not replace it automatically. A high `-port` can support compatible test clients, but ordinary Windows UNC paths do not express an arbitrary SMB port, so simply changing to 1445 may break the intended transfer.

On the client, the path is `\\server-address\TRANSFER\filename`. Separate reachability, authentication, share lookup and file permissions when diagnosing failure. Modern Windows may reject guest access or require signing; `-smb2support` selects protocol support and does not by itself establish compliance with every signing/encryption policy. Do not weaken the client's policy as the first fix.

Keep the foreground transcript private: authentication details and file paths may appear. After a transfer, verify the received file's size/hash at both ends where possible; a connection log is not proof of a complete copy. Stop the listener when finished and verify the port is closed. Retain received artifacts intentionally rather than deleting the whole directory as automatic cleanup.

Resolve implementation differences with the upstream [server CLI, authentication and share creation](https://github.com/fortra/impacket/blob/master/examples/smbserver.py).
