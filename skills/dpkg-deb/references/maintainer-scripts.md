# Package hooks and installer authority

`DEBIAN/preinst`, `postinst`, `prerm` and `postrm` are executable control scripts. Building a .deb does not run them; an installer runs relevant hooks at defined stages, normally with root authority on an ordinary system installation. A backend allowed to install a caller-supplied package can therefore delegate code execution through its hooks, even if the backend shell-quotes package filenames correctly. This is a package-trust/privilege boundary, distinct from shell injection into the filename.

## Prepare a minimal controlled hook package

For an authorized installation test, choose a fresh `tree` and output `deb`, and a unique package name that does not collide with an installed package. This **illustrative fixture** has no data payload or persistent privilege change; it prints a marker and the hook's actual identity into the installer's output. Adapt the package metadata to the controlled task:

~~~bash
umask 077
mkdir -p -- "$tree/DEBIAN"
cat >"$tree/DEBIAN/control" <<'CONTROL'
Package: owned-hook-probe
Version: 0.1
Architecture: all
Maintainer: Test Operator <operator@example.invalid>
Description: Controlled installer hook identity probe
CONTROL
cat >"$tree/DEBIAN/postinst" <<'HOOK'
#!/bin/sh
set -e
case "$1" in
  configure)
    printf '%s\n' 'owned-hook-probe: configure'
    id
    ;;
esac
exit 0
HOOK
chmod 0755 "$tree/DEBIAN/postinst"
chmod 0644 "$tree/DEBIAN/control"
chmod 0755 "$tree/DEBIAN"
dpkg-deb --build --root-owner-group "$tree" "$deb"
~~~

Use the entrypoint's archive/control inspection afterward. The chosen tree must be dedicated and fresh; these writes replace its selected control files. Installing this package still changes the package database even though the hook only prints evidence. Hand it to the explicitly selected installer only within that task's authorization, retain the archive identity and collect the installer/job result. A marker without the same job/package association is weak evidence; a permission denial or missing hook output is not a completed privilege test.

For an existing production package, preserve its required payload and configuration procedure rather than replacing its hook with this fixture. Inspect shebang, executable mode, command paths/environment, case arguments and error handling. `postinst configure` is a specific configuration stage; hooks can also be invoked for recovery/error transitions. Use documented arguments and idempotent changes so a retry does not compound damage. Scripts must handle missing prerequisites and return meaningful status; printing success before a failed operation is insufficient.

## Interpret installation effects

A hook can modify privileged file permissions or launch processes as its installer. If a task deliberately tests such a change, retain the before/after owner/mode, exact changed artifact and observed resulting capability, and account for restoration. A setuid bit alone does not demonstrate a resulting effective UID: filesystem `nosuid`, process restrictions, executable behavior and namespace boundaries can change the result. Bash privileged mode preserves an already supplied effective identity; it does not grant one. Prefer the selected capability's direct evidence over a root-looking prompt.

A local archive can be complete while the installer fails on dependencies, locks, conflicts or a hook error. Do not rebuild/reinstall blindly after a partial configuration: inspect the package/job state and actual last stage first. Extracting a hook for review is different from running it directly, which skips installer arguments/environment and can itself change the system. Removal/purge is also an installer operation with possible hooks, not automatic harmless cleanup.

References: [Debian maintainer-script stages and errors](https://www.debian.org/doc/debian-policy/ch-maintainerscripts.html), [maintainer-script interface](https://www.debian.org/doc/debian-policy/ch-maintainerscripts.html#summary-of-ways-maintainer-scripts-are-called) and [Bash privileged invocation](https://www.gnu.org/software/bash/manual/html_node/Invoking-Bash.html).
