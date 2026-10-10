---
name: sharp-gpoabuse
description: Apply a selected GPO local-administrator change with SharpGPOAbuse through a remote Windows command session. Use from Linux to distinguish policy write rights, linked client scope, application and fresh token evidence.
---


# Apply and verify the selected GPO operation

Read this entire SKILL.md before acting. SharpGPOAbuse is a Windows .NET executable, run on the authorized Windows host through a remote session from the Linux worker. Require the selected existing GPO, affected clients, principal to add and complete restoration plan before writing. Finish with policy-write, client-application and fresh-token evidence separately; 'Done' is not all three.

Confirm the existing reviewed binary and supported help; deployment of an absent binary is a separate task. The selected user needs the relevant directory and SYSVOL write rights. A graph GenericWrite edge is a lead; it does not establish all required file/attribute writes or that the GPO applies to this computer.

Inspect links, computer-half enablement, security/WMI filters and precedence. The connection DC is not the sole affected client. Record the current GPO directory attributes/version, `GPT.ini`, extension attributes and selected `GptTmpl.inf` contents/absence before mutation, with a way to restore only owned changes while preserving concurrent edits. Do not use `--Force` automatically to overwrite an existing file.

Inside the remote PowerShell session, define `$binary` as the reviewed Windows executable path, `$memberAccount` as the actual intended AD account and `$gpoName` as the observed display name:

~~~powershell
& $binary --AddLocalAdmin --UserAccount $memberAccount --GPOName $gpoName
~~~

This changes the GPO security template and directory/SYSVOL version state; it does not merely change the running host's current group list. Inspect the reported domain, GPO GUID and resolved account SID. Similar display names such as `analyst` and `analyst.adm` are different principals; do not carry the operator's login name into the target account silently. On a domain controller, an Administrators change concerns its domain controller security context, not an ordinary member-server local SAM assumption.

After an approved change, policy processing on the intended client can be requested separately:

~~~powershell
gpupdate /target:computer /force
~~~

This is state changing on that client. A successful refresh is not proof every setting applied; inspect resultant policy/errors and actual membership. Normal refresh is not universally exactly 90 minutes: member clients normally use 90 minutes plus jitter, DC defaults differ and extension/policy settings can change timing. Open a fresh selected-user session and inspect `whoami /user` and `whoami /groups`; an old token may not reflect the new membership. Group presence and enabled token authority remain different observations.

Restore the owned policy changes and verify directory/SYSVOL state, client policy and membership. Removing a setting need not reverse an already applied membership, so reconcile that explicitly within the approved scope. See [upstream supported operation](https://github.com/ReversecLabs/SharpGPOAbuse#adding-a-local-admin) and [Windows policy processing](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-policy/group-policy-processing).
