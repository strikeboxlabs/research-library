---
name: sudo
description: Interpret sudo policy, RunAs identities, helper paths, environment handling and sudoedit on Linux. Use when a permitted command behaves differently under sudo or a walkthrough overstates privilege from a policy listing.
---

# Understand the permitted operation

Read this entire SKILL.md before acting; reuse complete current context. Establish the exact RunAs identity, command/argument restrictions and authentication tags. For scripts, helpers, environment-dependent children, Git hooks, SSH client commands or Python module presets, read [permitted-program behavior](references/permitted-programs.md) fully before attributing privilege. Finish with the policy and supported effects; listing a command is not an executed result.

Read the effective listing before selecting an elevated command:

~~~bash
sudo -l
sudo -ll
~~~

Listing may require authentication. For unattended inspection, `sudo -n -l` fails instead of prompting; that failure does not by itself mean no policy entry exists. Record the target RunAs user/group, command path, argument restrictions and tags together. `(dev_admin : dev_admin)` is a permitted target identity, not a root grant.

An additional PAM prompt can be a separate authentication requirement, not another request for the account password. Inspect readable `/etc/pam.d/sudo` and its included stacks when diagnosing it. A failed `required` module can still allow later prompts before the stack rejects authentication. Keep authentication failure distinct from sudo policy denial; an interrupted challenge does not establish the effective policy. Diagnose the configured requirement without editing PAM to bypass it.

`NOPASSWD` affects authentication for matching entries; it does not grant arbitrary commands. `SETENV` changes environment restrictions for the matching operation. `env_reset` and `secure_path` can explain why a program works normally but finds different variables or executables under sudo.

A sudoers command entry with no argument specification permits any arguments; an explicit `""` argument specification permits none. Thus a path-only daemon grant can include options selecting a different configuration. For Nginx, inspect permitted `-c`/`-g` inputs, included files and module paths: configuration controls worker identities, listeners and file operations. Record that authority without launching a replacement privileged service. A configuration-test flag does not make arbitrary module/configuration loading passive.

In command-argument patterns, sudoers wildcards can match whitespace and span arguments; `*` is not necessarily one filename. That policy pattern differs from typing an unquoted `*` in the invoking shell, which can expand filenames before sudo receives the arguments. Use explicit documented arguments when assessing a permitted operation. Interpret the actual permitted operation, including options. Package installers can execute hooks, and backup tools may execute a password-helper command. Build/runtime commands such as `dotnet run` can execute a selected project's build logic and application. `iptables-save -f` writes the selected file with the program's privileges, unlike redirection performed by the invoking shell. Restricting the executable name alone does not make its subcommands passive inspection. Preserve the effective policy and program semantics together before drawing a privilege conclusion.

For an authorized edit, define `run_as` as the permitted target user and `file` as the exact allowed absolute path:

~~~bash
sudoedit -u "$run_as" -- "$file"
~~~

`sudoedit` edits temporary copies as the invoking user, then uses privilege to copy changes back. It is different from launching an editor itself under sudo. A saved editor buffer does not prove the final copy-back succeeded; inspect errors and the resulting file. File/path safety checks can reject an otherwise listed edit.

When evaluating a historical sudo vulnerability, inspect the installed distribution package and its advisory/patch status. The upstream-looking string from `sudo --version` alone does not establish that a distro build is vulnerable. Record observed policy and behaviour separately from an exploitation hypothesis.

Consult the [sudoers policy manual](https://github.com/sudo-project/sudo/blob/main/docs/sudoers.man.in) for command matching and [Git's hook events](https://git-scm.com/docs/githooks) for the permitted program's behavior.
