---
name: chisel
description: Build and diagnose explicit Chisel port forwards or reverse SOCKS connections. Use when client/server direction, listener exposure, endpoint reachability or fingerprint authentication is unclear.
---

# Chisel tunnel direction

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

For reverse SOCKS, replace the remote with `R:127.0.0.1:1080:socks` and permit that reverse listener in the auth map. Consumers connect to the server-side SOCKS port; their traffic exits from the client. Server `--socks5` is for the other, server-side SOCKS mode and is not required by reverse SOCKS.

Diagnose transport connectivity/authentication, listener bind and destination reachability separately. Check actual listener addresses and a known application response. Keep TLS validation when using HTTPS in addition to the Chisel fingerprint. Stop the foreground client/server processes you started and verify both listeners close; reconnecting clients can otherwise restore tunnels.

Documentation reviewed 2026-10-09; Linux execution untested. Cases: Antique p. 8; Anubis p. 8; Appsanity p. 15. Source: [upstream remote syntax and authentication](https://github.com/jpillora/chisel#usage).
