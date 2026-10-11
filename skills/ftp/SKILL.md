---
name: ftp
description: Transfer selected files with a traditional Linux ftp client and distinguish authentication, data-channel success and file integrity. Use for binary downloads, stalled listings or an authorised upload-to-web mapping check.
---

# FTP file transfers

Read this entire skill before acting; complete current context need not be re-read. Establish the intended server, known credentials and selected transfer before connecting. For an authorised upload and HTTP publication check, read [upload-to-web mapping](references/upload-web-mapping.md) fully first. Completion requires transfer/content evidence for the requested task; login success alone is insufficient.

Identify the installed implementation through its package/version and interactive `help`. GNU inetutils, tnftp and other clients differ in passive-mode defaults and switches. `sftp` is a different protocol, not a spelling of FTP.

An OpenBSD writeup's `ftp http://...` is an HTTP fetch supported by that client, not an FTP transaction. Verify URL-fetch support before transplanting it to Linux; otherwise select an HTTP client. Protocol choice determines the relevant transport and diagnostics, regardless of the executable's name.

Define `server` as the intended FTP host and `out` as a new private local directory. Connect from that directory and enter the known credentials at the client prompts:

~~~bash
umask 077
mkdir -- "$out" && (cd -- "$out" && ftp "$server")
~~~

At the **FTP prompt**, inspect `status`, select `binary`, then use `pwd`/`ls` to locate the artifact. Run `get remote-name local-name` with actual selected filenames; these are FTP arguments, not shell variables. Use a fresh local name to avoid overwriting evidence. Finish with `bye`.

`pwd` and `cd` refer to the server's directory; `lcd` changes the client's local download directory. If the local destination is unwritable, use `lcd` with an existing private output directory and confirm the client's acknowledgement before downloading. That does not change remote permissions. A directory listing resembling `/root` does not establish the server's host filesystem root, your local account identity or a root shell; the service can map its own namespace.

Select binary mode explicitly for password databases, ZIP/TAR archives, executables and hives. ASCII mode can change bytes; a successful transfer message alone does not establish integrity. Verify expected size and any independently available checksum, then use the artifact's own integrity/parser check. If a download is incomplete, retain it as partial and re-fetch to a fresh name; use `reget` only after confirming matching source and client resume behaviour.

A login/control connection can succeed while `ls` or `get` stalls: both need a separate data connection. Inspect `status` and `help passive`; in common clients bare `passive` **toggles** the setting. Check the selected passive endpoint and firewall/NAT path. Active mode reverses the data-connection direction. Change only the relevant mode/path after observing the failure, not the host's entire firewall policy.

Plain FTP exposes credentials and data on the network. If the service requires FTPS, use a client that actually supports its TLS policy; this interactive recipe does not add TLS. Record transfer mode, source, destination and integrity result separately from authentication success.

Sources: [NetBSD/tnftp manual](https://github.com/NetBSD/src/blob/trunk/usr.bin/ftp/ftp.1), [OpenBSD URL fetching](https://man.openbsd.org/ftp.1). Check local client help for implementation differences.
