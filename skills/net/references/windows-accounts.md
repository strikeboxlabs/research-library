# Read Windows account metadata in the established session

Require an already authorized Windows command session on the selected owned machine and its actual native `net.exe`. These commands run there, not through the Linux Samba binary. Record machine/session identity before interpreting the account domain.

In that Windows PowerShell session, use the native installed executable:

~~~powershell
net.exe user
$status = $LASTEXITCODE
~~~

This lists that computer's user accounts. For one established account, define `$account` as its actual local account name:

~~~powershell
net.exe user $account
$status = $LASTEXITCODE
~~~

Inspect status and the complete result. Omit password arguments and mutation switches. `/domain` changes the query to the computer's primary-domain controller; use it only when that is the intended account store. The name's appearance does not establish that it is enabled, currently authenticated or the identity of a running application. A failed query does not prove account absence.

Reference: [Microsoft net user query contract](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/net-user).
