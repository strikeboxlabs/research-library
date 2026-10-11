---
name: apt-get
description: Plan and perform a selected package installation with APT, distinguishing simulated dependency changes, repository trust and actual installer completion.
---

# Install one selected APT package

Read this entire SKILL.md before acting. Require the intended controlled Linux image, trusted existing APT configuration/repositories and the exact package name. Simulation supports planning; installation additionally requires authorization for the proposed dependency/configuration changes and sufficient privileges. For a repository/proxy/authentication or package-identity discrepancy, read [repository evidence](references/repository-evidence.md) fully before diagnosing it. That resource is conditional. Finish with the selected transaction, actual status and installed-version evidence or the unresolved failure.

Define `apt_get_bin` as the intended APT executable and `package` as one exact repository package name. Inspect this version's help and current metadata before planning:

~~~bash
"$apt_get_bin" --version
"$apt_get_bin" --help
"$apt_get_bin" --simulate install "$package"
~~~

Keep the proposed new, upgraded and removed packages and diagnostics. An **illustrative** `Inst example-tool ...` is a planned unpack operation; `Conf` is configuration and `Remv` is removal. Simulation does not install anything, test maintainer scripts or prove the application works. It disables locking, and a non-root simulation may miss inaccessible configuration. Reconcile stale metadata or changing package state before relying on the plan; refreshing repository indexes is a separate network/state change.

For the already authorized transaction, run in the approved privileged context:

~~~bash
"$apt_get_bin" install "$package"
~~~

Review the actual proposal before accepting its prompt. Dependencies and maintainer scripts can change more than the selected executable, including service state. Existing packages can be upgraded by `install`; avoid treating it as an unconditional new-package-only operation. Do not add unauthenticated repositories or bypass integrity checks to fix a download failure.

Preserve exit status and errors: normal operation returns 0, errors 100. A successful simulation, cached download or printed command is not completed installation. After a successful transaction, reconcile the package-manager record and intended executable/version; a missing command can concern PATH or package contents rather than require another install. Locks, permission, repository and broken-dependency errors require their own diagnosis, not blind retries or deleting lock files.

See the [APT command and simulation contracts](https://manpages.debian.org/testing/apt/apt-get.8.en.html).
