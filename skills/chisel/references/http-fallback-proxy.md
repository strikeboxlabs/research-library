# Serve an owned HTTP origin through the server fallback

Use when an approved HTTP origin is reachable from the Chisel server's namespace and the task requests an ordinary HTTP proxy endpoint. Require the installed server help, a free unprivileged listener and a known harmless upstream response. This uses the server's fallback handler; it needs no Chisel client or remote specification.

Define `proxy_port` and `upstream_origin` as the selected port and an HTTP(S) origin URL without a path prefix. Start the owned server in the foreground:

~~~bash
chisel server --host 127.0.0.1 --port "$proxy_port" --proxy "$upstream_origin"
~~~

In v1.7.6, server `--proxy` and `--backend` address the same setting. Later help may expose a different spelling. Client `--proxy` instead selects a proxy for the client's transport connection; it does not create this fallback. The fallback sends ordinary HTTP requests upstream from the server's namespace. Its upstream director changes the origin and Host while retaining the request path, so do not assume an upstream URL path becomes a prefix.

Observe the loopback listener and request the known public marker path with the application's approved HTTP client. Retain status/body plus upstream evidence where available. A server startup or TCP accept alone is insufficient. With fallback configured, `/health` and `/version` can also be forwarded rather than identifying Chisel itself. An upstream `X-Powered-By` header is an application claim, not verified PHP/FPM build evidence.

Chisel's SSH user authentication/fingerprint protects the tunneling protocol, not ordinary fallback HTTP requests. Keep this listener on loopback unless a separately designed exposure/access policy authorizes otherwise. Stop the foreground server after the task and verify its listener closes. Report unreachable origin, unexpected body or missing upstream evidence as the actual remaining gap.

See the [versioned CLI](https://github.com/jpillora/chisel/blob/v1.7.6/main.go), [proxy director](https://github.com/jpillora/chisel/blob/v1.7.6/server/server.go) and [fallback dispatch](https://github.com/jpillora/chisel/blob/v1.7.6/server/server_handler.go).
