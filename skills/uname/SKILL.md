---
name: uname
description: Read the current kernel release and machine identity with GNU uname. Use when a login banner, installed kernel package or file timestamp is being mistaken for the running kernel.
---

# Read kernel identity in the actual execution context

Read this entire SKILL.md before acting. Establish which host/container/session runs the command and confirm GNU coreutils with `uname --version`; no conditional resources are required. Finish with the selected fields, command status and execution context. Missing execution evidence remains unresolved; an old banner is not a current kernel query.

For the current kernel name, release and machine hardware name:

~~~bash
LC_ALL=C uname -s -r -m
status=$?
~~~

Check stderr and `status`. The three fields answer which kernel identity this process sees. `-r` is the kernel release; `-v` instead prints its version/build string. With no options, GNU uname prints only the kernel name. Use `uname -a` when the additional node/build/OS fields matter, retaining the full output rather than parsing it as a fixed column table; some fields can contain spaces and unknown processor/platform fields may be omitted.

The result does not enumerate installed kernel packages, establish the Linux distribution, show every security backport or identify a future boot's kernel. Check the actual distribution/package metadata when those are the question. A container usually shares its host kernel, while its userspace can belong to another distribution; retain that context. Machine hardware naming also does not establish that an arbitrary binary's architecture, loader or libraries will run here.

A release string is a lead for matching vendor support/advisory records, not proof that a particular vulnerability is present. Vendor patches and configuration can differ without the upstream version alone expressing them. A login message, filesystem mtime or source screenshot has its own time/context and cannot replace a fresh query.

See the packaged [GNU uname manual](https://manpages.debian.org/bookworm/coreutils/uname.1.en.html).
