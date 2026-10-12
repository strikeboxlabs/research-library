---
name: curl
description: Capture HTTP evidence, request selected byte ranges and test API or application boundaries with curl. Use when hostname/TLS routing, encoding, authentication, partial results, redirects or config-driven transfers obscure an operational result.
---

# curl HTTP evidence

Read this entire SKILL.md before acting; complete current context need not be re-read. Preserve the intended URL/route, capture status and body from the same request, and distinguish transport completion from application success. Read the applicable reference fully before its procedure; leave unrelated branches unloaded.

- Selected byte-range retrieval from an approved ordinary HTTP artifact: [range responses](references/http-ranges.md).
- Express download routes with encoded relative paths and selected source-file disclosure: [download/file-read boundaries](references/express-file-read.md).
- URL-checking forms whose value reaches a curl command line, multiple URLs or protocol filters: [URL-checker boundaries](references/url-checker.md).
- Backdrop packaging-version files and query-routed CMS paths: [Backdrop evidence](references/backdrop-evidence.md).
- Joomla manifest/version evidence and CVE-2023-23752 configuration access: [Joomla webservices](references/joomla-webservices.md).
- Grafana CVE-2021-43798 applicability, literal plugin paths and selected SQLite acquisition: [Grafana file reads](references/grafana-file-read.md).
- Company-domain ticket reply addresses used for registration/verification: [helpdesk email trust](references/ticket-email-trust.md).
- Controlled contact-mail routing and browser-rendered HTML: [mail application tests](references/mail-routing-and-html.md).
- Webhook callbacks, outbound method injection, alias/file transformations or mass-assigned account fields: [controlled application tests](references/webhook-and-file-tests.md), using the API/session references as applicable.
- A server-side TCP testing route, including read-only Memcached protocol operations: [HTTP socket bridge](references/tcp-socket-bridge.md).
- Neo4j/Cypher authentication queries or shell-running custom procedures: [Cypher and process boundaries](references/cypher-and-procedures.md).
- Stored post/title values evaluated only by a later feed or alternate renderer: [stored template boundaries](references/stored-template-tests.md).
- XML uploads with reflected external-entity file content or a newly recovered handler: [XML processing boundaries](references/xml-upload.md).
- InfluxDB v1 HTTP queries, measurement records, JWT authentication and partial results: [InfluxDB v1 queries](references/influxdb-v1.md).
- Read-only metadata for a known Elasticsearch index: [Elasticsearch index evidence](references/elasticsearch-index.md).
- Kubernetes self-permission review through an explicitly selected API: [Kubernetes permission evidence](references/kubernetes-permissions.md).
- A recovered JSON handler explicitly passing a field to a shell: [shell-backed JSON requests](references/shell-backed-json.md).
- JSON/form APIs, JSON-RPC or MCP trace interpretation, API catalogues, multipart uploads, file PUTs, token handling or acquired OAuth code/token traces: [API request construction](references/api-requests.md).
- An HTTP Negotiate service using the selected existing Kerberos cache: [Negotiate authentication](references/negotiate.md).
- Rails report downloads, hidden path fields, same-origin session riding or leading-pipe file/process inputs: [Rails report boundaries](references/rails-reports.md).
- Cookie-bound CSRF requests or a browser-only failure: [session and preflight diagnosis](references/session-and-preflight.md).
- GraphQL schema, variables and operation errors: [GraphQL requests](references/graphql.md).
- Spring Boot management discovery and mapping interpretation: [Actuator responses](references/spring-actuator.md).
- Proxy routing, CONNECT and forwarded-header interpretation: [proxy requests](references/proxy-requests.md).
- Selected read-only Squid administrator menu and FQDN-cache reports: [Squid manager reports](references/squid-manager-reports.md).
- Scheduled `-K` transfers, writable URL/output configs or inherited curlrc: [config transfer boundaries](references/config-transfers.md).
- A selected read-only HTTP request over a local Unix socket: [Unix-socket HTTP](references/unix-socket-http.md).
- HTTP/2 claims based on banners, upgrade requests or TLS negotiation: [HTTP protocol evidence](references/http-protocol.md).
- Read-only Tomcat application or virtual-host lists with a provisioned identity: [Tomcat management interfaces](references/tomcat-manager.md).

Check `curl --version` for protocols/TLS backend and inspect local help for version-dependent switches. Define `url` as the exact scoped URL and `headers`/`body` as fresh private files:

~~~bash
umask 077
curl --silent --show-error --connect-timeout 5 --max-time 30 --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\npeer=%{remote_ip}\n' "$url"
~~~

Check curl's exit status immediately. Without `--fail`/`--fail-with-body`, a completed `404` or `500` response can still return zero. Keeping the body is useful for diagnosis; `--fail-with-body` gives an HTTP-error exit while retaining it on supporting versions. Transport failure with a partial body is not a complete response.

