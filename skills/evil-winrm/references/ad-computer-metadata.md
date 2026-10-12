# Read one selected AD computer through the existing Windows session

Require the established owned Windows session, an already available ActiveDirectory module, directory read permission, the selected computer's SAM name/GUID/DN/SID and the intended directory server. This is a remote Windows cmdlet; Linux PowerShell does not thereby acquire RSAT. Define `$computerIdentity` and `$directoryServer` in that session, then request the specific properties:

~~~powershell
Import-Module ActiveDirectory -ErrorAction Stop
$computer = Get-ADComputer -Identity $computerIdentity -Server $directoryServer -Properties DNSHostName,OperatingSystem,OperatingSystemVersion,TrustedForDelegation -ErrorAction Stop
$computer | Select-Object Name,DistinguishedName,SID,DNSHostName,OperatingSystem,OperatingSystemVersion,TrustedForDelegation
~~~

Keep object identity, server, time and errors with the result. Missing module, denied query or absent object is unresolved, rather than a blank property value. Directory OS strings are stored descriptions, not live OS/patch inventory. A base build without its update revision cannot settle a particular security update. `TrustedForDelegation` describes unconstrained-delegation configuration; a resource-based delegation ACL is a different property and neither proves completed impersonation. A `primaryGroupID=515` filter excludes computers using another primary group, including domain controllers; it is not a complete computer inventory.

Only when the requested task includes resolving this computer's existing hostname, validate the returned value before one lookup:

~~~powershell
$fqdn = [string]$computer.DNSHostName
if ([string]::IsNullOrWhiteSpace($fqdn)) { throw 'Selected computer has no DNSHostName; no lookup performed.' }
[System.Net.Dns]::GetHostAddresses($fqdn) | Select-Object IPAddressToString,AddressFamily
~~~

An empty string makes this API return local-host addresses, so repeated local IPs beside blank directory names are not evidence that those computers share an address. A supplied IP returns itself; hosts-file entries and the session machine's resolver also affect results. Retain all returned address families, the queried name and errors. Choosing the first IPv4 address hides other answers. Resolution does not establish host reachability, current service state or domain membership. Finish with the selected object's metadata and, if requested, separately attributed resolution result or explicit missing-name/error gap.

See [Get-ADComputer identity, properties and server selection](https://learn.microsoft.com/en-us/powershell/module/activedirectory/get-adcomputer) and [.NET name-resolution behavior](https://learn.microsoft.com/en-us/dotnet/api/system.net.dns.gethostaddresses).
