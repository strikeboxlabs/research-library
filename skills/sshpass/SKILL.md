---
name: sshpass
description: Supply one authorized SSH password noninteractively with sshpass and diagnose prompt, host-key and authentication failures. Use when an existing password-based account needs a bounded command without embedding its secret in process arguments.
---

# Password input for a selected SSH account

Read this entire SKILL.md before acting. Require an authorized selected account/endpoint, an independently verified host key and a private password source. Use the actual installed sshpass/OpenSSH options below. Finish with the SSH result and observed remote identity or requested command outcome; a supplied password and connection banner alone do not prove the intended access.

`sshpass` runs the SSH client through a dedicated terminal and recognizes its password prompt. It does not discover passwords or make a database/CMS credential valid for an OS account. Confirm the actual account separately; `/etc/passwd` is an account record, not an authentication result. A single evidenced reuse test differs from trying an entire username list against a login.

Inspect `sshpass -V`/`sshpass -h` and OpenSSH's installed options. Define `password_file` as a private existing file whose first line contains the approved password, `ssh_host`/`ssh_port`/`user` as the selected endpoint/account and `known_hosts` as the existing file with its independently verified key. In Bash:

~~~bash
(
  exec 3<"$password_file" || exit
  sshpass -d 3 ssh -p "$ssh_port" \
    -o StrictHostKeyChecking=yes -o UserKnownHostsFile="$known_hosts" \
    -o ConnectTimeout=10 -o NumberOfPasswordPrompts=1 \
    "$user@$ssh_host" 'id'
)
~~~

The subshell closes its descriptor when done. `-d` consumes an inherited descriptor and keeps the password out of argv; supplying it on stdin can steal bytes intended for the remote command. `-f` instead reads the first line of a chosen file; `-e` uses exported SSHPASS, which is still sensitive environment data. `-p` puts the secret on the command line and can expose it via history/process inspection. Do not copy a writeup's literal password into reusable commands.

The command sends `id` to that account after authentication. A login satisfied by an existing key is not proof that this password was accepted; retain the actual authentication mechanism when reuse is the question. Preserve stderr, status and the returned numeric identity; a denied remote command is different from rejected authentication. For an authorized interactive session omit the final remote command and let SSH's terminal rules apply. ConnectTimeout bounds connection establishment, not the entire session; use the worker's task/session budget for the latter.

| Observation | Interpretation and next decision |
|---|---|
| sshpass status 5 | Password rejected in this attempt; inspect account/method/server policy before attributing it to all uses of the secret. |
| sshpass status 6 or 7, or an SSH host-key error | Unknown/changed host key. Resolve trust independently rather than disabling checking or changing credentials. With strict checking SSH can report 255 instead. |
| status 4 or waiting at a prompt | Prompt parsing differs. `-P` selects an actually observed prompt; it is not an answer mechanism for every MFA challenge. |
| SSH status 255 | Transport/configuration/key/policy error can share this status; read stderr. |
| Output plus zero | Check the requested identity/action output. Remote command failures can propagate a nonzero code that overlaps a sshpass code, so retain context. |

Multiple sources or invalid options produce separate errors. Use at most one password source. Preserve existing host-key policy and do not infer that disabling public-key authentication or forcing a new method is necessary merely from one prompt failure.

See [sshpass's packaged manual](https://manpages.debian.org/bookworm/sshpass/sshpass.1.en.html) and [OpenSSH options](https://man.openbsd.org/ssh.1) for prompt, descriptor and status behavior.
