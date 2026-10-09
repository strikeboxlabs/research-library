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

An additional PAM prompt can be a separate authentication requirement, not another request for the account password. Inspect readable `/etc/pam.d/sudo` and its included stacks when diagnosing it. A failed `required` module can still allow later prompts before the stack rejects authentication. Keep authentication failure distinct from sudo policy denial; an interrupted challenge does not establish the effective policy. Diagnose the configured requirement without editing PAM to bypass it.

`NOPASSWD` affects authentication for matching entries; it does not grant arbitrary commands. `SETENV` changes environment restrictions for the matching operation. `env_reset` and `secure_path` can explain why a program works normally but finds different variables or executables under sudo.

In command-argument patterns, sudoers wildcards can match whitespace and span arguments; `*` is not necessarily one filename. Interpret the actual permitted operation, including options. Package installers can execute hooks, and backup tools may execute a password-helper command. Build/runtime commands such as `dotnet run` can execute a selected project's build logic and application. `iptables-save -f` writes the selected file with the program's privileges, unlike redirection performed by the invoking shell. Restricting the executable name alone does not make its subcommands passive inspection. Preserve the effective policy and program semantics together before drawing a privilege conclusion.

`sudo -E` asks policy to preserve the **exported environment** and can be denied. A shell-only assignment such as `PYTHONPATH=/some/path` on its own need not be exported, so a following `sudo -E` failure does not prove that variable preservation is universally broken. Distinguish shell export state, sudo filtering and the target program's own startup rules. Preserve only the variable actually needed; inspect the permitted wrapper's imports, config and child commands before changing their environment.

For an authorized edit, define `run_as` as the permitted target user and `file` as the exact allowed absolute path:

~~~bash
sudoedit -u "$run_as" -- "$file"
~~~

`sudoedit` edits temporary copies as the invoking user, then uses privilege to copy changes back. It is different from launching an editor itself under sudo. A saved editor buffer does not prove the final copy-back succeeded; inspect errors and the resulting file. File/path safety checks can reject an otherwise listed edit.

When evaluating a historical sudo vulnerability, inspect the installed distribution package and its advisory/patch status. The upstream-looking string from `sudo --version` alone does not establish that a distro build is vulnerable. Record observed policy and behaviour separately from an exploitation hypothesis.


For a permitted `git pull`, include the working directory in the policy assessment. The chosen repository can supply local configuration and executable hooks, so an exact executable/subcommand restriction alone does not establish a passive update. A Linux `post-merge` hook may run after a successful merge-path update, including a fast-forward; an already-current checkout or conflicted merge is different. Inspect the selected repository, effective hook path, script and ownership checks before concluding that a listed grant permits execution of a particular hook. A GitLab webhook merely explains what launched the local command; it is not that local hook. Do not invoke the elevated pull just to discover its effects.

Consult the [sudoers policy manual](https://github.com/sudo-project/sudo/blob/main/docs/sudoers.man.in) for command matching and [Git's hook events](https://git-scm.com/docs/githooks) for the permitted program's behavior.
