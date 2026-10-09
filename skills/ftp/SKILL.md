---
name: ftp
description: Retrieve selected files with a traditional Linux ftp client without binary conversion or data-channel confusion. Use for archive/database downloads and diagnosing listings that hang after successful login.
---

# FTP file retrieval

Identify the installed implementation through its package/version and interactive `help`. GNU inetutils, tnftp and other clients differ in passive-mode defaults and switches. `sftp` is a different protocol, not a spelling of FTP.

Define `server` as the intended FTP host and `out` as a new private local directory. Connect from that directory and enter the known credentials at the client prompts:

~~~bash
umask 077
mkdir -- "$out" && (cd -- "$out" && ftp "$server")
~~~

At the **FTP prompt**, inspect `status`, select `binary`, then use `pwd`/`ls` to locate the artifact. Run `get remote-name local-name` with actual selected filenames; these are FTP arguments, not shell variables. Use a fresh local name to avoid overwriting evidence. Finish with `bye`.

Select binary mode explicitly for password databases, ZIP/TAR archives, executables and hives. ASCII mode can change bytes; a successful transfer message alone does not establish integrity. Verify expected size and any independently available checksum, then use the artifact's own integrity/parser check. If a download is incomplete, retain it as partial and re-fetch to a fresh name; use `reget` only after confirming matching source and client resume behaviour.

A login/control connection can succeed while `ls` or `get` stalls: both need a separate data connection. Inspect `status` and `help passive`; in common clients bare `passive` **toggles** the setting. Check the selected passive endpoint and firewall/NAT path. Active mode reverses the data-connection direction. Change only the relevant mode/path after observing the failure, not the host's entire firewall policy.

Plain FTP exposes credentials and data on the network. If the service requires FTPS, use a client that actually supports its TLS policy; this interactive recipe does not add TLS. Record transfer mode, source, destination and integrity result separately from authentication success.

Documentation reviewed 2026-10-09; Linux execution untested. Cases: Administrator p. 7; Admirer pp. 7–8. Source: [NetBSD/tnftp manual](https://github.com/NetBSD/src/blob/trunk/usr.bin/ftp/ftp.1). Check local client help for implementation differences.
