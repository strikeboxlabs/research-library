---
name: pacman
description: Inspect Arch package archives and installed package ownership with pacman without installing them. Use when package metadata, payload lists, install scriptlets or transaction hooks affect a change or sudo-policy assessment.
---

# Inspect a package before choosing a transaction

Check `pacman --version` and `pacman -Q --help`. Define `package` as an existing absolute path to a package archive. Query its metadata and payload list:

~~~bash
pacman -Qip -- "$package"
pacman -Qlp -- "$package"
~~~

Here `-Q` selects query and `-p` means a package file rather than an installed database entry. Check the reported name, version, architecture, dependencies and install-script indication alongside file paths. These queries do not install the archive. An empty-looking payload or successful metadata parse does not establish that installation has no side effects or that the package is trustworthy.

Use an available libarchive `bsdtar` to inspect archive metadata members as text:

~~~bash
bsdtar -tf "$package"
~~~

If the listing contains an install script, define `member` as its exact listed name, commonly `.INSTALL`, then print that member without extracting files into the system:

~~~bash
bsdtar -xOf "$package" "$member"
~~~

Read it without sourcing or executing it. `PKGBUILD` is executable build input consumed by `makepkg`; pacman installs the resulting package archive. A PKGBUILD's `install=` file becomes package install-script content. Functions such as `post_install` and `post_upgrade` can run during package transactions. Separately, ALPM `.hook` files have triggers and PreTransaction/PostTransaction actions. Review both mechanisms when predicting a transaction's effects; one is not evidence of the other's content.

**Illustrative:** metadata reports an install script while the payload list contains only directories. Inspect the script before concluding the package does nothing. A console message about post-transaction hooks does not describe every package scriptlet that ran. The absence of `.INSTALL` also does not rule out triggered system hooks or file replacement.

For a selected existing file, define `path` as its absolute path and identify the installed package:

~~~bash
pacman -Qo -- "$path"
~~~

Ownership is a database association, not proof that the current bytes or permissions still match the package. Retain the package identity and investigate discrepancies separately. `pacman -U` installs or upgrades a local archive and can run code with the transaction's privileges; it is not a preview command. Unrestricted sudo access to it is therefore broader than permission to inspect metadata. Do not use installation to inspect an unknown archive.

Use the [pacman query manual](https://man.archlinux.org/man/pacman.8.en), [PKGBUILD install-script reference](https://man.archlinux.org/man/PKGBUILD.5.en) and [ALPM hook reference](https://man.archlinux.org/man/alpm-hooks.5.en) to resolve operation-specific behavior.
