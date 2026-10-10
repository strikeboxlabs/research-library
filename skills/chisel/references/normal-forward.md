# Client-side listener to server-side destination

Use a **normal** forward when the application can reach an interface on the Chisel client but the selected receiver runs beside the Chisel server. Map transport port, client-side forwarded listener and server-side final receiver independently. A reverse SOCKS connection does not automatically route an application's separate outbound callback.

Require reviewed Chisel binaries, trusted server fingerprint, reachable transport endpoint and an auth-map entry for the selected destination. Normal-remotes auth patterns match the target host/port, whereas reverse-remotes patterns match `R:<bind>:<port>`. Do not reuse a reverse-only permission pattern as normal-forward authorization.

Start the selected authenticated server without requiring reverse mode:

~~~bash
chisel server --host "$server_bind" --port "$transport_port" --authfile "$auth_file"
~~~

With matching private credentials in `AUTH`, define `server_url`, trusted `fingerprint`, `client_bind` as the interface the selected application can reach, and `client_port` as a free forwarded port. Define `receiver_host`/`receiver_port` as the **destination reachable from the server**:

~~~bash
chisel client --fingerprint "$fingerprint" "$server_url" "$client_bind:$client_port:$receiver_host:$receiver_port"
~~~

For a receiver beside the server, `receiver_host=127.0.0.1` reaches the server's loopback. `0.0.0.0` is a listener wildcard, not a reliable remote destination address. The application connects to the client-side address/port, and the tunnel then connects to the separately selected receiver. If the receiver listens on 80, forwarding to 8080 will not reach it merely because the client listener is 8080. Conversely a receiver on 8080 needs that destination port, regardless of prose describing port 80.

A fixed forward carries the chosen TCP protocol. An HTTP monitor with host/protocol/port inputs must point to the observed client-side listener; a SOCKS URL is not an HTTP destination. Verify actual binds, an owned harmless request and receiver evidence before arranging an authentication test. A healthy Chisel transport can coexist with connection refusal at the receiver.

Expose the client bind only as needed for the selected sender; loopback is suitable only when that sender shares the client's namespace. Stop the owned client/server after use and verify listeners are gone. Check [remote expansion/direction and authentication](https://github.com/jpillora/chisel#usage) against the installed build.
