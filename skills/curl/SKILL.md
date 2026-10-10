---
name: curl
description: Capture HTTP responses and construct API, GraphQL or Spring Boot management requests with curl while preserving hostname routing, TLS identity and request-path semantics. Use when encoding, partial results, transport failures, config-driven transfers or redirects obscure a result.
---

# curl HTTP evidence

Read this entire skill before acting; complete current context need not be re-read. Preserve the intended URL/route, capture status and body from the same request, and distinguish transport completion from application success. Read the applicable reference fully before its procedure; leave unrelated branches unloaded.

- Webhook callbacks, outbound method injection, alias/file transformations or mass-assigned account fields: [controlled application tests](references/webhook-and-file-tests.md), using the API/session references as applicable.
- Neo4j/Cypher authentication queries or shell-running custom procedures: [Cypher and process boundaries](references/cypher-and-procedures.md).
- JSON/form APIs, multipart uploads, file PUTs and token handling: [API request construction](references/api-requests.md).
- Cookie-bound CSRF requests or a browser-only failure: [session and preflight diagnosis](references/session-and-preflight.md).
- GraphQL schema, variables and operation errors: [GraphQL requests](references/graphql.md).
- Spring Boot management discovery and mapping interpretation: [Actuator responses](references/spring-actuator.md).
- Proxy routing, CONNECT and forwarded-header interpretation: [proxy requests](references/proxy-requests.md).
- Scheduled `-K` transfers, writable URL/output configs or inherited curlrc: [config transfer boundaries](references/config-transfers.md).

Check `curl --version` for protocols/TLS backend and inspect local help for version-dependent switches. Define `url` as the exact scoped URL and `headers`/`body` as fresh private files:

~~~bash
umask 077
curl --silent --show-error --connect-timeout 5 --max-time 30 --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\npeer=%{remote_ip}\n' "$url"
~~~

Check curl's exit status immediately. Without `--fail`/`--fail-with-body`, a completed `404` or `500` response can still return zero. Keeping the body is useful for diagnosis; `--fail-with-body` gives an HTTP-error exit while retaining it on supporting versions. Transport failure with a partial body is not a complete response.

A name mentioned inside `Access-Control-Expose-Headers` or `Access-Control-Allow-Headers` is CORS policy data, not evidence that a response contains that named header. Likewise, allowed methods do not prove those operations are accepted or authorized. Check actual header fields, status and body before fingerprinting a service or inferring object versioning. A generic JSON health response establishes only what that request returned.

When DNS differs from the desired server, define `host`, `port` and `target_ip` and use a URL containing that hostname:

~~~bash
curl --silent --show-error --connect-timeout 5 --max-time 30 --resolve "$host:$port:$target_ip" --dump-header "$headers" --output "$body" "https://$host:$port/"
~~~

`--resolve` overrides the connection address while preserving URL hostname, HTTP Host, SNI and certificate-name checking. It is more complete than setting Host against an HTTPS IP URL. Check inherited proxy settings: a proxy can change where resolution/connections happen. Use the configured CA or an explicit trusted `--cacert` bundle rather than treating `-k` as a naming repair.

For an intentionally literal path test, `--path-as-is` preserves dot segments that curl otherwise normalizes; `--globoff` separately disables URL glob expansion. Neither prevents normalization by a proxy or server. Save the requested path and observed response together.

For an **illustrative local fixture**, a URL ending `/docs/../probe.txt` normally sends `/probe.txt`; adding `--path-as-is` sends `/docs/../probe.txt`. A changed response can therefore reflect a changed request target, not a changed server. Use the capture command above with the needed path flag and collect status, headers and body from that same GET. Discarding the first body with `-o /dev/null` and fetching again pairs the first status with a potentially different response.

A 200 body can be a login page, fallback page or application error. Compare the expected content and a known control before claiming file disclosure. A nonzero curl exit can leave both a status and a partial body; keep it as incomplete evidence. If transmission remains uncertain, a private verbose/trace capture can show the outgoing target, but also records authentication headers and content.

Inspect Location before adding `--location`; redirects can change hostname, method or authentication context. Do not forward credentials to new hosts automatically. A `500` after a mutating request does not prove rollback, so inspect state before retrying. Prefer structured status/body evidence over piping everything through `grep` for a version string.

When comparing cached responses, keep method, URL, cookies and relevant request headers constant and preserve each response in fresh header/body files. An `Age: 0` response is not a universal cache-miss test, and Age is not the object's configured TTL: it estimates time since origin generation/validation, potentially across caches. Compare Date, Cache-Control, Vary, response content and available cache diagnostics; do not infer a fixed refresh interval from one observed age. A custom `X-Cache` label follows that deployment's configuration. Varnish's usual two-number `X-Varnish` form identifies the current request and cached object's transaction; on the ordinary one-number miss form it is the second number that is absent. Headers can be rewritten, so correlate with cache logs/configuration where that distinction matters. See [HTTP Age semantics](https://www.rfc-editor.org/rfc/rfc9111.html#section-5.1) and [Varnish response construction](https://github.com/varnishcache/varnish-cache/blob/6.6/bin/varnishd/cache/cache_req_fsm.c).

Consult the [curl option reference](https://curl.se/docs/manpage.html) for version-specific behavior.
