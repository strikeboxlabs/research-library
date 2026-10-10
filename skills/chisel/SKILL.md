---
name: chisel
description: Build and diagnose explicit Chisel port forwards or reverse SOCKS connections. Use when client/server direction, listener exposure, endpoint reachability or fingerprint authentication is unclear.
---

# Chisel tunnel direction

Read this entire SKILL.md before acting. Select transport/listener/destination roles and the needed authentication before starting the applicable forward. Finish with actual listener and application-response evidence, then stop the owned client/server and verify their listeners close; transport connection alone is incomplete.

Check both binaries' versions and `server --help`/`client --help`. Identify where the transport listener runs and where the final destination is reachable. Normal remotes reach destinations from the server; `R:` remotes reach them from the client. A transport connection alone does not prove the destination works.

Define `listen_ip` as the server interface reachable from the client, `transport_port` as a free unprivileged port, and `auth_file` as an existing private JSON map of the form `{"user:password":["^R:127\\.0\\.0\\.1:18631$"]}`, with real private credentials and the intended port. Reverse entries match `R:<bind-address>:<port>`, not the eventual target. Start in the foreground:

~~~bash
chisel server --host "$listen_ip" --port "$transport_port" --reverse --authfile "$auth_file"
~~~

Record the server fingerprint through the trusted setup channel. On the client, define `server_url`, `fingerprint`, `forward_port`, `destination_host` and `destination_port`. Supply the matching `user:password` in the client process's `AUTH` environment rather than literal command history:

~~~bash
chisel client --fingerprint "$fingerprint" "$server_url" "R:127.0.0.1:$forward_port:$destination_host:$destination_port"
~~~

The forward listens on the **server's** loopback and connects to the destination **from the client**. Choose a high local port even if the destination uses a privileged port. Explicit loopback avoids the all-interface default for ordinary port forwards. A destination of `127.0.0.1` means the client's loopback in this reverse example.

This fixed TCP forward expects the application's own protocol. Run the consumer on the server side against `127.0.0.1:$forward_port`; do not configure that endpoint as a SOCKS proxy. The transport port, forwarded listener and destination port have distinct roles even when two numbers happen to match. If the application opens a separate outbound connection, the forward does not automatically carry it; inspect that connection's endpoint and route separately.

For reverse SOCKS, replace the remote with `R:127.0.0.1:1080:socks` and permit that reverse listener in the auth map. Consumers connect to the server-side SOCKS port; their traffic exits from the client. Server `--socks5` is for the other, server-side SOCKS mode and is not required by reverse SOCKS.

Diagnose transport connectivity/authentication, listener bind and destination reachability separately. Check actual listener addresses and a known application response. Keep TLS validation when using HTTPS in addition to the Chisel fingerprint. Stop the foreground client/server processes you started and verify both listeners close; reconnecting clients can otherwise restore tunnels.

See [upstream remote syntax and authentication](https://github.com/jpillora/chisel#usage).
