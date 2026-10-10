---
name: impacket-addcomputer
description: Create and verify a selected Active Directory computer account using Impacket from Linux. Use to choose SAMR versus LDAPS, understand quota and attribute differences, and remove only an explicitly temporary account owned by the task.
---

# Create the intended directory object

Read this entire file before acting. Resolve the domain/container, establish that the chosen name is unused, and preserve the new object's identity after creation. Finish with its DN/SID, method and observed attributes; creating a computer account does not join a Linux machine to the domain.

Check `impacket-addcomputer -h`. Define `identity` as `domain.example/user`, `dc_fqdn`, `dc_ip`, `computer_account` as the selected name including `$`, and `creation_log` as a new private file. With a matching Kerberos cache:

~~~bash
umask 077
impacket-addcomputer -k -no-pass -dc-host "$dc_fqdn" -dc-ip "$dc_ip" \
  -method LDAPS -computer-name "$computer_account" "$identity" > "$creation_log" 2>&1
~~~

Omitting `-computer-pass` lets supported builds generate a password. The log can contain that password: handle it as credential material, not an ordinary transcript. Inspect the result and read the created object through the directory client already available in the task. Record its exact DN/SID and check `sAMAccountName`, `dNSHostName`, SPNs and account flags relevant to the next operation.

| Choice or result | Operational meaning |
|---|---|
| `-method LDAPS` | Creates over TLS LDAP; trust/connectivity, container rights and directory policy matter. |
| Default `SAMR` | Uses SMB/SAMR; do not assume it populates the same DNS/SPN attributes as LDAPS. |
| Quota exceeded or access denied | Check effective creation rights, quota usage and selected container. A positive domain quota alone is not a guarantee for this caller. |
| Name already exists | Resolve that object. Do not switch to `-no-add` as a retry: it resets an existing account's password. |
| Creation partially succeeds | Read current state before retrying; another random name can leave an extra object behind. |

Newer builds offer SAMR/LDAP finalization modes; use them only when the installed interface supports them and the desired attributes are known. Avoid assuming those newer options exist in an older distribution.

For an explicitly temporary account, verify that its current DN/SID matches the object created by this task and that no dependent service needs it. Then use the same connection and name with `-delete`, and verify absence on the selected DC. This deletes a directory object; it does not revoke every previously issued ticket or undo unrelated delegation changes. Never delete an account merely because its name resembles a test name.

See [upstream CLI and creation paths](https://github.com/fortra/impacket/blob/master/examples/addcomputer.py). Runtime account changes require an actual authorized directory; documentation alone cannot establish the deployment's effective rights.
