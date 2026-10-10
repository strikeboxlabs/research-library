# Read a backend protocol through an HTTP socket bridge

Use only for an observed application route that opens a selected server-side TCP socket and returns its response. Establish the destination host/port, accepted command characters, HTTP authentication and response wrapper first. These commands adapt a browser-driven operation to curl; curl is the HTTP client, not a native Memcached client.

Define `socket_url` as the exact authorized route, `backend_port` as its selected observed TCP port, `cookie_file` as a private Netscape-format jar for its established session/gate, and fresh `headers`/`body` files per request. The following field names apply to a route actually using `port` and `cmd`:

~~~bash
umask 077
curl --silent --show-error --connect-timeout 5 --max-time 30 --get --cookie "$cookie_file" --data-urlencode "port=$backend_port" --data-urlencode 'cmd=stats slabs' --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\n' "$socket_url"
~~~

Check transport status and the application body. HTTP 200 can contain access denial or socket failure. Curl's total timeout bounds the HTTP operation; it does not prove the backend task was cancelled. The server's socket timeout/framing can truncate a result.

`--get --data-urlencode` preserves the parameter boundary and encodes a space without shell parsing. Confirm the route's actual decoding/filter behavior; literal `+` and decoded space need not be equivalent at every stage. A numeric port label alone does not identify the protocol, and this TCP route is not a UDP client.

## Follow Memcached's slab evidence to a selected key

When an independently confirmed Memcached ASCII response is returned, `stats slabs` identifies allocation classes; `stats items` describes their items. A class number is related to configured chunk sizes, not a stable table/database name. A class with one used chunk can contain one application object holding many records.

For a legacy server supporting key dumping, select a class from this response and a modest output limit. Set `command="stats cachedump $class_id $limit"` and use the same capture command with `--data-urlencode "cmd=$command"`. `ITEM key [size b; timestamp s]` supplies a key and metadata, not its value. This legacy dump is partial, version-dependent and can hold a class lock; lack of a listed key does not prove absence. Do not increase its limit merely to force a complete inventory. If supported and appropriate, `lru_crawler metadump` is a different metadata enumeration with its own scope/output limits; it is not a value export or atomic snapshot.

Once `cache_key` is an observed ASCII-protocol key (no spaces/control characters, within the server's length limit), retrieve that key with `command="get $cache_key"` through the same HTTP capture. A raw backend response has this **illustrative** shape:

~~~text
VALUE accounts 0 37
{"alice":"digest-a","bob":"digest-b"}
END
~~~

The illustrative payload is 37 ASCII bytes; determine the actual byte length from the captured raw value rather than transplanting this count. `VALUE` describes a byte-counted payload; `END` terminates retrieval. `END` alone is a miss at that time, not proof the key never existed. A key can expire/change between listing and get. Protocol errors, an incomplete frame or the HTTP bridge's output cap remain incomplete evidence.

If the application renders data inside HTML `<pre>`, extract the actual element and decode **one known HTML presentation layer** before processing the inner format. Do not globally replace `&#34;` in a whole response or repeatedly unescape inner JSON strings: a literal entity can be application data. Browser-displayed text may already be decoded. Backend `<bytes>` counts raw payload bytes, not escaped HTML length. Validate the full retrieved JSON and expected application shape separately; parsed JSON does not establish cache freshness or current OS authentication.

Retain only the needed selected records privately. A cached username-to-digest object supplies account/hash candidates; it is not a consistent database backup or proof that every application user exists as an OS account. Next decisions are schema-aware extraction, offline format testing and, only when selected, separate identity/authentication confirmation. Cache writes, flushes and storage commands are outside this read task.

Use the [Memcached basic protocol](https://docs.memcached.org/protocols/basic/), [framing and crawler protocol](https://github.com/memcached/memcached/blob/master/doc/protocol.txt) and [legacy cachedump implementation](https://github.com/memcached/memcached/blob/master/items.c) for server-version differences; [curl's option manual](https://curl.se/docs/manpage.html) defines the HTTP capture.
