---
name: dpkg
description: Install selected trusted local Debian archives, remove an explicitly selected owned package or inspect package state with dpkg. Use when archive identity, dependencies or incomplete configuration obscure the resulting state.
---

# Check the selected package state

Read this entire SKILL.md before acting. Require installed dpkg, the intended live Debian-family package database and exact package name. For an authorized local archive installation, read [selected local installation](references/local-install.md) fully first. For removal, establish the selected installed package and permitted removal effects before the branch below. Finish with state, version, audit findings and query status; missing records or failed transactions leave the requested state unverified.

Confirm `dpkg --version` and help. Define `package` as the established package name, retaining an architecture qualifier when needed:

~~~bash
dpkg --status "$package"
status=$?
dpkg --audit "$package"
audit_status=$?
~~~

Check each diagnostic. Installed means unpacked/configured; unpacked, half-configured and pending triggers require separate resolution. Selection for installation or residual config-files does not establish installation. Audit checks database consistency, not application health or authenticity.

Compare the complete recorded version/architecture with the intended package. A filename is only a label. `dpkg -i` can execute maintainer scripts and leave an incomplete installation; do not repeat it, force dependencies or configure every pending package as a query repair. Application startup remains separate evidence.

If reviewing `dpkg -l` output, its first columns are desired action, current state and error. **Illustrative** `hi` means held and installed, rather than half-installed; uppercase `H` is the distinct half-installed state. A whole-row grep can match descriptions/other names, and the human display can truncate fields. Use the exact-package status query above before mapping a version to a patch decision. A host package version does not identify a nested VM/container's actual runtime build. See [listing states](https://manpages.debian.org/bookworm/dpkg/dpkg-query.1.en.html).

For removal of that explicitly selected owned package, preserve its prior state and use the permitted administrative context:

~~~bash
dpkg --remove "$package"
remove_status=$?
dpkg --status "$package"
~~~

Removal runs maintainer scripts/triggers and removes installed files while normally retaining conffiles; it is not purge or deletion of every user-created artifact. Dependencies can prevent removal. Retain diagnostics and the resulting config-files/not-installed state or absence of a record; do not force removal or select all pending packages to hide a failure. An acquired .deb remains readable independently of the installed application's removal.

Reference: [dpkg states, removal and audit](https://manpages.debian.org/bookworm/dpkg/dpkg.1.en.html).
