---
name: rpm
description: Query the installed RPM database for a selected Linux package and retain its full version, release and architecture. Use when a vulnerability claim relies on an upstream version while distribution backports or a different package change applicability.
---

# Identify the installed package build

Read this entire SKILL.md before acting. Confirm that the selected machine uses an RPM database and select the actual package name, independently of a walkthrough's prose. No conditional resources are required. Finish with the query status, complete package identity and applicable distribution advisory; unavailable metadata leaves patch status unresolved.

Check `rpm --version` and installed help. Define `package` as the exact known installed package name, then query that database:

~~~bash
rpm -q -- "$package"
rpm -q --queryformat '%{NAME} %{EPOCH}:%{VERSION}-%{RELEASE}.%{ARCH}\n' -- "$package"
~~~

Preserve each command's status and diagnostics. Multiple returned builds/architectures are separate installed records. An absent epoch can print `(none)`; retain it rather than silently changing the version. A failed query can mean a missing package or an inaccessible/wrong database, not proof that the host is unaffected. A container's database describes that container, not the host installation.

Use `-q` with the selected package name for this task. `-qa` selects all installed packages; optional selector/pattern rules differ by RPM version, so a copied `rpm -qa package` spelling should not be assumed equivalent to exact package selection. `-qp` instead examines an RPM file and does not establish that it is installed.

Match the full epoch/version/release/architecture and distribution stream against its vendor advisory. Distribution fixes may preserve the upstream version while changing the release; do not classify all builds below an upstream threshold as vulnerable. A package query establishes database metadata, not that a particular daemon has restarted onto those files, that every exploit prerequisite exists or that exploitation succeeded. Keep a synopsis naming one component separate from a screenshot querying another.

See the [upstream RPM query manual](https://rpm.org/docs/6.0.x/man/rpm.8) for installed-version selectors and query formatting, and the [Red Hat explanation of security backports](https://access.redhat.com/security/cve/cve-2021-3560) when interpreting that distribution's package status.
