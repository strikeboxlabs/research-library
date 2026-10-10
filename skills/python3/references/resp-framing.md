# Encode a protocol command without losing argument bytes

Use this branch for a reviewed RESP command encoder or a selected Redis transport test. RESP bulk lengths count bytes and an array preserves distinct command arguments. `command.split(" ")` destroys spaces inside a value; `len(text)` miscounts UTF-8. Preserve serialized artifacts as bytes, including NULs and final newlines.

Use the supplied **required encoder** [scripts/resp_frame.py](../scripts/resp_frame.py), defining `resp_script` as its absolute installed path and `python_bin` as the trusted interpreter. It reads one exact argument per file, emits one command and performs no network I/O. For an inert local PING frame, define fresh private `command_file`, `frame_file` and optionally `json_string_file`:

~~~bash
umask 077
printf '%s' PING > "$command_file"
"$python_bin" -I -S "$resp_script" "$command_file" > "$frame_file"
"$python_bin" -I -S "$resp_script" --json-string "$command_file" > "$json_string_file"
~~~

The raw PING frame is **illustrative bytes** `*1\r\n$4\r\nPING\r\n`, where the displayed escapes denote actual CR/LF bytes. For a permitted SET, supply three files containing the exact command, selected key and value as separate positional arguments; no spaces/newlines are trimmed. The encoder neither validates Redis command semantics nor sends it. Use bounded known fixture values and inspect status/byte length before consuming output. Large argument files are read into memory; choose files within the task's resource budget.

`--json-string` produces one JSON string value, not a complete API request. A serializer must insert its decoded value into the actual schema. It requires UTF-8-representable data; raw mode supports arbitrary bytes. JSON preserves escaped control characters in a string, but the receiving application can reject, transform or re-encode them. Byte equality must be checked after that transformation before claiming delivery. Do not append QUIT or multiple commands merely because a copied helper did so.

For an authorized CRLF-capable webhook transport, first establish callback byte placement with an owned listener and inert marker. The outer HTTP method and JSON field containing an inner method are different values; protocol validity on Redis additionally requires reachability, authentication/ACLs and accepted framing. Redis can reject cross-protocol HTTP traffic; an HTTP callback does not establish its command acceptance. Preserve a reply or an independently observed fixture effect. A hidden error/body leaves read results uncertain. Prefer bounded known keys; SCAN requires cursor iteration and is not a snapshot, while KEYS over a shared keyspace can be expensive. Database-wide deletion is not a diagnostic control. Session changes require the exact driver/key/TTL and selected fixture restoration, not a guessed cookie string. See [RESP framing](https://redis.io/docs/latest/develop/reference/protocol-spec/), [SCAN limitations](https://redis.io/docs/latest/commands/scan/) and [Redis security](https://redis.io/docs/latest/operate/oss_and_stack/management/security/).
