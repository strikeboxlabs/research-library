---
name: redis-cli
description: Inspect selected Redis keys and persistence settings with redis-cli using known authentication and bounded cursor scans. Use when logical databases, ACLs, value types, effective configuration or SCAN completion make results ambiguous.
---

# Inspect the intended Redis data

Read this entire SKILL.md before acting. Select key inspection or the persistence-setting check below and establish the known endpoint/transport and configured authentication. For keys, select the logical database and permitted namespace, scan within the requested bounds and match reads to the value type. Finish with the selected result and its coverage limits, then leave the session. A connection or key name alone is insufficient.

Define `host`, `port`, `database` and `username` for the known endpoint, logical database and ACL account. For a password-authenticated session:

~~~bash
redis-cli --version
redis-cli -h "$host" -p "$port" -n "$database" --user "$username" --askpass
~~~

Use the known password at the prompt. For legacy password-only authentication omit `--user`; do not invent an account. When the service requires TLS, add `--tls` and its verified `--cacert` path plus any required client credentials. Changing transport or disabling certificate verification is not an authentication fix. Redis Cluster supports database zero only; a standalone server can expose multiple logical databases.

For the configured local Unix socket, define `socket` as its actual absolute path in this namespace and replace the host/port selection:

~~~bash
redis-cli -s "$socket" -n "$database" --user "$username" --askpass
~~~

`-s` overrides hostname/port. Socket filesystem access and Redis authentication/ACLs are separate requirements. Omit authentication options only when the selected service actually uses no password. A missing path or denied socket is a transport gap, not an empty database.

At the **Redis prompt**, start with the known namespace. This example uses a placeholder prefix to replace with the application's actual prefix:

~~~text
SCAN 0 MATCH app-prefix:* COUNT 100
TYPE app-prefix:observed-key
~~~

Each SCAN reply contains the next cursor and a key list. Continue with that returned cursor until it becomes zero, or stop at the task's call/time budget and report partial coverage. COUNT is a work hint, not a maximum result count. An empty page with a nonzero cursor is not completion; duplicates are possible, and a changing keyspace is not a consistent snapshot. Avoid `KEYS *` for routine discovery because it processes the whole keyspace in one blocking operation.

Check TYPE before reading a value. For a string, inspect STRLEN before a potentially large GET; for hashes prefer selected HGET/HMGET fields, and for lists use a bounded LRANGE. WRONGTYPE means the command does not fit the value's type, not that the database is corrupt. Nil/missing keys can also reflect expiry or a different selected database; ACL denial is a separate result.

Interactive output quotes/escapes bytes; `--raw` changes rendering and is the default when stdout is redirected. Preserve binary values accordingly. A field called password may contain ciphertext, an encoding or a verifier; inspect the producer's format before selecting a decoder or hash mode. Reading data does not require CONFIG SET, replication changes or destructive commands.

## Read selected persistence settings

For an approved configuration question, use the established session to read only the relevant nonsecret parameters. At the Redis prompt:

~~~text
CONFIG GET dir
CONFIG GET dbfilename
CONFIG GET appendonly
~~~

These read effective server settings, independently of the selected logical database. One parameter per call also works before Redis 7; multiple parameters in one call require Redis 7 or later. Interpret returned names and values rather than assuming the CLI's RESP2 array rendering is universal. A denied command is a configuration-access gap, and an empty result can mean an unsupported/unmatched parameter; neither means an empty database.

Combine `dir` and `dbfilename` only to describe the configured RDB location in the server's filesystem namespace. This does not prove a snapshot exists, its freshness, directory contents or access permissions. `appendonly` selects whether AOF is enabled; it does not establish the AOF's health. Do not test path existence by changing `dir`: that changes server state. Retain the selected values, endpoint/time and unresolved filesystem or persistence evidence. A broad `CONFIG GET *` can disclose unrelated secrets and is unnecessary for this task.

See [redis-cli transport/authentication options](https://redis.io/docs/latest/develop/tools/cli/), [SCAN guarantees](https://redis.io/docs/latest/commands/scan/) and [CONFIG GET semantics and version history](https://redis.io/docs/latest/commands/config-get/).
