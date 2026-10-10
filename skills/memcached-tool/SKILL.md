---
name: memcached-tool
description: Inspect Memcached statistics, slab use and bounded key listings with the upstream memcached-tool helper. Use to avoid rebuilding text-protocol queries and distinguish cache evidence from a complete or consistent backup.
---

# Inspect the cache with its existing helper

Read this entire file before acting. Choose statistics, key metadata or value export deliberately. Finish with the endpoint, supported mode and observed result, including server/client errors and coverage limits.

This skill is for the upstream Perl `memcached-tool`, not similarly named clients. Inspect its installed usage. Set `endpoint` to the authorized `host:port` or Unix socket path; the helper uses the basic text protocol and does not provide a general TLS/SASL client.

~~~bash
memcached-tool "$endpoint" stats
memcached-tool "$endpoint" display
memcached-tool "$endpoint" settings
~~~

`display` summarizes slab classes; a class number is an allocation class, not an item identifier. General statistics such as hits, misses and evictions are cumulative counters: compare changes over a known interval and account for uptime/restarts. A hit ratio needs both the chosen interval and workload context; a single lifetime ratio does not diagnose the present incident. Inspect per-class pressure rather than treating free memory in one class as immediately available to all object sizes.

For builds supporting the current bounded key mode:

~~~bash
memcached-tool "$endpoint" keys 10
~~~

The helper requests crawler metadata and limits what it consumes; ten printed keys do not mean the server holds only ten or that the server's work was restricted to ten. Keys may be URL-escaped; `keys -u 10` decodes them for presentation, which can introduce ambiguous whitespace/control characters. Preserve the original form when exact keys matter. Disabled/unsupported crawler commands are a coverage limitation, not an empty cache.

Only when value export is required, define `dump_file` as a fresh private path:

~~~bash
umask 077
memcached-tool "$endpoint" dump 10 > "$dump_file"
~~~

The output is a cache-loading command stream, not JSON or a selected-key lookup. Values can expire or change between listing and retrieval, and binary content must not be parsed as newline-delimited records. Do not feed the dump back into a server during inspection. For one known key, choose a client that supports direct get instead of exporting arbitrary entries.

Avoid `sizes` as a routine health check: behavior and blocking costs vary by server version. `move` concerns slab reassignment and changes state. A password-like value is cached application data, not proof it still authenticates an account. See [upstream modes and implementation](https://github.com/memcached/memcached/blob/master/scripts/memcached-tool) and [Memcached protocol](https://docs.memcached.org/protocols/basic/).
