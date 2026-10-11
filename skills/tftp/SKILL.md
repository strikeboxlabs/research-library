---
name: tftp
description: Transfer a selected ordinary file with the tftp-hpa client and interpret binary mode, remote names, timeouts and server errors. Use when a UDP port indication or connect command is being mistaken for a completed file transfer.
---

# Selected TFTP file transfer

Read this entire SKILL.md before acting. This procedure targets the installed **tftp-hpa** client and a known administration endpoint. Select one ordinary file and its permitted server name; identify the client before using this syntax. Finish with transfer status and available byte-integrity evidence, or the specific server/transport failure.

Define `server` and decimal `port` as the intended endpoint, `remote_file` as its configured file name, and `local_file` as a fresh local destination for download or an existing owned input for upload:

~~~bash
tftp -V
tftp -v -l -m binary "$server" "$port" -c get "$remote_file" "$local_file"
~~~

For a requested upload, use the opposite file order:

~~~bash
tftp -v -l -m binary "$server" "$port" -c put "$local_file" "$remote_file"
~~~

Binary mode preserves file bytes. Literal mode preserves colon-containing names; server-side path mapping remains configuration-specific. Check status and diagnostics before inspecting output. Compare size and a known digest when available; received bytes alone do not establish expected content.

The interactive `connect` command selects a default peer without a handshake. A UDP netcat indication likewise does not establish TFTP success. A server error for a missing or denied name differs from a timeout; neither proves the entire host filesystem is accessible. Investigate the selected name, server permissions and data-packet path before retrying. Bound interactive transfers with the client's `timeout` setting when needed.

TFTP supplies no authentication mechanism; use the designated administration service. Resolve implementation syntax with the installed help and the [tftp-hpa manual](https://manpages.debian.org/bookworm/tftp-hpa/tftp.1.en.html).
