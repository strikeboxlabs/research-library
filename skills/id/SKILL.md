---
name: id
description: Inspect current Linux process real/effective user and group IDs with GNU id. Use to verify an execution identity without confusing a prompt, group list or named account lookup with effective privilege.
---

# Establish the current execution identity

Read this entire SKILL.md before acting. Run the identity check in the actual session/process context being examined, and distinguish it from a named-account database lookup. Finish with numeric real/effective IDs and relevant group context; UID zero alone does not establish every requested capability or another process's identity.

For the current shell's execution context:

~~~bash
id --version
id
id -u
id -ru
id -g
id -rg
id -G
~~~

GNU `-u` and `-g` print the effective user and primary group IDs; `-r` selects their real IDs. `-G` lists group IDs, including supplementary membership. Check each status and preserve numeric output. Names can depend on account lookup and namespace; `-n` chooses names for these selectors, not a stronger identity check. A shell-launch wrapper may change IDs before id runs, so correlate a discrepancy with that launch rather than claiming the parent has identical IDs.

An **illustrative** `uid=0(root) gid=1000(worker) groups=1000(worker)` indicates UID zero with that primary/supplementary group context. It is not evidence that GID became zero. When real/effective IDs differ, ordinary id includes the differences; record both explicitly with the selectors above. A root-looking prompt or readable flag filename is weaker than the actual identity observation.

For a selected existing account, define `user` and query `id -- "$user"`. This describes the account database's IDs/groups, not a running process, authentication success or the caller's effective identity. A lookup failure can reflect unavailable name services or that account's absence in this namespace; it is not a password verdict.

User namespaces, capabilities, filesystem/mount policy and mandatory access controls can constrain what a UID-zero process can do. Use identity as evidence for the current action, then test the requested authorized capability separately when needed. Keep before/after identity checks tied to the same session and launch; an independent shell or later process may differ.

See [GNU id options and named-account semantics](https://www.gnu.org/software/coreutils/manual/html_node/id-invocation.html) and [upstream implementation](https://github.com/coreutils/coreutils/blob/master/src/id.c).
