---
name: consul
description: Inspect selected Consul KV data and validate existing agent configuration. Use when ACL behavior, datacenter selection or reload effects are confused with successful authentication.
---

# Consul KV and configuration inspection

Check `consul version` and the installed subcommand help. Establish the actual agent HTTP address, TLS policy and datacenter; a local forwarded port may reach a remote agent. Set `CONSUL_HTTP_ADDR` for the intended endpoint and use a private `CONSUL_HTTP_TOKEN_FILE` on versions supporting it, or supply the token through the process environment. Avoid literal token arguments and persistent shell-history entries.

Define `key` as one known KV key and `value_file` as a fresh private output. A read checks the permission actually needed:

~~~bash
umask 077
consul kv get -detailed "$key"
consul kv get "$key" >"$value_file"
~~~

Check each exit status. `-detailed` includes metadata such as ModifyIndex; ordinary get emits the value. Values can be binary or secret, so terminal output is not always appropriate. For a known prefix, `kv get -keys prefix/` lists keys without recursively printing all values. Set the intended datacenter with the verified `-datacenter` option when needed.

Do not use `kv put test ...` as an authentication check: it creates/overwrites a real key. Successful read, write, agent access and reload are distinct permissions. A denied request and an absent key are different outcomes; record the endpoint/datacenter/key and full diagnostic before changing credentials.

For an existing agent, inspect its actual service arguments to find every config file/directory. Define `config_dir` as the intended complete configuration directory:

~~~bash
consul validate "$config_dir"
~~~

Pass other actual config paths too when the service uses several. Validation checks configuration, not successful operation or permission to reload. A valid fragment alone can omit errors in the combined configuration.

`consul reload` changes a running agent and can activate checks. Script checks run commands with the agent's OS identity when enabled; writable configuration therefore matters independently of KV permissions. Inspect `enable_script_checks`, service identity and file permissions before planning any reload. Do not treat a health-check command as passive configuration.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Ambassador pp. 13–16. Sources: [KV get](https://developer.hashicorp.com/consul/commands/kv/get), [validate](https://developer.hashicorp.com/consul/commands/validate), [reload](https://developer.hashicorp.com/consul/commands/reload), [agent configuration](https://developer.hashicorp.com/consul/docs/agent/config/config-files).
