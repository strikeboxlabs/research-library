---
name: kpcli
description: Open an authorized KeePass database with its known unlock material and browse its group and entry inventory without saving changes. Use when validating a database backup or distinguishing unlock errors from format incompatibility.
---

# Inspect the selected KeePass inventory

Read this entire SKILL.md before acting. Establish the authorized database copy, known master password and any required key file, plus the installed kpcli/backend format support. Finish with the actual open result and requested inventory or the specific prerequisite gap. This task has no additional required resources.

Keep the original unchanged and define `database` as an existing absolute working-copy path. Review the installed options, then start a session that prevents database edits and does not persist command history:

~~~bash
kpcli --help
kpcli --readonly --histfile /dev/null --kdb "$database"
~~~

When this database requires a known key file, add `--key "$key_file"`, defining that variable as its existing absolute path. Enter the master password at the console prompt; keep it out of command arguments and logs.

Inside kpcli, use `help`, `help cd` and `help ls` to confirm the interactive syntax. `ls` lists groups and entry titles at the current database location; `cd` changes the group, not the host filesystem directory. Use a displayed group path with completion, then `ls` again. Names containing spaces or slashes require kpcli's own path handling. Do not assume a database root/group name from a writeup.

An invalid-key-or-corrupt error does not discriminate between wrong unlock material, damaged input and unsupported database features. Recheck the exact copy, required key file, text encoding and installed backend's KDB/KDBX support before changing anything. Newer KDBX support depends on implementation and dependencies, not merely the .kdbx suffix. Report incompatibility instead of weakening or saving the original database to make it load.

Record only the requested inventory and observed result. Opening the database does not validate its stored credentials against any service. Avoid secret-display, export, edit and save commands during this inventory task.

See [kpcli's packaged manual](https://manpages.ubuntu.com/manpages/jammy/en/man1/kpcli.1.html) and [the packaged command/option implementation](https://sources.debian.org/src/kpcli/4.1.3-1/kpcli-4.1.3.pl/) for interactive commands and version-dependent support.
