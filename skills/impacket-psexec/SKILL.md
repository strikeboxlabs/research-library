---
name: impacket-psexec
description: Execute a selected Windows command from Linux using Impacket's service-based PsExec implementation. Use to distinguish SMB authentication, writable shares, service-control rights, command output and cleanup failures.
---

# Execute through the intended service-control path

Read this entire file before acting. This tool uploads a service binary and creates/starts a remote service; use it when that remote execution and those artifacts are authorized. Read [failure and cleanup stages](references/failure-and-cleanup.md) for partial failures. Finish with command output/status and verified disposition of owned service/file artifacts.

Check local help for `impacket-psexec` or `psexec.py`. This is the Impacket implementation, with different behavior from Microsoft's PsExec. Define `psexec_bin` as the verified executable, `domain`, `user`, `target_name` and fresh unique `service_name`/`remote_name` identifiers for this operation. Ensure the identifiers do not collide with existing resources. Omitting a password from the target identity uses the prompt in the reviewed CLI:

~~~bash
"$psexec_bin" -service-name "$service_name" -remote-binary-name "$remote_name" \
  "$domain/$user@$target_name" 'cmd.exe /c whoami'
~~~

The harmless identity command still incurs upload/service execution. Use the actual returned identity; do not infer it from the account used for SMB authentication. Writable share access and Service Control Manager rights are separate prerequisites. A successful SMB login is insufficient.

For an existing Kerberos cache, add `-k -no-pass`, retain the intended hostname in the target identity and use `-target-ip` when transport must go to a particular address. `-dc-ip` selects the DC, not the remote Windows host. `KRB5CCNAME` must point to the correct valid cache; `-no-pass` only suppresses prompting.

The command is parsed on Windows as well as by the local shell. Quote to preserve the intended remote argument string; do not assume Bash escaping controls cmd.exe metacharacters. `-c` copies a local executable for later execution and is an additional transfer, not a command-output capture flag. If output decoding fails, determine the remote code page and select the matching `-codec`; do not mistake mojibake for command failure.

The tool attempts cleanup, but disconnects and blocked execution can leave files/services. Keep the logged share, binary path and service name for targeted verification. See [upstream CLI](https://github.com/fortra/impacket/blob/master/examples/psexec.py) and [service lifecycle](https://github.com/fortra/impacket/blob/master/impacket/examples/serviceinstall.py).
