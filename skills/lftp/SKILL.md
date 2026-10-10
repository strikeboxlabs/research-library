---
name: lftp
description: Use lftp for explicit FTPS listings and selected file transfers. Diagnose encryption-required logins, certificate failures, data-channel stalls and vsftpd virtual-user mapping.
---

# lftp for protected FTP transfers

Read this entire SKILL.md before acting; reuse complete current context. Establish the endpoint, known account and certificate trust before login. Finish with the selected operation's completion status and acquired file evidence, or the exact failed stage. For server-side account/root discrepancies when configuration is available, read [vsftpd identity and access](references/vsftpd-access.md) fully; otherwise keep that branch unloaded.

Check `lftp --version` for TLS support. Explicit FTPS upgrades an FTP connection, commonly on port 21; implicit FTPS starts with TLS, commonly on 990. SFTP uses SSH and is a different protocol. A server reply requiring encryption calls for the matching transport, not password guessing. After a `421` disconnect, open a fresh connection.

Start `lftp` without a URL so settings precede login. The following are **lftp prompt commands**, with illustrative endpoint/account/path values to replace. Keep an overall observation/transfer deadline in the harness; retries alone are not a total time limit.

~~~text
set ftp:ssl-allow yes
set ftp:ssl-force yes
set ftp:ssl-auth TLS
set ftp:ssl-protect-data yes
set ftp:ssl-protect-list yes
set ftp:ssl-use-ccc no
set ssl:verify-certificate yes
set ssl:check-hostname yes
set net:max-retries 1
set net:timeout 15
open -u analyst ftp://ftp.lab.example:21
pwd
cls -la
get report.csv -o /private/acquisition/report.csv
bye
~~~

Enter the known password at the prompt; do not embed it in the URL. Use an existing private destination directory and a fresh file. For a private CA, set `ssl:ca-file` to its independently trusted PEM file before `open`; retain hostname checking. `ftps://` selects implicit TLS and is not the replacement URL for a port-21 STARTTLS service. Inspect `set -a` if startup configuration or host-specific settings contradict the intended policy.

`get` transfers bytes in binary mode by default. Compare completed transfer size and an independently supplied checksum when available; an existing output file can be partial. Use `get -c` only when the local partial file is from the same unchanged remote object. A successful listing does not establish download or write permission. Only for an explicitly requested upload, `put local-file -o remote-name` writes that selected remote path and may overwrite it; choose the path deliberately. Do not substitute recursive `mirror` for one file.

| Observation | Next decision |
|---|---|
| Certificate/hostname verification failure | Correct trust input, name or endpoint before credentials; disabling verification is not a routine fix. |
| Login succeeds, listing or transfer stalls | Inspect the separate FTP data connection, passive-port reachability and data TLS/session-reuse diagnostics; control-channel success is insufficient. |
| `550` on one path | Check the server-visible root, selected name and permissions; do not infer an invalid password. |
| Transfer interrupted or process seems finished | Inspect operation status and `jobs`; lftp can keep active jobs in the background on exit. Cancel only this task's jobs if abandoning it. |

See the [lftp manual](https://lftp.yar.ru/lftp-man.html) for local option differences and [FTP over TLS](https://www.rfc-editor.org/rfc/rfc4217.html) for control/data protection.
