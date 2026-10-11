---
name: dpkg
description: Inspect one Debian package's installation state and audit incomplete configuration with dpkg. Use when an install command or archive filename is mistaken for a completed usable installation.
---

# Check the selected package state

Read this entire SKILL.md before acting. Require installed dpkg, the intended live Debian-family package database and exact package name. No conditional resources are required. Finish with state, version, audit findings and query status; missing records leave installation unverified.

Confirm `dpkg --version` and help. Define `package` as the established package name, retaining an architecture qualifier when needed:

~~~bash
dpkg --status "$package"
status=$?
dpkg --audit "$package"
audit_status=$?
~~~

Check each diagnostic. Installed means unpacked/configured; unpacked, half-configured and pending triggers require separate resolution. Selection for installation or residual config-files does not establish installation. Audit checks database consistency, not application health or authenticity.

Compare the complete recorded version/architecture with the intended package. A filename is only a label. `dpkg -i` can execute maintainer scripts and leave an incomplete installation; do not repeat it, force dependencies or configure every pending package as a query repair. Application startup remains separate evidence.

Reference: [dpkg states and audit](https://manpages.debian.org/bookworm/dpkg/dpkg.1.en.html).
