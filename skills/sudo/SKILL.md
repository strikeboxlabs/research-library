---
name: sudo
description: Interpret sudo policy, RunAs identities, environment handling and sudoedit on Linux. Use when a permitted command behaves differently under sudo or a walkthrough overstates privilege from a policy listing.
---

# Understand the permitted operation

Read the effective listing before selecting an elevated command:

~~~bash
sudo -l
sudo -ll
~~~

Listing may require authentication. For unattended inspection, `sudo -n -l` fails instead of prompting; that failure does not by itself mean no policy entry exists. Record the target RunAs user/group, command path, argument restrictions and tags together. `(dev_admin : dev_admin)` is a permitted target identity, not a root grant.

`NOPASSWD` affects authentication for matching entries; it does not grant arbitrary commands. `SETENV` changes environment restrictions for the matching operation. `env_reset` and `secure_path` can explain why a program works normally but finds different variables or executables under sudo.

In command-argument patterns, sudoers wildcards can match whitespace and span arguments; `*` is not necessarily one filename. Interpret the actual permitted operation, including options. Package installers can execute hooks, and backup tools may execute a password-helper command. Restricting the executable name alone does not make their subcommands passive inspection. Preserve the effective policy and program semantics together before drawing a privilege conclusion.

`sudo -E` asks policy to preserve the **exported environment** and can be denied. A shell-only assignment such as `PYTHONPATH=/some/path` on its own need not be exported, so a following `sudo -E` failure does not prove that variable preservation is universally broken. Distinguish shell export state, sudo filtering and the target program's own startup rules. Preserve only the variable actually needed; inspect the permitted wrapper's imports, config and child commands before changing their environment.

For an authorized edit, define `run_as` as the permitted target user and `file` as the exact allowed absolute path:

~~~bash
sudoedit -u "$run_as" -- "$file"
~~~

`sudoedit` edits temporary copies as the invoking user, then uses privilege to copy changes back. It is different from launching an editor itself under sudo. A saved editor buffer does not prove the final copy-back succeeded; inspect errors and the resulting file. File/path safety checks can reject an otherwise listed edit.

When evaluating a historical sudo vulnerability, inspect the installed distribution package and its advisory/patch status. The upstream-looking string from `sudo --version` alone does not establish that a distro build is vulnerable. Record observed policy and behaviour separately from an exploitation hypothesis.

Documentation reviewed 2026-10-09; Linux execution untested. Cases: Admirer pp. 21–22; Agile pp. 20–22; Armageddon pp. 10–12; Artificial pp. 13–14. Sources: [sudo/sudoedit manual](https://github.com/sudo-project/sudo/blob/main/docs/sudo.man.in), [sudoers environment and policy](https://github.com/sudo-project/sudo/blob/main/docs/sudoers.man.in), [Ubuntu's package-specific sudoedit fixes](https://ubuntu.com/security/CVE-2023-22809), [snap hooks](https://snapcraft.io/docs/reference/development/supported-snap-hooks/), [restic credential helpers](https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html).
