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
