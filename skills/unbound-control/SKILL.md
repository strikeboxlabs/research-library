---
name: unbound-control
description: Inspect an Unbound resolver's control status, counters and active forwarding policy. Use when control TLS, unsupported commands or DNS policy could explain a misleading result.
---

# Unbound control inspection

Read this entire SKILL.md before acting; reuse complete current context. Select the existing control configuration and endpoint, then use the inspection commands needed for the question. Finish with the command, response/exit status and what remains unverified; control reachability does not establish correct client DNS answers.

Use an existing authorized client configuration, including its referenced files. For TLS it needs the expected server certificate and the client certificate/private key; the server's private key is not a client prerequisite. Local Unix control sockets use filesystem permissions instead. Do not disable TLS or regenerate credentials to diagnose a failure.

Define `config` as that local configuration path and `control_endpoint` as the verified server IP, optionally followed by `@port`. For a configured local socket omit `-s` and use the configuration's endpoint. Check installed help before selecting commands:

~~~bash
unbound-control -h
unbound-control -c "$config" -s "$control_endpoint" status
~~~

Record its exit status immediately: documented `status` results are 0 for running, 3 for connection refused and 1 for other errors. Refusal at the selected address is not proof the resolver process is absent everywhere. Missing configuration/key permissions, TLS mismatch and unreachable listener require different repairs. Quiet mode `-q` intentionally suppresses successful output; silence alone proves neither TLS enforcement nor success.

For a counter snapshot without resetting it:

~~~bash
unbound-control -c "$config" -s "$control_endpoint" stats_noreset
~~~

`stats` can reset counters (subject to `statistics-cumulative`); `flush_stats` resets them explicitly. Preserve snapshot times and names when comparing values: daemon restarts or another collector's resets can break deltas. An **illustrative** `total.num.queries=42` describes a counter, not 42 successful client answers. Inspect the relevant answer/error counters and an actual client query before judging resolution.

When the question is active routing/local policy, use the matching read commands supported by the server:

~~~bash
unbound-control -c "$config" -s "$control_endpoint" list_forwards
unbound-control -c "$config" -s "$control_endpoint" list_local_zones
~~~

Compare the selected name against both policies. Included configuration can contain rules absent from the top-level file; an unreadable include leaves policy unknown. A successful empty list differs from `error unknown command`: check server/client versions or a custom build instead of reporting no policy. A help listing describes the client, not guaranteed server capabilities.

`forward_add` changes live resolution; its `+i` also adds a DNSSEC-insecure zone. It is not an inspection fallback. Cache flushing, reload and zone changes alter state and belong to an intended configuration change, not this diagnostic sequence.

References: [control commands](https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html), [configuration and control credentials](https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html).
