---
name: evil-winrm
description: Open a Windows WinRM session from Linux with Evil-WinRM using known credentials. Use for transport/authentication diagnosis, current token inspection, selected file transfers and distinguishing WinRM access from SMB login success.
---

# Evil-WinRM sessions

A valid SMB login does not establish WinRM permission. Confirm the Windows endpoint, listener transport/port and intended account. Inspect `evil-winrm -h` and `evil-winrm -V`; packaged releases can differ from current upstream.

Define `server` as the intended hostname/IP and `account` as the account identity accepted by that endpoint. For its normal HTTP listener, omit `-p` to enter the known password at the hidden prompt:

~~~bash
evil-winrm -i "$server" -u "$account"
~~~

For an HTTPS listener, use `-S` (default port 5986); HTTP defaults to 5985. A custom `-P` is a port, whereas lowercase `-p` supplies a password. In the reviewed client, SSL sets the default port during option parsing, so place an explicit `-P` after `-S`. This implementation disables TLS peer-certificate verification; `-S` alone does not authenticate the server's certificate.

`-H` expects the NT hash alone, not a whole SAM record or `LM:NT` pair. Do not combine it with `-p`. Kerberos uses `-r REALM`, a resolvable server FQDN and working realm configuration/cache; the default service prefix is `HTTP`. Verify cache options against this release rather than assuming Impacket's switches apply.

Once connected, use `whoami` and `Get-Location` to establish identity and working directory. A prompt is not proof of administrator rights. `download` copies remote to local and `upload` copies local to remote; use the session's `menu` help, explicit paths and one selected file first. Confirm local size/hash where a trusted remote comparison exists.

When the question concerns the session's authority, inspect its current Windows token inside the remote prompt:

~~~powershell
whoami /user
whoami /priv
~~~

Keep the account SID and privilege state. An illustrative `SeBackupPrivilege ... Enabled` is a property of this token; a listed but disabled privilege is not currently active. File access through backup privilege requires an enabled privilege and an API using [backup semantics](https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights#backup-and-restore-access-rights). It does not make every `Get-Content` or download bypass ACLs, or grant arbitrary write access. Check the intended operation's API and actual error before concluding that a token privilege is ineffective. Registry export is a separate operation that creates a potentially sensitive file; a privilege listing alone neither performs nor validates a backup.

For failures, separate connection refusal/timeouts from authentication errors and command authorization. Repeated password retries do not repair listener, realm or access-policy problems. Remote path completion warnings can be local Ruby limitations. Session logs and downloaded files may contain secrets. End with `exit`; preserve only needed evidence and account for uploaded artifacts.

For option or transfer differences, consult [upstream usage](https://github.com/Hackplayers/evil-winrm) and the [client implementation](https://github.com/Hackplayers/evil-winrm/blob/master/evil-winrm.rb).
