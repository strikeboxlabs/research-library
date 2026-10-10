# Diagnose one stateful WebSocket exchange

Use a trusted Python environment that already contains **websocket-client** (import name `websocket`). This is separate from the `websockets` package. Inspect the endpoint's client code or a known exchange first: URL, Origin/session requirements, greeting, token rotation, message schema and reply correlation all matter. Keep TLS verification for `wss://`; a missing dependency is not permission to install one.

The example below is for a native WebSocket protocol that greets with a JSON `token`, accepts `{"token": ..., "message": "help"}`, and replies with one JSON object. It handles the documented application text `ping`/`pong` as well as protocol control frames. Define `python_bin` and the scoped `ws_url`; adapt authentication/Origin from the actual contract without hardcoding secrets. Do not use it unchanged for multiplexed event streams or another schema.

~~~bash
"$python_bin" -I - "$ws_url" <<'PY'
import json
import sys
import time
from websocket import ABNF, create_connection

ws = create_connection(sys.argv[1], timeout=5)
deadline = time.monotonic() + 15

def receive_object():
    for _ in range(32):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("Application reply deadline expired")
        ws.settimeout(min(5, remaining))
        opcode, payload = ws.recv_data(control_frame=True)
        if opcode == ABNF.OPCODE_CLOSE:
            raise RuntimeError("Peer closed before application reply")
        if opcode in (ABNF.OPCODE_PING, ABNF.OPCODE_PONG):
            continue
        if opcode != ABNF.OPCODE_TEXT:
            raise ValueError("Unexpected binary application message")
        text = payload.decode("utf-8") if isinstance(payload, bytes) else payload
        if text == "ping":
            ws.send("pong")
            continue
        obj = json.loads(text)
        if not isinstance(obj, dict):
            raise ValueError("Expected a JSON object")
        return obj
    raise RuntimeError("No application reply within frame budget")

try:
    greeting = receive_object()
    token = greeting.get("token")
    if not isinstance(token, str) or not token:
        raise ValueError("Missing greeting token")
    ws.send(json.dumps({"token": token, "message": "help"}))
    reply = receive_object()
    print(json.dumps({k: reply[k] for k in ("status", "message") if k in reply}))
finally:
    ws.close(timeout=1)
PY
~~~

The library handles WebSocket control-ping replies; sending the text `pong` is a different, application-specific action. JSON serialization preserves quoting; interpolating query text into hand-built JSON can change the message. Keep the latest response token only when the protocol says to rotate it. For concurrent requests/events, use the observed response identifier/type; the next received object need not answer the last request.

Inspect the returned help content/status, not merely a successful upgrade or parse. An empty summary means the assumed fields do not match; it is not application success. Preserve a private bounded capture when diagnosing unexpected messages, while excluding tokens from general logs. Timeouts, close, malformed JSON and exhausted budgets leave the exchange incomplete. The deadline is checked between received frames, not a hard process runtime cap against a peer dripping fragmented data; use the worker's runtime budget when required.

Socket.IO adds Engine.IO/Socket.IO framing, event semantics and version compatibility over its transport. A `/socket.io/` request with `EIO=...` or polling frames should send you to an already available matching Socket.IO client, not this native-WebSocket example. A transport connection is not an authorized event subscription.

References: [websocket-client API and control frames](https://websocket-client.readthedocs.io/en/latest/core.html), [Socket.IO protocol distinction](https://socket.io/docs/v4/).
