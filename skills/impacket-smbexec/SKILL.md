---
name: impacket-smbexec
description: Run selected Windows commands through the Service Control Manager with Impacket smbexec from Linux. Use when SMB administrative access exists and service execution, output shares or SYSTEM versus user context matters.
---


# Execute through SCM with explicit output handling

Read this entire SKILL.md before acting. Require the selected host, known administrative identity or cache, permitted command and service/output cleanup scope. Finish with observed command output and identity plus residual-state checks; SMB authentication alone is incomplete.

Inspect `impacket-smbexec -h`; upstream also supplies `smbexec.py`. Define `domain`, `account` and `server` as the exact identity and Windows host. For the default SHARE output mode, prompt for the known password:

~~~bash
impacket-smbexec -mode SHARE -share 'C$' "$domain/$account@$server"
~~~

For an existing verified file cache, select its absolute path in `KRB5CCNAME`, use the service's FQDN and prevent password fallback:

~~~bash
KRB5CCNAME="$cache" impacket-smbexec -k -no-pass -mode SHARE -share 'C$' "$domain/$account@$server"
~~~

This authenticates over SMB/RPC, creates/starts a service to execute commands and reads output through the share. It is state changing even if the requested command is `whoami`. The share must be accessible with the needed write/read semantics; authentication and SCM permission do not prove output retrieval. `-mode SERVER` starts a local SMB server and makes the Windows host connect back for output, requiring that separate route and bind privileges; it is not an automatic repair for failed SHARE mode.

Inside the semi-interactive command prompt, run a selected `whoami` to establish the actual process identity. SCM execution commonly reports SYSTEM, which is not the authenticating user's interactive session or credential store. Commands do not form one durable interactive process; choose absolute paths and account for command-processor/encoding behavior. A missing output can reflect execution or retrieval failure, so do not automatically rerun a mutating command.

Exit the tool, inspect its cleanup messages and reconcile any created service, batch/output files or server-mode listeners. Errors can leave artifacts; remove only known owned state. See [upstream service/output implementation](https://github.com/fortra/impacket/blob/master/examples/smbexec.py).
