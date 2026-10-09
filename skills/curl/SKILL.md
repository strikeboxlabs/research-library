---
name: curl
description: Capture HTTP responses and construct API requests with curl while preserving hostname routing, TLS identity and request-path semantics. Use when encoding, status, transport failures or redirects obscure a result.
---

# curl HTTP evidence

Check `curl --version` for protocols/TLS backend and inspect local help for version-dependent switches. Define `url` as the exact scoped URL and `headers`/`body` as fresh private files:

~~~bash
umask 077
curl --silent --show-error --connect-timeout 5 --max-time 30 --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\npeer=%{remote_ip}\n' "$url"
~~~

Check curl's exit status immediately. Without `--fail`/`--fail-with-body`, a completed `404` or `500` response can still return zero. Keeping the body is useful for diagnosis; `--fail-with-body` gives an HTTP-error exit while retaining it on supporting versions. Transport failure with a partial body is not a complete response.

When DNS differs from the desired server, define `host`, `port` and `target_ip` and use a URL containing that hostname:

~~~bash
curl --silent --show-error --connect-timeout 5 --max-time 30 --resolve "$host:$port:$target_ip" --dump-header "$headers" --output "$body" "https://$host:$port/"
~~~

`--resolve` overrides the connection address while preserving URL hostname, HTTP Host, SNI and certificate-name checking. It is more complete than setting Host against an HTTPS IP URL. Check inherited proxy settings: a proxy can change where resolution/connections happen. Use the configured CA or an explicit trusted `--cacert` bundle rather than treating `-k` as a naming repair.

For an intentionally literal path test, `--path-as-is` preserves dot segments that curl otherwise normalizes; `--globoff` separately disables URL glob expansion. Neither prevents normalization by a proxy or server. Save the requested path and observed response together.

Inspect Location before adding `--location`; redirects can change hostname, method or authentication context. Do not forward credentials to new hosts automatically. A `500` after a mutating request does not prove rollback, so inspect state before retrying. Prefer structured status/body evidence over piping everything through `grep` for a version string.

For JSON/form APIs, validation errors and bearer-token handling, use [API request construction](references/api-requests.md).

For an HTTP proxy, explicit bypass control and CONNECT-versus-forwarding diagnosis, use [proxy requests](references/proxy-requests.md).

Documentation reviewed 2026-10-09; Linux execution untested. Cases: Ambassador pp. 5–7; Analytics pp. 3–5. Source: [curl manual](https://curl.se/docs/manpage.html).
