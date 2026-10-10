# Recover one selected credential in a suitable existing task context

Use this only when the task permits the selected script change and the existing task actually runs as the intended credential owner with a suitable logon context. Do not replace a production cleanup script blindly. Inspect exact task path/name, principal, logon type and actions:

~~~powershell
$task = Get-ScheduledTask -TaskName $taskName -TaskPath $taskPath
$task.Principal | Select-Object UserId, LogonType, RunLevel
$task.Actions | Select-Object Execute, Arguments, WorkingDirectory
~~~

A password-logon task stores usable registration credentials; S4U has different limitations, and an interactive-token task needs a logged-on user. Creating a password-logon task needs that password at registration, but it is false that every task type requires knowing a cleartext password. Starting an existing suitable task does not require registering a new one.

Confirm script permissions, relevant concurrency and the restore plan. Preserve original bytes/hash and metadata, and record the task definition. Choose an already secured fresh output path accessible only to the necessary owner/operator; a generic world-readable Tasks file is not an acceptable default.

For an approved temporary script body, define a literal selected `$credentialTarget` and `$privateOutput` within the script. This body recovers exactly that credential rather than all stored targets:

~~~powershell
$ErrorActionPreference = 'Stop'
Import-Module CredentialManager
$credential = Get-StoredCredential -Target $credentialTarget -ErrorAction Stop
if ($null -eq $credential) { throw 'Selected credential was not returned' }
$network = $credential.GetNetworkCredential()
[pscustomobject]@{
    UserName = $network.UserName
    Password = $network.Password
} | ConvertTo-Json | Set-Content -LiteralPath $privateOutput -Encoding UTF8
~~~

Write the reviewed temporary body through the authorized session, preserving/restoring the selected original script rather than appending an untracked secret dump. The output is cleartext sensitive evidence; its path/ACL must be selected before running, and filename existence is not proof of successful recovery.

~~~powershell
Start-ScheduledTask -TaskName $taskName -TaskPath $taskPath
Get-ScheduledTaskInfo -TaskName $taskName -TaskPath $taskPath
~~~

Track actual completion/time/error and the new output associated with this run. A task-start request is not completion. If the task or credential call fails, preserve that result without assuming another user/session would behave the same. Restore original script bytes/metadata after the selected run ends, verify the hash and task action, and account for the owned output. A recovered secret still needs a separately authorized service/account check before claiming reuse elsewhere.

See [Windows task logon types](https://learn.microsoft.com/en-us/windows/win32/api/taskschd/ne-taskschd-task_logon_type), [Start-ScheduledTask](https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/start-scheduledtask) and [credential API](https://learn.microsoft.com/en-us/windows/win32/api/wincred/nf-wincred-credenumeratew).
