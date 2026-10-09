---
name: bash
description: Diagnose Bash startup, environment inheritance and redirection-order mistakes in scripts or scheduled jobs. Use when an interactive shell, SSH session and job execute with different settings.
---

# Bash execution context

Determine which shell actually runs the command; `$SHELL` identifies a preferred login shell, not necessarily the current interpreter. Within Bash, these inspect the current context:

~~~bash
printf 'Bash=%s flags=%s\n' "$BASH_VERSION" "$-"
shopt login_shell
~~~

An `i` in `$-` indicates interactive mode. For ordinary Bash invocation:

| Context | Startup behaviour to check |
|---|---|
| Login | `/etc/profile`, then the first readable user file among `.bash_profile`, `.bash_login`, `.profile`. |
| Interactive non-login | `.bashrc`; system rc files also depend on distribution/build and explicit sourcing. |
| Noninteractive script | The file named by exported `BASH_ENV`, when set. Do not assume interactive rc files were read. |

Remote-shell detection, invocation as `sh`, POSIX mode and explicit startup-suppression options change these rules. Inspect the real invocation and actual files. A user's `.bashrc` does not generically override `/etc/bash.bashrc` by precedence. A cron job does not become an interactive Bash merely because the user's login shell is Bash.

When effective and real IDs differ, Bash normally resets its effective user ID unless invoked with `-p`. Privileged mode preserves an already obtained identity; it does not grant root to an ordinary process. It also changes environment/startup handling. Inspect actual IDs and invocation when comparing behavior; a setuid-looking permission string or a root-shaped prompt alone is insufficient evidence of effective privilege.

Invoking `sh script` uses that interpreter regardless of a Bash shebang. Bash's combined-output `>&file` redirection and `/dev/tcp/host/port` handling are not portable POSIX sh features; even Bash builds can differ in network-redirection support. Check the actual command, not only the script's first line, when diagnosing a copied snippet.

`source file` executes shell code in the current shell: it can change variables, functions, directory and subsequent execution. A virtualenv activation file is executable shell input, not passive settings. Its owner does not become the executing identity; a privileged process sourcing a writable file executes that code in its own context.

A plain assignment creates/updates a shell variable; `export NAME=value` exposes it to child processes. `NAME=value command` supplies it for that command. If a variable was already exported, reassignment retains that attribute. Sudo or an application can then apply additional filtering.

Redirections run left to right. `command 2>&1 >/dev/null` discards stdout but leaves stderr pointing at the original stdout. To capture both streams, define `log` as a fresh file and redirect `command >"$log" 2>&1`. Check the command's exit status as well as its log; silence is not success. Use `bash -n script` to check syntax, remembering that it does not validate runtime paths, permissions or behaviour.

Documentation reviewed 2026-10-09; Linux execution untested. Cases: Admirer p. 22; Agile pp. 17, 21–22; Analytics p. 5; Bamboo pp. 6, 11–12. Sources: [startup files](https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files.html), [environment](https://www.gnu.org/software/bash/manual/html_node/Environment.html), [redirections](https://www.gnu.org/software/bash/manual/html_node/Redirections.html), [privileged mode](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html).
