---
name: bloodhound
description: Inspect an acquired directory graph in the installed BloodHound Legacy GUI on Linux. Use for local import, object identity and permission-edge interpretation while distinguishing capture coverage from current directory state.
---

# Inspect a captured graph locally

Read this entire SKILL.md before acting. Require a trusted installed Legacy GUI, compatible prepared Neo4j instance, its existing credentials and an acquired reviewed collection archive. Import changes that local graph store. Finish with import completion, selected objects/edges and capture limits; unavailable runtime or format compatibility remains a prerequisite gap.

Identify the installed generation and collector schema before opening the archive. This task uses the historical Linux desktop launcher, separate from the directory collector and the newer Community Edition deployment. Define `bloodhound_bin` as that installation's verified launcher:

~~~bash
"$bloodhound_bin"
~~~

Connect the GUI to the selected private Neo4j endpoint with its prepared credentials. Do not assume historical default passwords or start a second database over an existing store. A launcher/window alone does not establish database authentication. If this is CE, use its actual receiving-server workflow instead; the Legacy Neo4j login instructions do not apply.

Before import, record the archive digest, producer/schema, collection methods/time and known collection failures. Select an isolated owned graph store when mixing datasets would obscure attribution. Import the selected ZIP/JSON through the GUI's upload control, then retain completion/errors and object counts. A ZIP filename or successful upload is not proof that all records were accepted; avoid deleting an existing graph to hide an import failure.

Search for the fully qualified object and verify its SID/object type/domain before interpreting results. Record each selected edge's source, destination, type and capture context. A user marked owned is an annotation, not evidence of a valid credential or session. A missing edge can reflect incomplete methods/import/visibility rather than absence of that permission.

For a permission finding, compare the graph label with the captured applicable ACE, property/extended-right GUID, owner and inheritance/group context. `ForceChangePassword`, `GenericWrite` and `WriteOwner` represent different modeled rights; none records a completed password, attribute, ownership or membership change. Ownership/DACL control can depend on OWNER RIGHTS and object/server restrictions. A graph path is a set of evidence questions, not proof that the endpoint was reached or the rights remain current.

Retain only the selected redacted relation evidence and the archive/import provenance in the task result. Close the owned GUI and account for the imported local dataset according to the task's retention policy; closing it does not erase database records.

See the [Legacy project and generation guidance](https://github.com/SpecterOps/BloodHound-Legacy) and [Windows directory access masks](https://learn.microsoft.com/en-us/windows/win32/secauthz/access-rights-and-access-masks) when resolving format or permission interpretation. Legacy is deprecated; this procedure documents an existing installation rather than directing its installation.
