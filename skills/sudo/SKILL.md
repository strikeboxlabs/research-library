---
name: sudo
description: Interpret sudo policy, RunAs identities, helper paths, authenticator/key-enrollment inputs, environment handling and sudoedit on Linux. Use when a permitted command behaves differently under sudo or a walkthrough overstates privilege from a policy listing.
---

# Understand the permitted operation

Read this entire SKILL.md before acting; reuse complete current context. Establish the exact RunAs identity, command/argument restrictions and authentication tags. For scripts, helpers, environment-dependent children, Git hooks, SSH client commands or Python module presets, read [permitted-program behavior](references/permitted-programs.md) fully before attributing privilege. For a permitted password-gated program with a public-key enrollment branch, read [authenticator inputs and effects](references/authenticator-inputs.md) fully before invoking it. Finish with the policy and supported effects; listing a command is not an executed result.

Read the effective listing before selecting an elevated command:

~~~bash
sudo -l
sudo -ll
~~~

Listing may require authentication. For unattended inspection, `sudo -n -l` fails instead of prompting; that failure does not by itself mean no policy entry exists. Record the target RunAs user/group, command path, argument restrictions and tags together. `(dev_admin : dev_admin)` is a permitted target identity, not a root grant.

An additional PAM prompt can be a separate authentication requirement, not another request for the account password. Inspect readable `/etc/pam.d/sudo` and its included stacks when diagnosing it. A failed `required` module can still allow later prompts before the stack rejects authentication. Keep authentication failure distinct from sudo policy denial; an interrupted challenge does not establish the effective policy. Diagnose the configured requirement without editing PAM to bypass it.

Membership in a group named sudo is a policy lead, not the effective grant. An observed `(ALL : ALL) ALL` entry permits arbitrary matching commands as the selected RunAs identity under that policy, including a selected root shell; it still does not mean NOPASSWD. Choose the actual target explicitly when reproducing it and verify identity inside the resulting session. `sudo su` additionally uses su's environment/session behavior; it is not equivalent to a login-style shell.

`NOPASSWD` affects authentication for matching entries; it does not grant arbitrary commands. `SETENV` changes environment restrictions for the matching operation. `env_reset` and `secure_path` can explain why a program works normally but finds different variables or executables under sudo.

For a permitted Backdrop Bee executable, the allowed `eval`/`php-script` inputs can execute PHP after application bootstrap with the RunAs process context. A path-only grant is not restricted to administrative status checks, and env_reset/secure_path do not remove an allowed evaluation subcommand. Establish the selected site, actual wrapper and observed child identity; a CMS login name is separate from OS privilege.

A sudoers command entry with no argument specification permits any arguments; an explicit `""` argument specification permits none. Thus a path-only daemon grant can include options selecting a different configuration. For Nginx, inspect permitted `-c`/`-g` inputs, included files and module paths: configuration controls worker identities, listeners and file operations. Record that authority without launching a replacement privileged service. A configuration-test flag does not make arbitrary module/configuration loading passive.

In command-argument patterns, sudoers wildcards can match whitespace and span arguments; `*` is not necessarily one filename. Sudo 1.9.10 and later also support POSIX extended regular expressions explicitly beginning with `^` and ending with `$`, with executable paths and argument strings matched separately. Verify the installed policy version before interpreting such a listing; an older wildcard-only manual does not establish its meaning. Policy patterns differ from typing an unquoted `*` in the invoking shell, which can expand filenames before sudo receives the arguments. Use explicit documented arguments when assessing a permitted operation. Interpret the actual permitted operation, including options. Package installers can execute hooks, and backup tools may execute a password-helper command. Build/runtime commands such as `dotnet run` can execute a selected project's build logic and application. `iptables-save -f` writes the selected file with the program's privileges, unlike redirection performed by the invoking shell. Restricting the executable name alone does not make its subcommands passive inspection. Preserve the effective policy and program semantics together before drawing a privilege conclusion.

For an authorized edit, define `run_as` as the permitted target user and `file` as the exact allowed absolute path:

~~~bash
sudoedit -u "$run_as" -- "$file"
~~~

`sudoedit` edits temporary copies as the invoking user, then uses privilege to copy changes back. It is different from launching an editor itself under sudo. A saved editor buffer does not prove the final copy-back succeeded; inspect errors and the resulting file. File/path safety checks can reject an otherwise listed edit.

For an explicitly authorized matching command, define `run_as` as the permitted target identity and `permitted_command` as its actual allowed executable path, with any permitted arguments selected from the effective policy. Execute that operation rather than treating the policy listing as its result:

~~~bash
sudo -u "$run_as" -- "$permitted_command"
~~~

This invocation has no additional arguments; add only the reviewed ones the task requires. If the selected grant permits a shell, verify `id` within that elevated shell and perform only the requested work before exiting. A root RunAs grant and successful UID-zero observation differ from a grant to another named administrator account. Do not infer unlimited shell authority from a restricted program entry, or universal host authority from a UID-zero process in a constrained namespace.

When evaluating a historical sudo vulnerability, inspect the installed distribution package and its advisory/patch status. The upstream-looking string from `sudo --version` alone does not establish that a distro build is vulnerable. Record observed policy and behaviour separately from an exploitation hypothesis.

Consult the [sudoers policy manual](https://github.com/sudo-project/sudo/blob/main/docs/sudoers.man.in) for command matching and [Git's hook events](https://git-scm.com/docs/githooks) for the permitted program's behavior.
