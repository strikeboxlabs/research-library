---
name: enum4linux
description: Inventory SMB share names and listing access on an explicitly selected managed server using classic enum4linux. Use to interpret partial wrapper results and distinguish share metadata from actual file access.
---

# Selected SMB share inventory

Read this entire SKILL.md before acting; reuse complete current context. This task requires classic enum4linux with Perl and its Samba helper executables, a managed server and approval for share listing/access checks. Select the server and authentication context first. Finish with observed share names and separate mapping/listing results, preserving any denied or unparsed results. Missing dependencies or blocked sessions are prerequisite gaps. There are no conditional resources.

Check `enum4linux -h` and its version. Classic enum4linux is distinct from enum4linux-ng. The reviewed implementation checks for `nmblookup`, `net`, `rpcclient`, `smbclient` and `which`; its operation depends on their installed behavior too. Define `server` as the single selected hostname/address. Where the server intentionally permits an empty-user/password session:

~~~bash
enum4linux -S "$server"
~~~

`-S` selects share inventory; no task option enables broader default enumeration. The wrapper also establishes session/workgroup context and attempts directory listings on returned shares. A share name/comment is metadata, not a verified backing path or read permission. Mapping success and listing success are different results; unexpected helper output may be unparsed rather than absent.

Use the transcript's per-share results and errors. A successful directory listing does not establish write access. `-A` enables additional write tests; leave it out of this read-only task. If the empty session is denied, retain that result and select an approved authenticated client flow rather than guessing credentials or weakening SMB policy. This narrow task does not claim user/RID, password-policy or share-name guessing coverage.

Resolve flag and helper differences with the installed help and the [classic implementation](https://github.com/CiscoCXSecurity/enum4linux/blob/master/enum4linux.pl).
