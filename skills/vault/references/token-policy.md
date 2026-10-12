# Inspect the intended active token and one policy

Require the intended Vault endpoint/namespace, trusted TLS and an authorized token context. If a provisioned existing token must be selected interactively, inspect `vault login -help`, then use `vault login -no-print` and enter it at the hidden prompt. This stores it in the configured helper without displaying it. Inherited `VAULT_TOKEN` can still select a different active token; reconcile the intended context before queries. Do not use leaked or unrelated tokens to resolve denial.

For nonsecret selected metadata, use `read -field` on the self-lookup endpoint. Do not attach `-field` to `token lookup`: its option set can omit that selector.

~~~bash
vault read -field=policies auth/token/lookup-self
vault read -field=display_name auth/token/lookup-self
vault read -field=ttl auth/token/lookup-self
~~~

Each query has its own status/time. A display name is a configurable token label, not verified OS identity. Policy names are not Linux groups; token creation TTL, current remaining TTL and renewability differ. Avoid unfiltered lookup output: it includes the token ID, while the queries above choose only these fields. A denied self-lookup leaves metadata unavailable rather than invalidating every separate capability observation.

Define `policy` as one observed intended ACL policy name and `policy_path` as its exact documented path for this server version. Modern ACL policies use `sys/policies/acl/$policy`; historical `sys/policy` aliases are version-dependent:

~~~bash
vault token capabilities "$policy_path"
vault policy read "$policy"
~~~

Check status and retain rules for that selected policy. Capability `read` on one policy path does not grant all policy listing or engine actions. Full effective access combines applicable policies and deployment constraints; `list` for an SSH path differs from `read` or credential issuance. An `ssh/creds/role` grant concerns that credential path, not unrestricted role configuration or all OS accounts. Use the existing role procedure when an actual owned OTP connection is required.

Finish with the active context, selected nonsecret metadata, policy/capability result and remaining effective-access facts. Authentication, helper persistence, policy inspection and actual service/OS operations are distinct results.

References: [login options](https://developer.hashicorp.com/vault/docs/commands/login), [read field selection](https://developer.hashicorp.com/vault/docs/commands/read), [lookup endpoint implementation](https://github.com/hashicorp/vault/blob/v1.19.0/command/token_lookup.go), [policy read](https://developer.hashicorp.com/vault/docs/commands/policy/read), and [ACL policy API](https://developer.hashicorp.com/vault/api-docs/system/policies).
