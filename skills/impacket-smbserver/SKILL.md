---
name: impacket-smbserver
description: Expose a temporary, explicitly bound SMB share from Linux for selected lab file transfers. Use when guest policy, SMB dialect, share direction or listener permissions cause transfer failures.
---

# Temporary Impacket SMB share

Inspect `impacket-smbserver -h`; upstream may install `smbserver.py`. Use a dedicated directory containing only intended transfer files, with no symlinks into unrelated data. The server's OS identity and directory permissions determine its file access. Upload destinations require a writable share; downloads need only reads.

Define `bind_ip` as the lab interface reachable by the client, `share_dir` as the absolute dedicated directory, and `share_user` as a temporary transfer username:

~~~bash
impacket-smbserver -ip "$bind_ip" -port 445 -smb2support -username "$share_user" TRANSFER "$share_dir"
~~~

The reviewed implementation prompts for a password when `-username` is supplied without `-password`/`-hashes`. Confirm that behavior locally instead of putting a reusable secret into argv. No username means anonymous access. Where supported, add `-readonly` for downloads; that option is version-dependent. The default share is writable subject to filesystem permissions.

Port 445 normally needs appropriate Linux bind privileges/capabilities. Check for an existing SMB service before starting; do not replace it automatically. A high `-port` can support compatible test clients, but ordinary Windows UNC paths do not express an arbitrary SMB port, so simply changing to 1445 may break the intended transfer.

On the client, the path is `\\server-address\TRANSFER\filename`. Separate reachability, authentication, share lookup and file permissions when diagnosing failure. Modern Windows may reject guest access or require signing; `-smb2support` selects protocol support and does not by itself establish compliance with every signing/encryption policy. Do not weaken the client's policy as the first fix.

Keep the foreground transcript private: authentication details and file paths may appear. After a transfer, verify the received file's size/hash at both ends where possible; a connection log is not proof of a complete copy. Stop the listener when finished and verify the port is closed. Retain received artifacts intentionally rather than deleting the whole directory as automatic cleanup.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Appsanity pp. 14–17. Source: [server CLI, authentication and share creation](https://github.com/fortra/impacket/blob/master/examples/smbserver.py).
