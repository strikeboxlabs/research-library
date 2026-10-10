---
name: credentialmanager
description: Read a selected stored Windows credential through the installed CredentialManager PowerShell module in a remote session. Use from a Linux worker when network-logon or SYSTEM context differs from the intended user credential set.
---


# Read the credential set associated with this token

Read this entire SKILL.md before acting. This is the Windows CredentialManager PowerShell module, used through an authorized remote Windows session; it is not a Linux credential-store reader. Require the selected host/user/target and private evidence scope. For a suitable existing scheduled task, read [scheduled user context](references/scheduled-user-context.md) fully before modifying its script. Finish with actual token/context, selected credential result and any restoration evidence; administrator status alone is insufficient.

In the remote PowerShell prompt, inspect the installed module and its help:

~~~powershell
Get-Module -ListAvailable CredentialManager
Get-Help Get-StoredCredential -Full
whoami /user
~~~

For a known stored target, define `$credentialTarget` and select it explicitly:

~~~powershell
$credential = Get-StoredCredential -Target $credentialTarget -ErrorAction Stop
$credential.UserName
~~~

`-Type` defaults to Generic in the reviewed module; choose the observed credential type from installed help if the selected target uses another type. The same target name with a different type is not necessarily the same record. The normal result is a PSCredential with a SecureString, not a printed cleartext password. When recovery of this selected secret is authorized, `$credential.GetNetworkCredential().Password` obtains its value; retain it only in the task's private evidence channel. Do not enumerate/dump every unrelated target merely because the module allows it. The `-AsCredentialObject` mode can expose additional raw fields, including a password, so it is not a harmless metadata alternative.

A selected target uses `CredRead`; omitting the target uses `CredEnumerate` and can enumerate the whole store. Both use the current token's logon-session credential set. Error 1312 (`ERROR_NO_SUCH_LOGON_SESSION`) can mean that session has no credential set; Windows network logons do not have one. A WinRM administrator login can therefore fail while a suitable user task succeeds. SCM execution as SYSTEM uses another identity/context and does not automatically read that administrator's store. A warning about conversion without username/password describes that returned object, not proof all stores are empty.

Inspect the actual task/logon context when it changes the decision. An ordinary account name, a machine hash or the presence of this module does not establish that a matching stored secret exists. A failure is specific to this store/context; changing the password or enabling RDP is not a default repair.

See [module implementation](https://github.com/davotronic5000/PowerShell_Credential_Manager/blob/master/PSCredentialManager.Cmdlet/Cmdlets.cs) and [selected credential API](https://learn.microsoft.com/en-us/windows/win32/api/wincred/nf-wincred-credreadw) and [enumeration/error semantics](https://learn.microsoft.com/en-us/windows/win32/api/wincred/nf-wincred-credenumeratew).
