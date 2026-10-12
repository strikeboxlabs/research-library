# Separate stored policy, current ACLs and effective access

Use the established authorized Windows session. Require the selected acquired policy file or exact registry key, current session identity and remote PowerShell version. Reading these records does not require importing PowerView or changing registry values.

For an already selected GPO security template, define `$policyFile` as its exact path and read it as data:

~~~powershell
Get-Content -LiteralPath $policyFile -ErrorAction Stop
~~~

Retain the GPO identity, acquisition context and relevant section/key/SID. GUID-named sibling directories in SYSVOL are separate GPOs, not policies inside one default policy. A GptTmpl.inf setting is stored configuration; links, scope, filtering, precedence and application state determine the target's effective policy. Do not report it as applied without that evidence.

For a selected registry security descriptor, define `$sddl` as the unchanged descriptor string:

~~~powershell
ConvertFrom-SddlString -Sddl $sddl -Type RegistryRights -ErrorAction Stop
~~~

This is a built-in Microsoft.PowerShell.Utility cmdlet, introduced in PowerShell 5.0 and available only on Windows. Its default type is FileSystemRights: the same numeric masks can then appear as file/directory rights. Select RegistryRights for registry descriptors; `KA` means registry full control, while `KR` means registry read. Preserve the raw SDDL, SID, mask and ACE flags alongside readable output. An unresolvable SID or conversion error is an evidence gap, not an empty ACL.

An allow ACE is not by itself effective access for a particular token. Evaluate deny entries, enabled/deny-only group SIDs, ownership and inheritance on the selected object. `CIIO` marks container inheritance plus inherit-only; that ACE does not apply to the current key itself. Friendly names are aids, not substitutes for SID comparisons.

Keep the original descriptor as the authority for flags. The cmdlet's readable output and converted RawDescriptor can normalize or omit inheritance-only entries when materialized as a non-container ACL; an absent rendered ACE does not prove it was absent from the input. If flags matter, inspect the unchanged string directly:

~~~powershell
$originalDescriptor = [System.Security.AccessControl.RawSecurityDescriptor]::new($sddl)
$originalDescriptor.DiscretionaryAcl |
    Select-Object SecurityIdentifier, AccessMask, AceType, AceFlags
~~~

To compare a stored descriptor with the current selected key, define `$registryKey` as the exact provider path:

~~~powershell
$currentAcl = Get-Acl -LiteralPath $registryKey -ErrorAction Stop
ConvertFrom-SddlString -Sddl $currentAcl.Sddl -Type RegistryRights -ErrorAction Stop
Get-ItemProperty -LiteralPath $registryKey -ErrorAction Stop
~~~

Keep the host, session identity, query time and 32/64-bit process/registry view. A current value or configured DLL path does not establish that a process loaded it. Preserve the complete returned path; a different architecture-specific filename in prose is not equivalent evidence. A readable ACL does not prove permission to change the key.

Treat logon-right names separately: `SeDenyNetworkLogonRight` concerns network logon, `SeInteractiveLogonRight` concerns local interactive logon and `SeRemoteInteractiveLogonRight` concerns Remote Desktop logon. An interactive allow setting does not grant every other logon method; a network deny does not prove those other methods succeed. Reconcile configured rights with the actual logon type, effective policy and token before attributing a failure.

Finish with separately labelled stored settings, current queried values/ACLs and the conclusions those observations support. Missing effective-policy, SID-resolution, token or registry-view evidence remains unresolved. No registry write, policy refresh or uploaded module is required.

References: [ConvertFrom-SddlString](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/convertfrom-sddlstring), [ACE flags and rights](https://learn.microsoft.com/en-us/windows/win32/secauthz/ace-strings), [deny network logon](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/security-policy-settings/deny-access-to-this-computer-from-the-network), [allow local logon](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/security-policy-settings/allow-log-on-locally).
