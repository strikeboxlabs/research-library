---
name: sftp
description: Inspect an authorized SFTP account's path namespace, retrieve a selected file or create a selected owned symlink without confusing SSH transport, filesystem access and web-server behavior.
---

# Use the selected SFTP namespace

Read this entire SKILL.md before acting. Require the selected SSH endpoint/account, established host-key trust and requested paths. Retrieval requires a fresh private local destination; symlink creation requires authorization for that owned remote directory entry and target. Finish with the actual listing/transfer/link result and unresolved namespace or permission limits. No conditional resources are required.

Define `sftp_bin`, `server`, `ssh_port` and `account` for the intended OpenSSH client and SSH service, then use the established credential mechanism:

~~~bash
"$sftp_bin" -P "$ssh_port" "$account@$server"
~~~

Uppercase `-P` selects the port; lowercase `-p` preserves transferred metadata. In the interactive prompt, run `help`, `version`, `pwd` and `lpwd`. Protocol version is not the OpenSSH package version. The prompt has its own command parser, not a remote shell: `ls` concerns remote paths, `lls` local paths, and `!` launches a local shell. Do not expect Bash variable expansion in these commands.

Use `ls -l` for the selected remote directory. Its root/current directory may be a restricted server namespace, not the host's filesystem root. Login proves SFTP access only; it does not prove an interactive SSH shell, forwarding permission or a web application's login rights.

For a requested retrieval, `get "REMOTE_PATH" "FRESH_LOCAL_PATH"` uses actual paths substituted at the prompt. Quote spaces and escape glob characters rather than unintentionally selecting several files. Confirm the transfer result and local bytes/size; compare a trusted digest when available. An existing partial copy is not automatically a safe resume baseline.

For an authorized owned-directory symlink, `symlink "OWNED_TARGET" "NEW_LINK"` records the target string at the new remote link name; substitute actual paths and inspect that exact entry afterward. A successful link does not prove the target exists or that another process can follow/read it. Absolute targets and relative targets resolve in the consuming process's namespace. Web exposure, handler selection and symlink policy are separate application configuration; do not infer them from an SFTP listing. Unsupported server operations or access denial leave the change unresolved. End with `bye` and account for any requested remote change.

See [OpenSSH SFTP commands and path rules](https://man.openbsd.org/sftp.1).
