---
name: scp
description: Copy selected files with OpenSSH scp from a Linux client. Use for SFTP versus legacy SCP differences, remote Windows paths, port selection and incomplete evidence transfers.
---

# Selected SSH file transfers

Read this entire SKILL.md before acting; reuse complete current context. Select upload or retrieval and exact authorized endpoints/paths before copying. Preserve transfer status and available size/digest evidence; an incomplete copy or successful transfer alone does not establish content validity or execution.

Inspect the OpenSSH client version with `ssh -V` and the installed `scp` manual. OpenSSH 9.0 and later use SFTP by default; the remote server needs an SFTP subsystem. A successful SSH shell does not prove that subsystem or the desired file is accessible.

Define `ssh_target` as the known SSH alias or `user@host`, `port` as the SSH port, `remote_path` as one observed absolute server-side path without wildcards, and `local_file` as a fresh absolute destination in a private workspace:

~~~bash
umask 077
scp -P "$port" -- "${ssh_target}:${remote_path}" "$local_file"
~~~

`-P` selects the port; lowercase `-p` preserves times and mode bits. Existing SSH configuration, identities, jump hosts and host-key checks still apply. Check the transfer exit status before using the output; scp can leave a partial file after interruption and overwrite an existing destination. Choose a new destination for a retry and compare expected size/digest when available.

The colon separates the host from the remote path. For a **local** filename containing a colon, use an explicit local path such as `./name:part` or an absolute path. Quote the entire remote specification against the local shell. A Windows path pasted with unquoted backslashes loses characters in Bash; use the path syntax actually exposed by that server's SFTP subsystem, commonly forward slashes, and confirm drive/home mapping through a listing. Do not transplant a Windows command-prompt path mechanically.

## Upload one selected local artifact

For an authorized upload, define `local_source` as the exact acquired local file and `remote_file` as a fresh complete destination path as exposed by that server. Use the same established `ssh_target` and `port`:

~~~bash
scp -P "$port" -- "$local_source" "${ssh_target}:${remote_file}"
~~~

An existing remote destination can be overwritten; select the intended name rather than relying on a directory basename. Check status and compare remote size/digest through the task's existing access when available. An uploaded pspy or other binary still needs the actual architecture/loader and separate authorization to change permissions/run it. scp transfers bytes; it does not install the program, make it executable or prove its provenance. An interruption can leave a partial remote file, so do not retry execution to test transfer completeness.

## Recover from a failed transfer

For a failed SFTP-default transfer, **illustrative** diagnostics such as these identify different next checks:

| Diagnostic | Next decision |
|---|---|
| `Permission denied (publickey)` | Resolve SSH identity/authentication; changing transfer protocol does not solve it. |
| `subsystem request failed on channel 0` | The SFTP subsystem request was rejected. Check its availability and account policy; this alone does not prove legacy SCP will work. |
| `No such file or directory` after SFTP starts | Confirm the path as exposed by SFTP, including home/chroot/drive mapping. Do not change protocols merely to guess paths. |
| Interrupted copy or connection loss | Treat the local file as partial. Preserve it if useful, choose a fresh destination, and recheck source stability before retrying. |

When SFTP is available, inspect its view with:

~~~bash
sftp -P "$port" "$ssh_target"
~~~

At the SFTP prompt, use `pwd` and `ls` on the observed directory, then `bye`. A successful listing resolves path visibility, not readability of every file. For additional transfer diagnostics, add `-v` to a retry directed to a fresh local file.

If the endpoint is confirmed to require legacy SCP and permits its remote command, use a new destination with:

~~~bash
scp -O -P "$port" -- "${ssh_target}:${remote_path}" "$local_file"
~~~

`-O` changes remote-shell interpretation. Recheck quoting for spaces/metacharacters before this invocation; the local quotes alone do not guarantee literal interpretation by the remote shell. Retain host-key verification and the selected identity. Finish only after a successful exit and available size/digest checks; a progress bar reaching 100% does not prove the artifact is valid.

`-r` follows symbolic links encountered during traversal; a directory transfer may include more than its apparent tree. Retrieve selected files when that is sufficient. Copying a live database is not a consistent backup: obtain a coordinated snapshot/export, including required journal state, before transferring it. Report source, destination, transfer result and integrity evidence separately from the file's semantic validity.

For installed-version options and protocol differences, consult the [OpenSSH scp manual](https://man.openbsd.org/scp).
