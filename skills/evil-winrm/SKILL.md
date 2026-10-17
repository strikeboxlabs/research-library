---
name: evil-winrm
description: Open an owned Windows WinRM session from Linux with a provisioned password or client certificate; inspect current token, selected service, AD computer metadata, registry and policy evidence, and diagnose authentication or transfer failures.
---

# Evil-WinRM sessions

Read this entire SKILL.md before acting. Require the selected endpoint/account and credential mechanism, then confirm the actual remote identity and requested action/transfer. Read [service inspection](references/service-inspection.md) fully for selected Windows service evidence, [AD computer metadata](references/ad-computer-metadata.md) fully for one selected directory computer and its name-resolution evidence, or [policy and registry evidence](references/policy-and-registry-evidence.md) fully for stored GPO settings, registry SDDL or selected current registry metadata. These references are conditional; other session tasks use this entrypoint. Missing WinRM permission or incomplete evidence remains unresolved, regardless of another protocol's login result.

A valid SMB or web-portal login does not establish WinRM permission. Confirm the Windows endpoint, listener transport/port, WSMan route and intended account. An open TCP 5985 or an HTTPAPI/IIS banner alone does not establish a working WinRM listener. An HTTP 404 with missing authentication headers can concern the route or service; it does not by itself prove a bad password. Inspect `evil-winrm -h` and `evil-winrm -V`; packaged releases can differ from current upstream.

Define `server` as the intended hostname/IP and `account` as the account identity accepted by that endpoint. For its normal HTTP listener, omit `-p` to enter the known password at the hidden prompt:

~~~bash
evil-winrm -i "$server" -u "$account"
~~~

For an HTTPS listener, use `-S` (default port 5986); HTTP defaults to 5985. A custom `-P` is a port, whereas lowercase `-p` supplies a password. In the reviewed client, SSL sets the default port during option parsing, so place an explicit `-P` after `-S`. This implementation disables TLS peer-certificate verification; `-S` alone does not authenticate the server's certificate.

For a provisioned client-certificate identity on the owned HTTPS listener, require the issued certificate, its matching private key and the administrator-established WinRM account mapping. Define `client_cert` and `client_key` as their existing protected absolute PEM paths:

~~~bash
evil-winrm -i "$server" -S -c "$client_cert" -k "$client_key"
~~~

`-c` supplies a certificate, not a bare public-key file or PFX bundle; `-k` supplies its private key. The reviewed certificate branch does not require `-u` or a password prompt: the server's mapping determines the account. Both files and HTTPS are required; providing one path or omitting `-S` is not a usable certificate connection. Confirm the installed release's flags and consumer support for the key's encryption before connection. A key-passphrase/loading failure is separate from server mapping or WinRM authorization; do not remove key protection as an automatic retry.

Successful PFX extraction establishes neither issuance trust nor mapping. Verify the intended certificate identity, validity/usage and key match under the provisioning process first. This client branch also disables peer verification; require an independently established owned server/channel appropriate to that limitation. Once connected, retain `whoami /user` and the intended harmless administrative result before attributing the mapped identity. Certificate acceptance does not imply administrator rights, and a remote prompt alone is insufficient. Finish and close the selected session as below. See [certificate options and connection behavior](https://github.com/Hackplayers/evil-winrm/blob/master/evil-winrm.rb).

`-H` expects the NT hash alone, not a whole SAM record or `LM:NT` pair. Do not combine it with `-p`. Kerberos uses `-r REALM`, a resolvable server FQDN and working realm configuration/cache; the default service prefix is `HTTP`. Verify cache options against this release rather than assuming Impacket's switches apply.

Once connected, use `whoami` and `Get-Location` to establish identity and working directory. A prompt is not proof of administrator rights. A WinRM network-logon token also need not expose that user's interactive Credential Manager set: WinCred error 1312 can mean this logon session has no associated credential set. A separate SCM command running as SYSTEM changes identity but does not select the original user's store. Diagnose the actual token/logon context before interpreting an empty/error credential query. `download` copies remote to local and `upload` copies local to remote; use the session's `menu` help, explicit paths and one selected file first. Confirm local size/hash where a trusted remote comparison exists.

When the question concerns the session's authority, inspect its current Windows token inside the remote prompt:

~~~powershell
whoami /user
whoami /groups
whoami /priv
~~~

Keep the account SID, token group SIDs/attributes and privilege state. An enabled group is part of this token's authorization context; its display name alone does not establish a particular service operation or unrestricted host access. A disabled or deny-only group needs its actual attributes interpreted rather than treating every listed membership as an enabled grant. An illustrative `SeBackupPrivilege ... Enabled` is a property of this token; a listed but disabled privilege is not currently active. File access through backup privilege requires an enabled privilege and an API using [backup semantics](https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights#backup-and-restore-access-rights). It does not make every `Get-Content` or download bypass ACLs, or grant arbitrary write access. Check the intended operation's API and actual error before concluding that a token privilege is ineffective. Registry export is a separate operation that creates a potentially sensitive file; a privilege listing alone neither performs nor validates a backup.

When two sessions for the same account show different privilege states, retain each session's SID, invocation/logon context and token output separately. A privilege listed as Disabled is present in that token but inactive; this differs from its absence. A later Enabled listing is evidence about the later token, not proof that the account's assigned rights changed or that the first session lacked the privilege. Do not enable privileges or select an elevated process merely to collect this evidence. See [Windows privilege/token semantics](https://learn.microsoft.com/en-us/windows/win32/secauthz/privileges).

For failures, separate connection refusal/timeouts from authentication errors and command authorization. `WinRM::WinRMAuthorizationError` prints as the generic line "Cannot establish connection to remote endpoint. Check credentials and network." followed by the class name; the first line alone reads as a network fault, so read both lines before diagnosing — the credential was rejected, and retrying against listener/firewall state will not change it. The banner and version warning print before any connection attempt, so their presence does not indicate an established session. For scripted use without a TTY, piping commands works: `printf 'whoami\nexit\n' | evil-winrm -i "$server" -u "$account" -p "$password"` — feed `exit` explicitly or the client waits on closed stdin. Repeated password retries do not repair listener, realm or access-policy problems. Remote path completion warnings can be local Ruby limitations. Session logs and downloaded files may contain secrets. End with `exit`; preserve only needed evidence and account for uploaded artifacts.

If an expected identity command is unavailable on a specialized Windows image, retain that command-resolution error. USERPROFILE and a home-directory path are environment metadata, not account SID or token-privilege evidence. Similarly, ownership/readability of a credential XML file does not establish its decryption context: Windows PowerShell CLIXML credential encryption binds the exporting user and computer through DPAPI. Treat these as separate limitations; do not substitute directory names or file ownership for verified session authority. See [Import-Clixml platform and user binding](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/import-clixml).

For option or transfer differences, consult [upstream usage](https://github.com/Hackplayers/evil-winrm) and the [client implementation](https://github.com/Hackplayers/evil-winrm/blob/master/evil-winrm.rb).
