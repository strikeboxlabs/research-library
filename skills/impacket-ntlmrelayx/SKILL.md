---
name: impacket-ntlmrelayx
description: Configure a selected NTLM relay with Impacket and distinguish inbound authentication, target authentication and the chosen protocol action. Use for controlled relay testing with explicit listeners, destinations and result evidence.
---

# Select the destination and post-authentication action

Read this entire file and [relay stages](references/relay-stages.md) before starting a listener. For a selected LDAP DNS-record action or an AD CS HTTP authentication mismatch, also read [LDAP record and enrollment destinations](references/ldap-dns-and-adcs.md) fully. Require the authorized source client, listener network and destination. Finish with the actual principal, protocol, destination result and action evidence; captured challenge-response material alone is not a successful relay.

Inspect `impacket-ntlmrelayx -h` for the installed build. This tool can perform actions after authentication; default behavior is not necessarily passive collection. Select a target and action explicitly. An omitted target can select reflection, and a target-file watcher can expand destinations after startup.

For a controlled SMB relay whose selected outcome is an interactive SMB client rather than an automatic dump, define `target_host` and `listen_ip`. A current build with the shown server controls can restrict ingress to its SMB listener:

~~~bash
impacket-ntlmrelayx -t "smb://$target_host" -ip "$listen_ip" -smb2support -i \
  --no-http-server --no-wcf-server --no-raw-server --no-rpc-server \
  --no-winrm-server --no-mssql-server --no-rdp-server
~~~

Older builds lack some server types/options. Match the disable list to the installed help and verify actual listeners; do not delete an unknown switch and assume the same network exposure. Required port-binding privileges and conflicts must be resolved before claiming readiness. Arrange the explicitly authorized client's connection separately; starting ntlmrelayx does not itself prove that client authenticated.

After a successful SMB relay, the `-i` mode reports a local interactive-console port. Use that exact endpoint to run only the selected SMB operation. For example, `shares`, `use SHARE`, then `ls *` establish progressively narrower access; they do not establish read permission for every file or remote OS command execution. See [upstream options](https://github.com/fortra/impacket/blob/master/examples/ntlmrelayx.py).
