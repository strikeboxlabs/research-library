---
name: getent
description: Resolve Linux users and groups through NSS when local passwd/group files omit an identity, or group listings differ from a running session's privileges.
---

# Resolve the identity the system actually uses

Read this entire SKILL.md before acting; reuse complete current context. Query the known identity before enumerating a directory. Finish with the resolved account/group, lookup status and whether the evidence describes the directory or this process.

An account can resolve through LDAP/SSSD or another Name Service Switch provider without a row in `/etc/passwd`. A large UID or home-directory name alone does not identify that provider. `getent` uses the configured NSS sources; it does not test the account's password.

Define `account` and `group_name` as the exact observed names:

~~~bash
getent passwd "$account"
getent group "$group_name"
getent initgroups "$account"
~~~

The passwd row carries the name, password placeholder, UID, primary GID, comment, home and shell. A numeric passwd key looks up a UID; a numeric group key looks up a GID. Preserve names and numbers together. The group row's member list does not necessarily enumerate users whose **primary** GID is that group; `initgroups` asks for the selected account's group list instead.

Compare `id "$account"` (the named identity) with bare `id` (the invoking process). Changes in the directory need not update supplementary groups already held by a session. A named group or listed membership alone does not prove socket access; combine the process's effective identity with the socket's ownership/mode and selected service context.

**Illustrative:** `engineer:*:502:alice,bob` identifies GID 502 and two listed members. It neither grants the current worker GID 502 nor proves every member can reach a particular Docker daemon.

Status 2 means at least one requested key was not found; an NSS/backend outage, configuration, cache or visibility issue can still explain the missing result. Status 1 denotes an argument/unknown-database problem; 3 denotes unsupported enumeration. A bare `getent passwd` can omit remote accounts when enumeration is disabled even though a keyed lookup succeeds. Inspect the applicable `passwd`, `group` and `initgroups` rules in `/etc/nsswitch.conf` before treating a local-file search as a directory inventory. Do not flush caches or restart identity services just to force a result.

See [getent lookup semantics and status](https://man7.org/linux/man-pages/man1/getent.1.html) and [NSS configuration](https://man7.org/linux/man-pages/man5/nsswitch.conf.5.html).
