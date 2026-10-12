---
name: umask
description: Set or inspect Bash file-creation permissions for an owned job. Use when a mask set after creation or in another shell is mistaken for protection of an existing file.
---

# Set the mask before creating output

Read this entire SKILL.md before acting. Identify the actual creating shell/process and intended output access. No conditional resources are required. Finish with observed output mode/ACLs and the job result; a mask value is not an effective-access test.

In Bash, `type umask` distinguishes the builtin from a wrapper. `umask` prints the current mask. For a selected owned job, define `job` as its reviewed executable and supply only its intended arguments:

~~~bash
(
  umask 077 || exit
  "$job"
)
status=$?
~~~

The subshell scopes the change; the job inherits it. Without a default parent ACL, creation permissions are requested mode AND the complement of the mask. Ordinary requests of 0666/0777 with mask077 yield 0600/0700. A mask removes bits rather than adding them. Default ACL inheritance can change this calculation.

Set the mask **before** redirection, touch or another creation. It does not retroactively restrict existing files; reopening an existing output can retain its old permissions. Mask0006 removes other read/write but leaves other search/execute and group access. Inspect resulting metadata and parents; choose an explicit authorized chmod for an existing file. Do not test Linux permissions using Windows mode emulation.

Sources: [Bash builtin](https://manpages.debian.org/bookworm/bash/bash.1.en.html), [Linux creation and ACL behavior](https://manpages.debian.org/bookworm/manpages-dev/umask.2.en.html).
