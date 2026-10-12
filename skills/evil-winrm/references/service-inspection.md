# Separate configured and current service evidence

Run these read-only Windows commands inside the established session. Define `$serviceName` as the selected exact service name, rather than a display name or broad wildcard. Preserve session identity, remote PowerShell version and each error.

~~~powershell
Get-Service -Name $serviceName -ErrorAction Stop |
    Select-Object Name, DisplayName, Status
~~~

A returned Status describes that service at query time. Access denied or an unavailable cmdlet leaves state unknown; an empty process-name search does not prove a service is absent. Get-Service property availability differs between Windows PowerShell and newer PowerShell versions.

`CanStop=True` describes the service's accepted stop control, not the current caller's `SERVICE_STOP` permission. Start and stop are separate access rights. A failed security-descriptor query leaves those rights unknown; it does not justify assuming restart access. Likewise, `STOP_PENDING` or `START_PENDING` acknowledges a transition in progress, not its final state. Keep capability, caller authorization and completed state distinct without issuing a restart merely to inspect permission. See [CanStop](https://learn.microsoft.com/en-us/dotnet/api/system.serviceprocess.servicecontroller.canstop?view=dotnet-plat-ext-5.0) and [service access rights](https://learn.microsoft.com/en-us/windows/win32/services/service-security-and-access-rights).

For static configuration, select the same service's registry key:

~~~powershell
$serviceKey = 'HKLM:\SYSTEM\CurrentControlSet\Services\' + $serviceName
Get-ItemProperty -LiteralPath $serviceKey -ErrorAction Stop |
    Select-Object ImagePath, ObjectName, Start, Type
~~~

These are configured values, not running-state evidence. Preserve the complete executable path and arguments; do not execute the string or assume a portable `Progra~1` short path. An installation directory or file-version string is a lead to reconcile with the selected service, running binary and vendor release information, not a vulnerability verdict.

ImagePath arguments can expose a plaintext application credential. Keep the original only in private evidence and redact secret values from the finding; a broad pipeline that selects only ImagePath loses its association with the service key. Retain that key/name when selecting the specific configuration. Excluding every svchost.exe row or requiring the text `exe` limits the inventory and cannot establish that omitted services are uninteresting or absent. A credential-like argument is an exposure observation, not proof of the service's current process identity, account validity or permission to replay it.

For Microsoft Entra Connect, distinguish the ADSync service identity from the AD DS connector account and the Entra connector account. Reading ObjectName identifies the configured service account only; it does not establish either connector's identity. Account defaults depend on installation history and host configuration. Do not read credential tables or decrypt secrets to answer this metadata task.

Finish with current state if available, separately labelled configuration, version/context and unresolved permission or coverage gaps. No service start/stop, registry changes or uploaded scripts are needed.

References: [Get-Service](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-service), [Get-ItemProperty](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-itemproperty), [Connect account roles](https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/reference-connect-accounts-permissions).
