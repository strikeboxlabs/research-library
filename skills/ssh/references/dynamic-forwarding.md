# Dynamic forwarding and DNS

Use this when an established SSH account permits forwarding to a selected service you administer. Identify the SSH endpoint, its verified host key, the destination service and the consuming client. Obtain the service's expected URL/hostname and certificate trust before connecting. A SOCKS listener is a client-side TCP proxy, not a general VPN or a new listener on the remote service.

Define `ssh_host` and `user` for that account, and `socks_port` as a free high port on the Linux client. Keep the initial connection in the foreground:

~~~bash
ssh -N -T -o ExitOnForwardFailure=yes -D "127.0.0.1:$socks_port" "$user@$ssh_host"
~~~

`-D` accepts SOCKS4/5 requests at the explicitly bound local loopback address. SSH then opens each requested TCP connection from the SSH server. `-N` requests no remote command; `-T` requests no terminal. A quiet connection is normal. Authentication and successful listener creation do not prove the selected destination will accept a later connection; `ExitOnForwardFailure` cannot test that future request.

The OpenSSH dynamic SOCKS5 listener negotiates no-authentication for its local proxy protocol. The SSH account authenticates the transport separately; copying that account's password into a browser or ProxyChains SOCKS entry is unnecessary and does not authenticate the destination application. Keep this listener loopback-bound and configure the consumer for the actual local endpoint. See the upstream [SOCKS negotiation](https://github.com/openssh/openssh-portable/blob/master/channels.c).

For a known HTTP(S) endpoint, use curl in a second terminal. Define `url` as that service's complete approved URL, and `headers` and `body` as fresh files in a private working directory. They can contain application data or session identifiers.

~~~bash
curl --proxy "socks5h://127.0.0.1:$socks_port" --noproxy "" \
  --connect-timeout 5 --max-time 20 \
  --dump-header "$headers" --output "$body" --url "$url"
status=$?
~~~

The empty `--noproxy` overrides a configured proxy exclusion for this request. Choose the DNS location deliberately:

| Proxy scheme | Where the destination name is resolved |
|---|---|
| `socks5h://` | The SOCKS server side, through the SSH server's resolver context. |
| `socks5://` | The curl client; SSH subsequently connects from the server to the resulting address. |

The address of the SOCKS listener itself is always local. A destination URL containing `127.0.0.1` instead addresses the SSH server's loopback. A client's hosts-file entry does not configure the remote resolver. A browser's SOCKS proxy and remote-DNS preferences must match the intended model; verify the actual browser settings before attributing a different result to the service. Record and restore temporary client settings afterward.

Keep the application's hostname in `url` so HTTP Host and HTTPS SNI/certificate identity remain meaningful. Use the verified private CA when required, rather than disabling certificate verification. Follow a redirect only after checking that its destination remains within the selected service scope.

Inspect both `status` and the saved HTTP status/response. Without `--fail`, an HTTP 403 or 500 can accompany a zero curl exit: transport completed, but the application denied or failed the request. A dashboard greeting is an application identity, not the SSH operating-system account.

If binding fails, choose a free port or identify its owner. If SSH reports forwarding administratively prohibited, inspect the account's forwarding policy; changing credentials does not resolve a destination restriction. For a name-resolution error, check the resolver corresponding to the selected proxy scheme. For a connection refusal, check the selected service's address, port and listener from the SSH server's context. Do not infer that every remote service is reachable from one successful connection.

Finish with the observed SSH account, local listener, DNS choice and selected application's response, or the specific unresolved dependency. Stop the foreground SSH connection with Ctrl-C and verify that its listener closes. A separately configured multiplexed/background connection needs its own lifetime tracking.

References: [OpenSSH dynamic forwarding](https://man.openbsd.org/ssh.1), [curl proxy and DNS options](https://curl.se/docs/manpage.html).
