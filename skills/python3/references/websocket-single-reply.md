# Capture one legitimate application reply

Require the application's established native-WebSocket endpoint and a legitimate request contract. Use a trusted installed `websockets` environment, distinct from `websocket-client`. The example requires its modern `websockets.asyncio.client` API and Python 3.11+ for `asyncio.timeout`; historical 10.4 imports differ. Confirm the installed version before choosing this branch.

Define `ws_url` as the owned endpoint and `version` as the application's ordinary version string. This **illustrative version-query contract** sends one object without waiting for a greeting. Adapt it only to the observed legitimate schema and authentication/Origin requirements:

~~~bash
"$python_bin" -I - "$ws_url" "$version" <<'PY'
import asyncio
import json
import sys
from websockets.asyncio.client import connect

async def query():
    async with asyncio.timeout(15):
        async with connect(sys.argv[1], open_timeout=5, close_timeout=1,
                           max_size=65536, proxy=None) as ws:
            await ws.send(json.dumps({"version": sys.argv[2]}))
            raw = await ws.recv()
            if not isinstance(raw, str):
                raise ValueError("Expected a text reply")
            reply = json.loads(raw)
            if not isinstance(reply, dict):
                raise ValueError("Expected an object reply")
            print(json.dumps(reply))

asyncio.run(query())
PY
~~~

`proxy=None` makes this selected direct connection explicit; it is not suitable where the approved route requires a proxy. Keep TLS verification for `wss://`. A close, deadline expiry or JSON/schema error leaves the query unresolved. Retain a bounded private reply and validate the contract's actual result fields; successful connection/parsing alone does not prove an update exists. Distinct URL paths can return different schemas despite sharing a port.

The library handles control ping/pong. An application that greets, rotates tokens, multiplexes events or requires response IDs needs its corresponding state/correlation logic; the next received object need not answer the request. An HTTP 400 from a generic probe can mean an invalid upgrade request rather than absence of a WebSocket service.

References: [asyncio connection, reply and proxy API](https://websockets.readthedocs.io/en/stable/reference/asyncio/client.html), [asyncio deadline context](https://docs.python.org/3/library/asyncio-task.html#asyncio.timeout).
