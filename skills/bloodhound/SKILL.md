---
name: bloodhound
description: Import and inspect acquired directory evidence in BloodHound CE or the installed Legacy GUI on Linux. Use for generation-compatible ingestion, object identity and permission-edge interpretation while distinguishing capture coverage from current directory state.
---

# Inspect a captured graph locally

Read this entire SKILL.md before acting. Require an acquired reviewed collection archive and the selected prepared receiving instance. For CE, read [CE file ingestion](references/ce-file-ingest.md) fully before upload; use the Legacy procedure below only for its installed GUI and compatible prepared Neo4j instance. Import changes the receiving graph store. Finish with import completion, selected objects/edges and capture limits; unavailable runtime or format compatibility remains a prerequisite gap.

Identify the installed generation and collector schema before opening the archive. This task uses the historical Linux desktop launcher, separate from the directory collector and the newer Community Edition deployment. Define `bloodhound_bin` as that installation's verified launcher:

~~~bash
"$bloodhound_bin"
~~~

Connect the Legacy GUI to the selected private Neo4j endpoint with its prepared credentials. Do not assume historical default passwords or start a second database over an existing store. A launcher/window alone does not establish database authentication.

Before import, record the archive digest, producer/schema, collection methods/time and known collection failures. Select an isolated owned graph store when mixing datasets would obscure attribution. Import the selected ZIP/JSON through the GUI's upload control, then retain completion/errors and object counts. A ZIP filename or successful upload is not proof that all records were accepted; avoid deleting an existing graph to hide an import failure.

Search for the fully qualified object and verify its SID/object type/domain before interpreting results. Record each selected edge's source, destination, type and capture context. A user marked owned is an annotation, not evidence of a valid credential or session. A missing edge can reflect incomplete methods/import/visibility rather than absence of that permission.

For a permission finding, compare the graph label with the captured applicable ACE, property/extended-right GUID, owner and inheritance/group context. `ForceChangePassword`, `GenericWrite` and `WriteOwner` represent different modeled rights; none records a completed password, attribute, ownership or membership change. `GenericAll` concerns full control of the selected directory object. A computer object, domain object and host execution token are distinct; a GenericAll edge to a DC computer does not itself grant every privilege on that machine. A summary count describes modeled relations in this capture, not every effective right. Ownership/DACL control can depend on OWNER RIGHTS and object/server restrictions. A graph path is a set of evidence questions, not proof that the endpoint was reached or the rights remain current.

For replication-permission findings, retain each contributing edge to the same selected domain. `GetChangesAll` alone is not the complete DCSync relationship: the model combines it with `GetChanges`. Verify both captured rights, principal/group context and capture time before reporting the combined exposure. This graph interpretation does not require retrieving directory secrets. See the [GetChangesAll edge definition](https://bloodhound.specterops.io/resources/edges/get-changes-all).

For a captured `ReadLAPSPassword` relation, retain the destination computer and the applicable LAPS generation/account policy. Legacy `ms-Mcs-AdmPwd` and Windows LAPS `msLAPS-Password` are different schema attributes; encrypted Windows LAPS storage introduces further conditions. These describe a managed device account, not arbitrary domain users' passwords. On a domain controller, distinguish any DSRM policy/account from an ordinary local account and from a domain Administrator login. A graph edge, computer DN or account's display name alone does not prove that login. Review the owner's schema/policy and redacted capture without retrieving password values. See [Microsoft's schema and account fields](https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-technical-reference).

Retain only the selected redacted relation evidence and the archive/import provenance in the task result. Close the owned GUI and account for the imported local dataset according to the task's retention policy; closing it does not erase database records.

An `adminCount` value describes directory ACL-protection metadata associated with administrative-group history. It is not the current Domain Admins membership list, an execution token or proof of WMI/WinRM access. Reconcile the selected captured memberships, applicable permission edges and service authorization before making an access claim. See [Admin-Count semantics](https://learn.microsoft.com/en-us/windows/win32/adschema/a-admincount).

See the [Legacy project and generation guidance](https://github.com/SpecterOps/BloodHound-Legacy) and [Windows directory access masks](https://learn.microsoft.com/en-us/windows/win32/secauthz/access-rights-and-access-masks) when resolving format or permission interpretation. Legacy is deprecated; this procedure documents an existing installation rather than directing its installation.
