---
name: groups
description: Inspect the current Linux process group names or a selected account lookup with GNU groups. Use to distinguish live session membership from directory membership and application authorization.
---


# Read the group context that matters

Read this entire SKILL.md before acting. Choose current process membership or a named-account lookup deliberately. Finish with that context and observed groups; membership alone does not prove login or sudo authority.

~~~bash
groups
~~~

With no account arguments, GNU groups reports primary/supplementary groups of the current process. `groups "$account"` instead looks up that account through the configured name service. Newly changed directory groups need not appear in an existing session; an NSS lookup and the process's inherited group list can legitimately differ. Use `id -G` for numeric IDs when names are ambiguous.

An **illustrative** `domain users linux_admins` response identifies group names, not their policy meaning. Inspect the relevant access provider and sudo policy: an SSSD `simple_allow_groups` entry applies when the simple provider is selected, while `sudo -l` describes a different permission decision. Neither the group name nor AD membership alone guarantees every Linux service accepts that account.

On Debian-style systems, `adm` commonly permits reading many system logs; it is distinct from `sudo` and the root identity. Use actual file ownership/modes/ACLs and the current process group context to select readable logs. A denied file or inaccessible parent can still limit that access. Log records can contain user-supplied query or authentication fields, so group access may expose sensitive evidence without establishing those values' owners or present validity. See the [Debian group definitions](https://sources.debian.org/src/base-passwd/3.5.51/doc/users-and-groups.sgml).

See [GNU group lookup semantics](https://github.com/coreutils/coreutils/blob/master/doc/coreutils.texi) and [implementation](https://github.com/coreutils/coreutils/blob/master/src/groups.c).
