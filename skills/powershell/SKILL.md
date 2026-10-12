---
name: powershell
description: Inspect Windows filesystem metadata or a selected authentication policy through an established PowerShell session. Use when provider paths, aliases, access errors or NTLM policy values need precise interpretation.
---

# Inspect Windows metadata and policy

Read this entire SKILL.md before acting. Require an already authorized Windows PowerShell session on the owned machine. Select filesystem drive inventory below, supply the permitted directory for its listing, or read [NTLM policy evidence](references/ntlm-policy.md) fully for that conditional registry task. A Linux worker needs that existing Windows execution context; installing Linux pwsh does not supply it. Finish with metadata/status and the supported result, keeping denied or incomplete queries explicit.

Inspect `$PSVersionTable` and actual command resolution before applying copied aliases:

~~~powershell
$PSVersionTable
Get-Command Get-ChildItem,ls,wget -ErrorAction Continue
~~~

Windows PowerShell 5.1 and PowerShell 7 can resolve short names differently. An `ls` in a PS prompt commonly calls Get-ChildItem rather than GNU ls; a historical `wget` can invoke Invoke-WebRequest rather than GNU Wget. Inspect the actual binding rather than borrowing another program's switches.

When identifying filesystem roots available to this session:

~~~powershell
Get-PSDrive -PSProvider FileSystem |
    Select-Object Name,Root,DisplayRoot,Used,Free
~~~

A PSDrive is a provider mapping, not necessarily a physical disk. The unfiltered command also lists providers such as Registry, Alias and Environment. A filesystem drive may represent a local volume, network mapping or session-created root; a new letter alone does not prove added hardware or shared storage. These results describe the current session's mappings, not another service account's access. Select a root before the directory query; visible metadata does not prove its contents readable.

Define `$directory` as the selected absolute Windows filesystem path, with no wildcard discovery. Read its immediate children:

~~~powershell
Get-ChildItem -LiteralPath $directory -Force -ErrorAction Stop |
    Select-Object Name,FullName,Mode,Length,LastWriteTime
~~~

`-LiteralPath` treats wildcard-looking characters as path data; `-Force` includes otherwise hidden/system entries but does not bypass access controls. No recursion is selected. Retain errors and the actual host/path. A visible installation folder is evidence of a directory, not proof its application is running, that all children are readable or that the current account can read configuration contents. Length and timestamp are metadata rather than content identity. Source-derived passwords and secret database files are outside this listing task.

References: [Get-ChildItem filesystem and access semantics](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-childitem?view=powershell-5.1), [command lookup](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/get-command?view=powershell-5.1), [Get-PSDrive provider and session scope](https://github.com/MicrosoftDocs/PowerShell-Docs/blob/main/reference/5.1/Microsoft.PowerShell.Management/Get-PSDrive.md).
