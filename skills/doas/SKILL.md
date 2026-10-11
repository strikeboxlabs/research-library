---
name: doas
description: Validate a selected doas policy match and run an already authorized command as its configured target user. Use to distinguish policy permission, password authentication, environment changes and command failure on a portable Linux doas installation.
---

# Use the configured command permission

Read this entire SKILL.md before acting. Require an installed identified doas implementation, the existing policy, an authorized command and target identity, and the configured authentication method. All steps are inline. Finish with policy-match limits and the actual command outcome; parsing a configuration never establishes successful execution.

On Linux, identify the installed portable implementation and consult its matching manual. OpenDoas is a portable fork, with PAM/shadow and optional persisted-authentication differences from OpenBSD. Do not assume another system's authentication settings or invent a `--version` option. Missing policy or authentication is a prerequisite gap, not an instruction to change policy.

Define `config` as the selected existing configuration, `target_user` as the intended configured account, `command_path` as the absolute authorized executable, and Bash array `command_args` as its intended arguments. When policy interpretation is needed:

~~~bash
doas -C "$config" -u "$target_user" "$command_path" "${command_args[@]}"
~~~

`-C` parses the file and, with a command, prints the matching decision: `permit`, `permit nopass` or `deny`. It executes nothing. Checking an alternate file does not make it the installed policy. Review all relevant rules: the last matching rule wins and no match denies. Missing `cmd` allows all commands; missing `args` allows any arguments, while `args` alone means no arguments. A rule permitting a target user does not supply a password or prove current authentication succeeds.

For the actual approved action under the installed policy:

~~~bash
doas -u "$target_user" "$command_path" "${command_args[@]}"
~~~

Enter the invoking user's password through the interactive prompt if requested. Do not place it in arguments. For unattended work, use the implementation's documented noninteractive option only when its installed policy/authentication contract supports the task; refusal is an unresolved prerequisite rather than a reason to weaken authentication.

The target defaults to root when omitted, so keep the intended target explicit. The command runs in the current working directory, with a newly constructed target environment modified by policy. Shell expansion and redirection written outside the doas command run in the invoking shell; they do not inherit the command's target identity. Select the exact approved command rather than substituting a general shell.

Distinguish policy denial, authentication error, missing executable and failure inside the invoked command using diagnostics and final status. When identity is material, use the task's own bounded identity evidence. Report the command's requested result and any side effects; permission matching alone is incomplete.

References: [OpenDoas implementation differences](https://github.com/Duncaen/OpenDoas), [command contract](https://github.com/Duncaen/OpenDoas/blob/master/doas.1), [policy matching](https://github.com/Duncaen/OpenDoas/blob/master/doas.conf.5).
