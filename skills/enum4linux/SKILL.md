---
name: enum4linux
description: Inventory SMB share names/listing access or read returned domain password-policy metadata on a selected managed server with classic enum4linux. Use to distinguish partial helper results from complete access or effective per-account policy.
---

# Selected SMB share inventory

Read this entire SKILL.md before acting; reuse complete current context. Require classic enum4linux with Perl and its Samba helpers, the selected managed server and permitted session. Choose share inventory below or read [password-policy metadata](references/password-policy.md) fully for that task; its polenum dependency is additional. Finish with the selected metadata/access results and helper diagnostics. Missing dependencies, denied sessions or unparsed output are concrete gaps.

Check `enum4linux -h` and its version. Classic enum4linux is distinct from enum4linux-ng. The reviewed implementation checks for `nmblookup`, `net`, `rpcclient`, `smbclient` and `which`; its operation depends on their installed behavior too. Define `server` as the single selected hostname/address. Where the server intentionally permits an empty-user/password session:

~~~bash
enum4linux -S "$server"
~~~

`-S` selects share inventory; no task option enables broader default enumeration. The wrapper also establishes session/workgroup context and attempts directory listings on returned shares. A share name/comment is metadata, not a verified backing path or read permission. Mapping success and listing success are different results; unexpected helper output may be unparsed rather than absent.

Use the transcript's per-share results and errors. A successful directory listing does not establish write access. `-A` enables additional write tests; leave it out of this read-only task. If the empty session is denied, retain that result and select an approved authenticated client flow rather than guessing credentials or weakening SMB policy. This share task does not cover user/RID or share-name guessing.

Resolve flag and helper differences with the installed help and the [classic implementation](https://github.com/CiscoCXSecurity/enum4linux/blob/master/enum4linux.pl).
