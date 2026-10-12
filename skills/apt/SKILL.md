---
name: apt
description: Review and perform selected interactive APT installation or broken-dependency repair on the controlled Linux image. Use when package selection, incomplete dpkg state or a successful plan is confused with a completed transaction.
---

# Selected interactive package installation

Read this entire SKILL.md before acting. Require the controlled APT-based image and trusted repository configuration. Select an exact package for installation, or the known broken-dependency state for the repair branch below. Review the proposal before the authorized transaction; finish with status and resulting package/executable evidence. No conditional resources are required. Installing this skill does not install a package.

Define `package` as one exact repository package name, without patterns or action suffixes. Inspect the installed interface and current package metadata:

~~~bash
apt --version
apt show "$package"
apt --simulate install "$package"
~~~

Keep the selected version and proposed dependency changes. A simulation does not run installers or prove the program works; repository indexes and package state can change afterward. An unavailable candidate requires resolving the selected image/repository/metadata, not guessing a package from another distribution. Index refresh is a separate network and state change.

For the approved transaction in the permitted privileged context:

~~~bash
apt install "$package"
~~~

Review the actual prompt; dependencies and maintainer scripts can alter existing packages or services. Avoid copying an automatic `-y` from a walkthrough before that scope is understood. Record status and diagnostics: normal operation returns0, errors100. A download or simulation is not completed installation. Confirm the installed version and actual executable afterward; a package name need not equal its command name.

APT's interactive defaults/output can change across versions. Use its result as human-readable transaction evidence; choose the dedicated stable APT interfaces for automation rather than parsing apt's progress display. Lock, permission and dependency failures require their actual cause; deleting a lock file does not resolve its owner.

For a known incomplete local-archive installation, preserve the original dpkg diagnostics and inspect the proposed repair:

~~~bash
apt --simulate --fix-broken install
~~~

With no package argument, APT chooses a dependency solution across the current package database; it can configure, install or remove packages beyond the original archive. Review every proposed change against the authorized repair scope. In the permitted administrative context, the accepted repair is:

~~~bash
apt --fix-broken install
~~~

Retain transaction status, then recheck the affected package states and requested executable. No available solution remains an explicit dependency gap; forcing versions or removing packages is not an automatic retry. `--fix-missing` addresses retrieval problems and is a different option.

See the [packaged APT manual](https://manpages.debian.org/bookworm/apt/apt.8.en.html) and [simulation/installation options](https://manpages.debian.org/bookworm/apt/apt-get.8.en.html).
