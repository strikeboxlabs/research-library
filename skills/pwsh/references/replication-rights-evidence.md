# Interpret captured AD replication ACE records

Require an already acquired complete permission record and its collection context. Preserve the target object's DN, trustee SID, ACE qualifier/type, access mask, object-right GUID, inheritance/object flags and whether the display resolved GUID names. A command name such as `Get-ObjectACL` does not establish its module/version or that it ran; use the package parser when reviewing the original PowerShell source instead of importing it.

Keep the target object's SID distinct from an ACE's `SecurityIdentifier`: the latter identifies the trustee. Match complete SIDs, not a RID or friendly-name fragment. A matching `whoami /user` observation associates that session with the SID at that time, while group membership and effective token contents remain separate.

An allowed object-specific `ExtendedRight` ACE for `DS-Replication-Get-Changes-All` is a significant permission observation on the recorded object. It is insufficient alone to establish effective replication access. Microsoft's permission logic first checks `DS-Replication-Get-Changes` on the naming-context root; additional checks depend on the requested attribute set, including secret and filtered attributes. Preserve that distinction when a writeup equates a single printed ACE with complete access.

Assess the full descriptor, target naming context, applicable inheritance and the actual principal/group token before a conclusion about effective permissions. A source filter selecting `GenericAll` or a replication-name fragment discards other ACEs; a cropped match omits contrary or supporting evidence. An unresolved GUID is not proof of absent rights, and `IsInherited=False` only describes the observed ACE.

Finish with the precise permission observation and missing effective-access facts. Reviewing captured records does not retrieve directory secrets, grant rights or validate an old live AD module on Linux PowerShell.

References: [MS-DRSR permission logic](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-drsr/15bbda52-7742-4ce3-9327-018647b0fc26), [object-specific ACE fields](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-access_allowed_object_ace), and [access checks](https://learn.microsoft.com/en-us/windows/win32/secauthz/how-dacls-control-access-to-an-object).
