---
name: redis-cli
description: Inspect selected Redis keys, server metadata and persistence settings with redis-cli using known authentication and bounded cursor scans. Use when logical databases, ACLs, value types, build identity, closed connections or SCAN completion make results ambiguous.
---

# Inspect the intended Redis data

Read this entire SKILL.md before acting. Select key inspection, server metadata or the persistence-setting check below and establish the known endpoint/transport and configured authentication. For keys, select the logical database and permitted namespace, scan within the requested bounds and match reads to the value type. Finish with the selected result and its coverage limits, then leave the session. A connection or key name alone is insufficient.

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

Distinguish a server error reply from connection loss. An **illustrative** argument-free GET returning `wrong number of arguments` identifies a recognized command with incomplete input; no value was read. `unknown command` is a different lookup failure. A CLI message that the server closed the connection establishes neither command completion nor an empty result: retain the preceding response and check the selected server's logs, transport and policy before reconnecting with the established settings. Redis's HTTP-protection handling can close a connection instead of issuing an ordinary command error; an HTTP method name is not a Redis data-read operation. Use the installed version's [response format](https://redis.io/docs/latest/develop/reference/protocol-spec/) and [server command checks](https://github.com/redis/redis/blob/7.0/src/server.c) to resolve ambiguous transcripts.

Interactive output quotes/escapes bytes; `--raw` changes rendering and is the default when stdout is redirected. Preserve binary values accordingly. A field called password may contain ciphertext, an encoding or a verifier; inspect the producer's format before selecting a decoder or hash mode. Reading data does not require CONFIG SET, replication changes or destructive commands.

## Inspect selected server metadata

In the established known-authentication session, request the relevant server section at the Redis prompt:

~~~text
INFO server
~~~

This reads server metadata independently of the selected logical database; it does not enumerate key values or change settings. Preserve relevant returned fields such as redis_version, redis_build_id, redis_mode, process_id, run_id and uptime alongside the endpoint/time. Fields vary with version; missing or unfamiliar fields are not automatically errors. NOAUTH means this operation lacks authentication; NOPERM is an ACL denial after authentication. Neither is an empty server response to interpret as a version.

An acquired program's printed INFO output is a historical application observation, not proof of your direct session's authentication or of the same running process. A pathname or PID needs namespace/time correlation before attributing OS ownership. A build ID is not an independently verified executable digest, and a numeric version alone does not establish distribution patch state or advisory applicability. For packaging-specific issues, match installed vendor package/build records with its advisory; do not execute an exploit or change server settings to validate a version lead. Finish with the selected fields and remaining package/process association. See [INFO sections and field meanings](https://redis.io/docs/latest/commands/info/).

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
