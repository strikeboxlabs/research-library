# Inspect an existing SSH OTP role, then connect when required

Use the established Vault endpoint, namespace and authorized token. Define `ssh_mount` as the known engine mount path relative to that namespace, without leading/trailing slashes, and `role` as the exact known role name. Read an acquired setup script as text; its enable/write commands change the server and do not prove the current role configuration.

~~~bash
vault read -format=json "$ssh_mount/roles/$role"
vault token capabilities "$ssh_mount/creds/$role"
~~~

The capability command uses the active token when no explicit token argument is supplied; it does not issue a credential. Check each command's status. `deny`, a denied role read and an absent path differ; verify namespace/mount and authorization rather than creating a replacement role. Capability output describes policy on that path, not fulfillment of role or host conditions.

For an OTP role, inspect `key_type`, `default_user`, user restrictions, `cidr_list`, exclusions and `port`. The default username is a fallback, not proof of unrestricted username selection. CIDRs describe destination eligibility, not reachability or the operator's authorization. A role's port informs the client; it is not part of the OTP-generation restriction. A `key_type=ca` role needs certificate signing, not this OTP procedure. Use the installed version's API documentation when fields differ.

OTP authentication requires the remote SSH/PAM helper to validate the credential with Vault. Role configuration alone does not establish that helper's installation, TLS trust or connectivity. Issuance, helper validation and SSH account/session policy are separate stages. The OTP is consumed by successful verification; do not call the verification API as a harmless preflight.

For a task that actually requires an authorized login, define `ssh_user` and `target_ip` as the intended permitted account and exact destination IP, confirm the role's port and the server's host key, then use:

~~~bash
vault ssh -mount-point="$ssh_mount" -role="$role" -mode=otp "$ssh_user@$target_ip"
~~~

This requests a credential and launches the local SSH client. It is not a read-only role check. If `sshpass` is unavailable, supported clients display the OTP for entry at SSH's prompt; keep it out of shared logs. Preserve host-key checking rather than disabling it for automation. Missing interactive input is an execution prerequisite, not a reason to repeatedly issue credentials.

`-no-exec` suppresses SSH execution **but still generates and prints credentials**. Use it only when issuance itself is intended, with a private output destination. It is not a dry run. Avoid interpreting the absence of an SSH session as absence of a Vault-side effect.

| Observation | Next decision |
|---|---|
| Vault denies issuance | Check active token, namespace, exact credential path and role restrictions. An SSH password retry cannot fix Vault policy. |
| OTP issued, SSH rejects login | Check actual IP/port/user, helper/PAM policy, helper-to-Vault communication and whether the OTP was already consumed. Do not assume issuance grants OS-root access. |
| SSH session established | Report the actual remote identity and requested operation; a role name or token policy is not equivalent evidence. |

References: [role fields and paths](https://developer.hashicorp.com/vault/api-docs/secret/ssh), [capability queries](https://developer.hashicorp.com/vault/docs/commands/token/capabilities), [OTP/helper lifecycle](https://developer.hashicorp.com/vault/docs/secrets/ssh/one-time-ssh-passwords), [SSH command options](https://developer.hashicorp.com/vault/docs/commands/ssh).
