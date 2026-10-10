# HTTP proxy requests

Use curl's native proxy support to make the route explicit. Define `proxy_url` as the selected proxy URL, `url` as one known in-scope HTTP endpoint reachable from it, and `headers`/`body` as fresh private files:

~~~bash
umask 077
curl --proxy "$proxy_url" --noproxy '' --silent --show-error --connect-timeout 5 --max-time 20 --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\nconnect=%{http_connect}\npeer=%{remote_ip}\n' "$url"
~~~

The empty `--noproxy` deliberately overrides inherited bypass lists so this selected request uses the proxy. Without it, `NO_PROXY` can bypass even an explicitly supplied proxy, especially for loopback. A destination URL containing `127.0.0.1` is reached from the HTTP proxy's context, not the workstation's. Preserve URL hostname/port and inspect redirects before following them.

When a Linux wrapper relies on inherited settings, curl accepts `http_proxy` only in lowercase; uppercase `HTTP_PROXY` is deliberately ignored. Other supported proxy variables accept uppercase variants, with lowercase taking precedence. Record the effective environment and bypass rules before diagnosing an unobserved proxy request; environment-name behavior on Windows cannot establish Linux casing behavior.

For an HTTP destination, ordinary `--proxy` uses HTTP forwarding. `--proxytunnel` instead requests CONNECT to the destination host/port. HTTPS through an HTTP proxy normally uses CONNECT before origin TLS. A proxy may allow ordinary HTTP forwarding while denying CONNECT to that same port; these are different tests. Native forwarding and ProxyChains' HTTP mode are therefore not interchangeable.

`http_connect` describes the proxy's CONNECT response when one occurs; it is not the origin application's status. The connected peer can be the proxy. Inspect headers/body to distinguish proxy-generated denial/error pages, proxy authentication (`407`), origin authentication and actual application responses. A proxy-branded `200` or absence of one particular error sentence is not proof that a destination service is open.

Check curl's exit status before accepting a body; transport errors/timeouts can leave partial evidence. For TLS, distinguish trust of an HTTPS proxy (`--proxy-cacert`) from origin trust (`--cacert`). Do not disable both checks to diagnose a naming error. Proxy traces can expose authentication headers and internal destinations; keep only needed diagnostics privately.

A scanner that classifies responses using one Squid error phrase can misidentify an endpoint. Validate an interesting result with a bounded request and the actual protocol; an HTTP-only probe is not a general TCP port inventory.

## Forwarded headers do not choose the network route

`--header "X-Forwarded-For: $claimed_ip"` changes HTTP request content. It does not use a proxy, bind a source address or make the connection originate at that claimed IP. Preserve the real route and distinguish its connected peer from application-reported client identity.

For an authorised comparison of header-dependent behavior, first capture the selected URL with the entrypoint's normal command. Keep URL, method, cookies and route unchanged; use fresh output files for the second request and add only the header with the agreed test value. Compare complete status/body pairs, including login/fallback/error content. A changed response supports a dependency on that input in this context, not independent proof of the entire authentication path. Repeated uncontrolled guesses change the task and obscure the comparison.

A proxy may append, replace or strip supplied forwarding headers. Security decisions need the configured trusted proxy chain and observed server-side handling; neither the first comma-separated value nor any client-supplied address is inherently authoritative. Request traces can help show what curl sent, while server/proxy logs are needed to establish what was trusted. See [forwarded-header trust and parsing](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-For).

Consult the [curl proxy, environment and write-out manual](https://curl.se/docs/manpage.html) for option precedence and platform differences.
