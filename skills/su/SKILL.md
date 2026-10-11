---
name: su
description: Start a selected local Linux account session with su and a known credential. Use when login environment, PAM policy, terminal handling or application-versus-OS identity changes the result.
---

# Selected local account session

Read this entire SKILL.md before acting; reuse complete current context. Select the actual OS account and intended session, authenticate through the prompt, and verify the resulting process identity before reporting access. A password recovered for an application account is only a reuse candidate for an OS account.

Check `su --version` and `su --help` to identify the installed implementation. The procedure below targets util-linux su. Define `account` as the selected local account whose session is authorized:

~~~bash
su --login "$account"
~~~

Enter the known password at the prompt. Once the new shell opens, run:

~~~bash
id
printf 'HOME=%s SHELL=%s PATH=%s\n' "$HOME" "$SHELL" "$PATH"
pwd
~~~

Confirm effective UID/GID/groups and the intended account, directory and shell environment. An application username such as root or an administrator role does not establish OS UID 0. A changed prompt alone is weaker evidence than the returned identity. Namespace/capability restrictions can still limit a UID-0 process.

`--login` starts a login shell, changes to the account's home and resets much of the environment; PAM and startup files can modify it afterward. Plain `su "$account"` normally retains the working directory and more of the caller's environment. Choose that deliberately when reproducing an environment-dependent result, rather than assuming the two sessions are equivalent. On systemd systems, a login-style su shell is not automatically a complete new login session in the system manager.

For an interactive account change needing terminal separation, use `su --pty --login "$account"` when the installed util-linux build supports --pty. This allocates a separate pseudo-terminal and proxies input/output; it changes terminal handling, not authentication rights. Ordinary su can share the caller's terminal, allowing permitted TIOCSTI input from a lower-privilege process to be consumed by another shell after the nested session returns. Compare stdin endpoints and actual session/foreground groups before asserting that chain; current kernels may disable legacy TIOCSTI. Do not treat a changed UID or --login alone as terminal separation.

For a Bash login shell, startup reads /etc/profile then the first readable .bash_profile, .bash_login or .profile in that order. It does not automatically read all three or .bashrc; .bashrc may be sourced by a selected file. Noninteractive and other shells have different rules. If testing an authorized startup-file change, preserve the original, choose the file the actual shell will read, use a bounded marker and restore it afterward. Startup execution under the target account does not by itself prove execution under the su caller. A target's restricted/default shell, disabled account, expiration, PAM access rule or MFA requirement can prevent the requested session even with a correct password. Read the actual failure; do not turn every denial into repeated password attempts or a policy change.

Finish the intended work and `exit` the nested shell. Verify the caller's identity again. Su normally returns the child command's exit status, while its own pre-execution failures have separate statuses; zero after an unrelated child command is not a general credential-validity test.

See the upstream [util-linux su manual](https://github.com/util-linux/util-linux/blob/master/login-utils/su.1.adoc) for the installed version's environment, PAM, terminal and status behavior.
