---
name: vault
description: Inspect HashiCorp Vault status, active-token policy metadata and existing SSH OTP roles. Use to distinguish cached credentials, seal state, policy capabilities, credential issuance and actual SSH login.
---

# Vault status and SSH access

Read this entire SKILL.md before acting; reuse complete current context. Establish the intended Vault endpoint, namespace and authorized token context first. For active-token metadata or one selected policy, read [token and policy inspection](references/token-policy.md) fully. For SSH role inspection or an authorized OTP connection, read [SSH OTP roles](references/ssh-otp.md) fully. Finish with actual status, scoped policy/role evidence or the login result; cached-token presence and credential issuance do not prove remote access.

Use the installed HashiCorp `vault` CLI, distinct from Ansible Vault. Check `vault version` and `vault ssh -help` locally for the supported options. A skill does not establish that this binary or the remote SSH helper is installed.

Set the deployment's known `VAULT_ADDR`, applicable `VAULT_NAMESPACE` and trusted CA configuration before server requests. Keep TLS verification enabled; check inherited agent/proxy/namespace settings when the endpoint seems wrong. A familiar mount name can resolve differently in another namespace.

The default token helper caches credentials in `~/.vault-token`; custom helpers and `VAULT_TOKEN` can change the active token source. Do not print a cache or export its contents merely to check whether it exists. A file's presence does not establish token validity, policy or permission to use it.

Once the endpoint/context is established:

~~~bash
status=0
vault status -format=json || status=$?
printf 'vault_status_exit=%s\n' "$status"
~~~

Interpret the JSON and status together: 0 means unsealed, 2 sealed, 1 an error. A responding sealed service differs from a connection/TLS failure; unsealed is not an authorization result. Record the reported server version separately from the client version. Missing endpoint, authentication or SSH-role prerequisites leave that part of the task unresolved; inspecting an existing deployment does not require enabling engines, writing roles or unsealing servers.

An authentication token is distinct from seal key material. Shamir unsealing needs the configured threshold of key shares; an auto-unseal deployment has its own seal provider. A token labeled root does not itself unseal a sealed service. Keep [seal semantics](https://developer.hashicorp.com/vault/docs/concepts/seal) separate from token policy.

References: [status and exit codes](https://developer.hashicorp.com/vault/docs/commands/status), [CLI connection settings](https://developer.hashicorp.com/vault/docs/commands), [token helpers](https://developer.hashicorp.com/vault/docs/commands/token-helper).
