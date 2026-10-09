# HTTP proxy requests

Use curl's native proxy support to make the route explicit. Define `proxy_url` as the selected proxy URL, `url` as one known in-scope HTTP endpoint reachable from it, and `headers`/`body` as fresh private files:

~~~bash
umask 077
curl --proxy "$proxy_url" --noproxy '' --silent --show-error --connect-timeout 5 --max-time 20 --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\nconnect=%{http_connect}\npeer=%{remote_ip}\n' "$url"
~~~

The empty `--noproxy` deliberately overrides inherited bypass lists so this selected request uses the proxy. Without it, `NO_PROXY` can bypass even an explicitly supplied proxy, especially for loopback. A destination URL containing `127.0.0.1` is reached from the HTTP proxy's context, not the workstation's. Preserve URL hostname/port and inspect redirects before following them.

For an HTTP destination, ordinary `--proxy` uses HTTP forwarding. `--proxytunnel` instead requests CONNECT to the destination host/port. HTTPS through an HTTP proxy normally uses CONNECT before origin TLS. A proxy may allow ordinary HTTP forwarding while denying CONNECT to that same port; these are different tests. Native forwarding and ProxyChains' HTTP mode are therefore not interchangeable.

`http_connect` describes the proxy's CONNECT response when one occurs; it is not the origin application's status. The connected peer can be the proxy. Inspect headers/body to distinguish proxy-generated denial/error pages, proxy authentication (`407`), origin authentication and actual application responses. A proxy-branded `200` or absence of one particular error sentence is not proof that a destination service is open.

Check curl's exit status before accepting a body; transport errors/timeouts can leave partial evidence. For TLS, distinguish trust of an HTTPS proxy (`--proxy-cacert`) from origin trust (`--cacert`). Do not disable both checks to diagnose a naming error. Proxy traces can expose authentication headers and internal destinations; keep only needed diagnostics privately.

Bamboo's scanner classifies responses using one Squid error phrase. Validate an interesting result with a bounded request and the actual protocol; an HTTP-only probe is not a general TCP port inventory.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Bamboo pp. 2–5. Sources: [curl proxy and write-out options](https://curl.se/docs/manpage.html), [reviewed scanner implementation](https://gist.githubusercontent.com/xct/597d48456214b15108b2817660fdee00/raw/f1fff423d457655b0740699acf4a61126804d16f/squidscan.go).
