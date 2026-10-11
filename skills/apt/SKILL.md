---
name: apt
description: Review and perform a selected interactive APT package installation on the controlled Linux image. Use when dependencies, package selection, stale indexes or a successful plan are confused with completed installation.
---

# Selected interactive package installation

Read this entire SKILL.md before acting. Require the controlled APT-based image, its trusted repository configuration and an exact package name. Review the proposal before the authorized installation; finish with transaction status and installed package/executable evidence. No conditional resources are required. Installing this skill does not install a package.

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

See the [packaged APT manual](https://manpages.debian.org/bookworm/apt/apt.8.en.html) and [simulation/installation options](https://manpages.debian.org/bookworm/apt/apt-get.8.en.html).
