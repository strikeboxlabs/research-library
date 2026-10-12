# Receive a selected Socket.IO event with an existing client

Use this when the observed service is Socket.IO rather than a native WebSocket. Select an already installed trusted socket.io-client build compatible with the server; do not invent Engine.IO packets or assume the latest client can talk to an older server. A source using client 2.x and `EIO=3` needs that protocol compatibility. A v3/v4 server can support legacy clients only with its corresponding compatibility configuration.

Identify the Socket.IO namespace, transport path, authentication and event contract from an authorized exchange. URL pathname selects the namespace; an option such as `path: "/socket.io/"` selects the transport endpoint. These are different. A successful transport upgrade does not establish an authenticated application subscription. Browser cookies/Origin handling do not automatically transfer to a Node CLI: supply the intended authorized session through the installed client's documented options. Keep TLS validation and separate browser policy from direct-client behavior.

Define `node_bin`, `client_module` (the verified absolute installed package entry/directory), `url` (including the intended namespace), a private `options_file` with reviewed client options/session material, and a private `subscription_file` with this application's selected event/payload. The subscription contract is an **illustrative shape**, with names such as `user_join` and `private_recv` used only after confirming them:

~~~json
{"join_event":"user_join","join_payload":{"username":"owned-test-user"},"receive_event":"private_recv"}
~~~

The join payload itself is an application action. Use the intended account/test identity; an arbitrary client-supplied username is not evidence of server-side identity. Register handlers before connecting, disable automatic reconnection for this bounded test, and capture one selected event privately:

~~~bash
umask 077
"$node_bin" --input-type=commonjs - "$client_module" "$url" "$options_file" "$subscription_file" > "$event_file" <<'JS'
const fs = require('node:fs');
const [clientModule, url, optionsFile, subscriptionFile] = process.argv.slice(2);
const exported = require(clientModule);
const io = typeof exported === 'function' ? exported : exported.io;
if (typeof io !== 'function') throw new Error('Client export does not match this driver');
const options = JSON.parse(fs.readFileSync(optionsFile, 'utf8'));
const sub = JSON.parse(fs.readFileSync(subscriptionFile, 'utf8'));
if (!sub.join_event || !sub.receive_event) throw new Error('Missing observed event names');
const socket = io(url, {...options, forceNew: true, reconnection: false,
  autoConnect: false, timeout: 5000});
let done = false;
const timer = setTimeout(() => finish(2, 'No selected event within observation window'), 15000);
function finish(code, reason) {
  if (done) return;
  done = true;
  clearTimeout(timer);
  process.exitCode = code;
  if (reason) console.error(reason);
  socket.disconnect();
}
socket.on('connect', () => socket.emit(sub.join_event, sub.join_payload));
socket.on(sub.receive_event, data => {
  const text = JSON.stringify({event: sub.receive_event, data});
  if (Buffer.byteLength(text, 'utf8') > 65536) return finish(2, 'Event exceeds capture budget');
  console.log(text);
  finish(0);
});
socket.on('connect_error', () => finish(1, 'Socket.IO connection/authentication error'));
socket.on('error', () => finish(1, 'Socket.IO error'));
socket.on('disconnect', () => finish(2, 'Disconnected before selected event'));
socket.connect();
JS
~~~

Define `event_file` as a fresh private capture before running. Review option credentials in that file without echoing them. The driver executes the selected trusted client module; unlike the resolver, it loads code and contacts the service. Its budgets are test choices, not protocol constants. No event within the window is incomplete observation, not proof of no private messages or no accessible subscription. A captured event establishes its payload under this session/route, not the entire chat history or identity claimed in the join.

Do not force WebSocket-only transport just to remove polling noise; proxies and client versions can need the normal polling/upgrade sequence. Header behavior differs between browser and Node transports and releases; use the matching client API for the actual options. Direct CLI success does not prove a browser can initiate/read the same exchange across origins.

Use polling-only transport when the observed route supports that mode and the compatible client exposes the option. In Engine.IO4 polling, the transport sid, Socket.IO namespace connection id and application-issued session identifier are separate values. HTTP POST success acknowledges transport delivery, not application authentication. Payload packets are separated by byte0x1e; ping2/pong3 are Engine.IO packets rather than native WebSocket control frames. Let the compatible client manage these details. See [Engine.IO protocol](https://socket.io/docs/v4/engine-io-protocol/).

See [2.x client API](https://socket.io/docs/v2/client-api/), [current client options](https://socket.io/docs/v4/client-options/) and [protocol migration/compatibility](https://socket.io/docs/v3/migrating-from-2-x-to-3-0/).
