---
name: whoami
description: Read the effective Linux user name with GNU whoami. Use to identify the current execution context without confusing a prompt or account name with real UID or Windows token privileges.
---


# Identify the effective user

Read this entire SKILL.md before acting. Run the check in the actual session being examined. Finish with its observed effective user and any unresolved name lookup; a username does not establish all permissions.

~~~bash
whoami
~~~

GNU whoami prints the name associated with the process's effective UID, equivalent to `id -un`. For real/effective numeric IDs, run `id -u` and `id -ru` in the same context. A lookup error is not an authentication failure. A privileged wrapper or a new shell can change identity before the command executes.

An **illustrative** `postgres` result identifies the effective account name in this namespace; it does not imply database superuser rights, root or any particular group. Shell `whoami & hostname` backgrounds the first command, so output order cannot map each line reliably; run the two sequentially when correlating identity and host.

This is GNU's Linux command. Windows `whoami /user`, `/groups` and `/priv` inspect different token properties on the remote Windows host; those switches do not apply here. See the [GNU manual source](https://github.com/coreutils/coreutils/blob/master/doc/coreutils.texi) and [implementation](https://github.com/coreutils/coreutils/blob/master/src/whoami.c).
