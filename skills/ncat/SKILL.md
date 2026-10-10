---
name: ncat
description: Inspect simple TCP services with Nmap Ncat, including Memcached slab statistics and selected values. Use when line endings, EOF, timeouts or incomplete cache listings make protocol evidence ambiguous.
---

# Ncat protocol interaction

Check `ncat --version` and `ncat --help`. Nmap Ncat, OpenBSD nc and traditional netcat have different options; a walkthrough's `nc -lvnp` is not a portable Ncat recipe. This skill covers direct service interaction, not attaching a command interpreter to a socket.

Define `host` and `port` as the selected service, often an already-established local forward:

~~~bash
ncat --verbose --wait 5s --idle-timeout 20s "$host" "$port"
~~~

`--wait` limits connection establishment; `--idle-timeout` ends an inactive session, not the total duration of an active one. A connected socket without a banner may be waiting for a request. Use the observed protocol's harmless help/status request; don't send arbitrary HTTP or binary probes to an unknown service.

For a documented CRLF line protocol, `--crlf` translates stdin line endings. Do not add it to binary transfers or preformatted CRLF data. Ncat does not implement full Telnet negotiation; use a protocol-aware client when negotiation matters.

For a finite request, define `request_file` as the exact wire-format input and `response_file` as a fresh destination:

~~~bash
ncat --wait 5s --idle-timeout 20s "$host" "$port" <"$request_file" >"$response_file"
~~~

By default, stdin EOF shuts down the sending side while response reading can continue. `--send-only` ignores responses and quits at input EOF, so it is unsuitable when a reply is the evidence. `--recv-only` never sends input. `--no-shutdown` changes half-close behavior and can make the session wait until the peer or timeout closes it; choose it only for a protocol requiring that behavior.

An open TCP port proves transport availability, not application authentication or command success. Retain stderr separately from protocol bytes when automating. For TLS, use the installed Ncat TLS/verification options and the intended hostname; plain Ncat against a TLS service produces misleading silence or binary output.

## Read Memcached statistics and a selected key

Use this only for an identified Memcached endpoint supporting the plaintext basic text protocol. Set `host`/`port` to that service; loopback refers to the machine running Ncat. TLS or authentication requirements need the matching transport/client.

~~~bash
printf 'version\r\nstats items\r\nquit\r\n' |
  ncat --wait 3s --idle-timeout 3s "$host" "$port"
~~~

Expect a `VERSION` line and statistics ending in `END`. **Illustrative:** `STAT items:1:number 5` means five stored items in slab class 1; it does not mean one item numbered 1. Counts can include expired items not yet reclaimed. One `quit` closes the connection. Missing terminators or a timeout leave incomplete evidence; a connection alone is not a successful query. Do not add `--crlf` to these already framed bytes.

If a limited legacy key listing is needed, define `slab` as an observed positive numeric class ID:

~~~bash
printf 'stats cachedump %s 10\r\nquit\r\n' "$slab" |
  ncat --wait 3s --idle-timeout 3s "$host" "$port"
~~~

The second number caps returned items; zero means no requested count cap, not zero items. Server limits and LRU implementation still apply, so this is not a complete cache inventory or backup. `CLIENT_ERROR` can mean the server disabled dumping; preserve that limitation instead of changing its settings. A returned key may disappear before retrieval.

For one required known key, define `key` as its exact protocol key (1–250 bytes, without spaces or control characters) and `response_file` as a fresh private destination:

~~~bash
umask 077
printf 'get %s\r\nquit\r\n' "$key" |
  ncat --wait 3s --idle-timeout 3s "$host" "$port" >"$response_file"
~~~

A hit has `VALUE key flags bytes`, followed by exactly that many data bytes, CRLF, and finally `END`. Flags are opaque client metadata; the length excludes framing. Values may be binary or contain newlines, so use a protocol-aware parser for extraction rather than treating each line as a record. `END` alone means a miss at that moment, not proof that the key never existed. A cached password-like value is application data; it does not prove current account validity.

See the [basic protocol](https://docs.memcached.org/protocols/basic/) and [wire-format reference](https://github.com/memcached/memcached/blob/master/doc/protocol.txt) for response framing. Legacy cachedump behavior varies by server version. The [Ncat manual](https://nmap.org/book/ncat-man.html) documents transport and EOF options.
