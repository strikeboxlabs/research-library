---
name: needrestart
description: Report restart requirements after updates on an owned Linux system without restarting services. Use to distinguish outdated-process findings, kernel status, incomplete visibility and package security fixes.
---

# Report restart requirements

Read this entire SKILL.md before acting. Require the maintained distribution package, trusted administrator-managed configuration and the intended process namespace. Use the established permitted invocation; system-wide process inspection needs sufficient privileges. No conditional resources are required. Finish with findings, command status and visibility limits; a successful scan does not prove the system is fully patched.

Verify the installed package revision against the distribution's security status before a privileged scan. An upstream version banner alone can miss backported fixes. Configuration and scanning hooks are executable inputs, so do not load an acquired configuration to inspect it or broaden a restricted grant.

Define `needrestart_bin` as the verified installed executable. Select list-only restart mode explicitly:

~~~bash
"$needrestart_bin" -r l
~~~

`-r l` reports requirements without restarting services; `-r i` and `-r a` select different behavior. This mode still performs a scan and loads configuration. Preserve stderr and exit status. If privileges, package state or trusted configuration are unavailable, report that prerequisite instead of retrying with another execution context.

An **illustrative** `No services need to be restarted` concerns this completed scan's service findings. Kernel, containers and user sessions have separate results. Interpreter detection is heuristic; permissions, exclusions and namespace scope can leave gaps. A pending service result is a maintenance candidate, not proof it was restarted. Arrange any restart through the service's maintenance procedure and verify it separately.

See the [packaged manual](https://manpages.debian.org/trixie/needrestart/needrestart.1.en.html), [upstream detection model](https://github.com/liske/needrestart/blob/master/README.md) and the applicable distribution notice, such as [Ubuntu's security update record](https://ubuntu.com/security/notices/USN-7117-1).