Keep the port inside the same URL: `"http://127.0.0.1:$port/"` with the selected decimal `port`. A space before the port supplies another URL argument. A response followed by a connection error can then belong to two transfers, rather than a failed connection to the requested service. Default multi-transfer exit status follows the last transfer; inspect each result or issue the single intended URL. See the conditional URL-checker reference for backend argument boundaries.

A name mentioned inside `Access-Control-Expose-Headers` or `Access-Control-Allow-Headers` is CORS policy data, not evidence that a response contains that named header. Likewise, allowed methods do not prove those operations are accepted or authorized. Check actual header fields, status and body before fingerprinting a service or inferring object versioning. A generic JSON health response establishes only what that request returned.

`--head` (`-I`) sends HEAD for HTTP; it does not capture a GET body, and a server can treat those methods differently. Record which method produced a header. `Server` and `X-Powered-By` are advertised strings that can be configured or rewritten; a development-version label is a lead about a build, not proof that it contains a particular historical commit or backdoor. Use independently obtained package/build provenance when determining applicability.

A version file beneath a theme or plugin directory describes that component unless independently associated with the application core. Capture its exact GET path and adjacent metadata before interpreting the value; for example, a WonderCMS Bike theme version does not establish the installed WonderCMS core version. Match the affected component and build before associating a vulnerability with the response.

For an authorized known Consul agent, set `url` to its `/v1/agent/services` endpoint and use the GET capture above with its established authentication/TLS inputs. The returned mapping describes services registered on that agent, not the complete cluster catalog or their current health. Retain any `X-Consul-Results-Filtered-By-ACLs` header; an empty or filtered mapping does not establish global absence. Read access does not establish registration permission. See the [agent service API](https://developer.hashicorp.com/consul/api-docs/agent/service).

When DNS differs from the desired server, define `host`, `port` and `target_ip` and use a URL containing that hostname:

~~~bash
curl --silent --show-error --connect-timeout 5 --max-time 30 --resolve "$host:$port:$target_ip" --dump-header "$headers" --output "$body" "https://$host:$port/"
~~~

`--resolve` overrides the connection address while preserving URL hostname, HTTP Host, SNI and certificate-name checking. It is more complete than setting Host against an HTTPS IP URL. Check inherited proxy settings: a proxy can change where resolution/connections happen. Use the configured CA or an explicit trusted `--cacert` bundle rather than treating `-k` as a naming repair.

For an established HTTPS service requiring a provisioned client identity, define `client_cert` and `client_key` as its approved certificate and private-key files. On a compatible Linux TLS backend, add `--cert "$client_cert" --key "$client_key"` to the same bounded GET capture, keeping server verification and expected hostname. `--cacert` supplies server trust; it does not supply a client identity. `-k` disables peer verification and does not satisfy client-certificate authentication. A completed TLS exchange can still receive an HTTP 403 from route/application policy; correlate the expected route and server verification result before attributing the denial. Client-certificate acceptance and an application's Basic/cookie login are separate checks.

For an intentionally literal path test, `--path-as-is` preserves dot segments that curl otherwise normalizes; `--globoff` separately disables URL glob expansion. Neither prevents normalization by a proxy or server. Save the requested path and observed response together.

For an **illustrative local fixture**, a URL ending `/docs/../probe.txt` normally sends `/probe.txt`; adding `--path-as-is` sends `/docs/../probe.txt`. A changed response can therefore reflect a changed request target, not a changed server. Use the capture command above with the needed path flag and collect status, headers and body from that same GET. Discarding the first body with `-o /dev/null` and fetching again pairs the first status with a potentially different response.

A 200 body can be a login page, fallback page or application error. Compare the expected content and a known control before claiming file disclosure. A nonzero curl exit can leave both a status and a partial body; keep it as incomplete evidence. If transmission remains uncertain, a private verbose/trace capture can show the outgoing target, but also records authentication headers and content.

Inspect Location before adding `--location`; redirects can change hostname, method or authentication context. Do not forward credentials to new hosts automatically. A `500` after a mutating request does not prove rollback, so inspect state before retrying. Prefer structured status/body evidence over piping everything through `grep` for a version string.

When comparing cached responses, keep method, URL, cookies and relevant request headers constant and preserve each response in fresh header/body files. An `Age: 0` response is not a universal cache-miss test, and Age is not the object's configured TTL: it estimates time since origin generation/validation, potentially across caches. Compare Date, Cache-Control, Vary, response content and available cache diagnostics; do not infer a fixed refresh interval from one observed age. A custom `X-Cache` label follows that deployment's configuration. Varnish's usual two-number `X-Varnish` form identifies the current request and cached object's transaction; on the ordinary one-number miss form it is the second number that is absent. Headers can be rewritten, so correlate with cache logs/configuration where that distinction matters. See [HTTP Age semantics](https://www.rfc-editor.org/rfc/rfc9111.html#section-5.1) and [Varnish response construction](https://github.com/varnishcache/varnish-cache/blob/6.6/bin/varnishd/cache/cache_req_fsm.c).

Consult the [curl option reference](https://curl.se/docs/manpage.html) for version-specific behavior.
