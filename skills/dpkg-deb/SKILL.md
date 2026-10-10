---
name: dpkg-deb
description: Build or inspect a selected Debian binary package with dpkg-deb. Use for control metadata, filesystem ownership, maintainer-script review and distinguishing archive creation from privileged installation.
---

# Debian package archives

Read this entire SKILL.md before acting; reuse complete current context. Select inspection or building below. For a package with installation hooks, read [maintainer scripts](references/maintainer-scripts.md) fully before preparing or handing it to an installer. Finish with a valid archive and inspected metadata/members; building or extracting does not install it or prove its scripts ran.

Check `dpkg-deb --version` and local help. Define `deb` as the selected existing absolute archive, and `control_dir` as a fresh private working directory:

~~~bash
umask 077
dpkg-deb --info "$deb"
dpkg-deb --contents "$deb"
dpkg-deb --control "$deb" "$control_dir"
~~~

Check each status. `--control` extracts control files, including hooks, without executing them; read those files as data. `--contents` lists the data archive, so it does not reveal every control script. `--extract` unpacks data into a chosen directory without updating the package database or running hooks; extracted executables remain untrusted. Keep extraction in a fresh ordinary-user workspace. Archive checks are not a sandbox for malformed input.

## Build a selected package tree

Define `tree` as a reviewed absolute staging directory and `deb` as a fresh absolute output outside it. The tree needs `DEBIAN/control` with the actual Package, Version, Architecture, Maintainer and Description, plus any intended payload under its final relative filesystem paths. Use `Architecture: all` only for architecture-independent content, not to hide a native binary's ABI requirement. Review file modes, symlinks and hooks before packaging.

For a tree whose data members should all be owned by root, dpkg 1.19.0+ supports an ordinary-user build:

~~~bash
dpkg-deb --build --root-owner-group "$tree" "$deb"
~~~

This sets ownership recorded in the data archive; it does not change the builder's UID or run a root command. Do not use it for a package needing non-root member ownership. On an older build, use the image's established packaging workflow rather than claiming ordinary staging-file ownership is correct. Keep the normal metadata/script checks enabled; `--no-check` does not repair invalid content.

Require a successful build, then inspect the resulting archive using the commands above and record its digest/size for transfer. A package name/version from `--info` is a declaration, not provenance. Dependency resolution, file conflicts, package database state, hook execution and configuration belong to the selected installer and need separate results.

See the [dpkg-deb manual](https://manpages.debian.org/trixie/dpkg/dpkg-deb.1.en.html) for installed-version options and [Debian binary control fields](https://www.debian.org/doc/debian-policy/ch-controlfields.html) for metadata rules.
