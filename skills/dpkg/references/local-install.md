# Install selected trusted local archives

Require the controlled Debian-family system, its permitted administrative context, an authorized installation and archives obtained through the established trusted distribution channel. Identify package names, complete versions, architectures and dependencies from archive metadata, rather than filenames. Compare their supplied digests and the system architecture; a transfer progress bar does not establish integrity.

Define `archives` as a Bash array of the exact inspected absolute archive paths, including any deliberately selected dependency archives. Record existing package state before changing it. In the intended privileged context:

~~~bash
dpkg --install "${archives[@]}"
install_status=$?
~~~

Installation can run maintainer scripts, replace files, configure packages and process triggers. Preserve its diagnostics and status. Dpkg does not fetch missing dependencies; an error can leave unpacked or partly configured packages. Resolve the specific dependency/version problem within the installation scope before retrying; avoid force flags or configuring every pending package.

For each selected package, define its exact `package` name, with an architecture qualifier when necessary:

~~~bash
dpkg --status "$package"
dpkg --audit "$package"
~~~

Retain both query statuses. Compare installed version/architecture with the intended artifacts. Then verify the requested executable separately: configured package state does not prove application behavior.

Reference: [dpkg installation, states and audit](https://manpages.debian.org/bookworm/dpkg/dpkg.1.en.html).
