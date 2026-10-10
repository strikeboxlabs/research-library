---
name: impacket-wmiexec
description: Execute a selected Windows command from Linux using Impacket WMI/DCOM and diagnose its SMB output channel. Use for authorized remote administration when WMI execution and output collection must be distinguished.
---

# Separate process creation from output retrieval

Read this entire file before acting. For failures, output handling or cleanup read [execution stages](references/execution-stages.md) fully. Finish with the chosen host/identity, command result, output evidence and unresolved effects; a connected session alone is not successful execution.

Check `impacket-wmiexec -h`. Define `identity` as `domain.example/user`, `server` as the actual hostname and `server_ip` as its address. With a matching Kerberos cache:

~~~bash
impacket-wmiexec -k -no-pass -target-ip "$server_ip" "$identity@$server" 'whoami'
~~~

This executes a real remote process. The selected account needs WMI/DCOM rights and the normal output path needs SMB access, usually to `ADMIN$`. Without Kerberos, omitting credentials from argv lets the client prompt. Do not substitute an arbitrary hostname merely to satisfy the syntax.

Omitting the command starts a semi-interactive command interface. This does not provide a persistent terminal/process environment: separate commands launch processes, although the client tracks its working directory. Use one properly quoted remote command for operations whose environment changes must survive into the next operation.

The default command shell is `cmd`; builds supporting `-shell-type powershell` add a different quoting and encoding layer. Linux-shell quoting happens before the remote shell parses the string. Start with the smallest command that demonstrates the requested capability, then choose the intended operation. See [upstream CLI and execution implementation](https://github.com/fortra/impacket/blob/master/examples/wmiexec.py).
