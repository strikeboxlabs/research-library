# Preserve a session and diagnose browser policy separately

Use the API's documented token endpoint, header name and body format. A returned CSRF token is not a login or an authorization grant. The following workflow assumes an existing authorized session (if required), a JSON `token` field and the header `X-CSRF-TOKEN`; adapt those to the observed contract. The existing `jq` parser is used to extract a field instead of splitting JSON on quotes.

Define `token_url`, a private `jar` path for this one session, and fresh private `token_headers`, `token_body` and `csrf_header` paths. For a new unauthenticated session, omit `--cookie` on the first request. For an existing session preserve its jar:

~~~bash
umask 077
curl --silent --show-error --connect-timeout 5 --max-time 30 \
  --cookie "$jar" --cookie-jar "$jar" --dump-header "$token_headers" \
  --output "$token_body" --write-out 'status=%{http_code}\n' "$token_url"
~~~

Check transport, HTTP status and the response contract before extracting. A missing or unwritable jar is not a usable saved session; verify it exists and inspect relevant cookie names/domain/path without printing secret values.

Cookie Path matching is not an unrestricted text-prefix test. An **illustrative** `Path=/docs` matches `/docs` and `/docs/page`, but not `/docstore`: beyond an exact match, the prefix must end in `/` or the next request-path character must be `/`. Check the actual stored Path and request path when a session disappears between routes. Path selects cookie delivery; it is not an application authorization boundary. See [cookie path matching](https://www.rfc-editor.org/rfc/rfc6265.html#section-5.1.4).

After a suitable token response:

~~~bash
jq -e -r '.token | select(type == "string" and length > 0) | select(test("[\r\n]") | not) | "X-CSRF-TOKEN: " + .' "$token_body" > "$csrf_header"
~~~

Require exit zero and a nonempty header file; otherwise stop. Do not reuse a stale header from another session. This constructs a secret-bearing header file, not terminal output. A JSON `success: false` does not by itself tell you whether a separate token field is usable: follow that endpoint's contract.

For the intended API operation, define the exact `url`, `method`, reviewed `request_json` and fresh `headers`/`body` files:

~~~bash
curl --silent --show-error --connect-timeout 5 --max-time 30 \
  --cookie "$jar" --cookie-jar "$jar" --header "@$csrf_header" \
  --request "$method" --header 'Content-Type: application/json' \
  --data-binary "@$request_json" --dump-header "$headers" \
  --output "$body" --write-out 'status=%{http_code}\n' "$url"
~~~

Match form versus JSON encoding before diagnosing misleading field-validation errors. An administrator-only error after CSRF validation is a separate authorization result. Inspect state after an uncertain write before retrying. Keep the jar/header private; don't automatically follow cross-host redirects with them. See [cookie handling](https://curl.se/docs/http-cookies.html) and [body/header options](https://curl.se/docs/manpage.html).

## Model an actual browser preflight

Keep cookies, localStorage and the server's authorization result separate. localStorage belongs to the page's origin and is not automatically attached as a Cookie header; an application must read and transmit it explicitly. A client flag that exposes a menu does not establish that the server permits its operation. Cookie Domain controls eligible hosts, while SameSite compares site context rather than requiring identical origins. A subdomain change can therefore be cross-origin yet same-site, subject to scheme and browser context. HttpOnly prevents script access to that cookie, not browser delivery on an eligible request. Diagnose the actual request/response and storage mechanism rather than inferring it from a developer-tools value. See [Web Storage](https://html.spec.whatwg.org/multipage/webstorage.html) and [cookie processing](https://datatracker.ietf.org/doc/html/draft-ietf-httpbis-rfc6265bis).

For a scoped policy check, define `origin` as the caller's origin (`scheme://host[:port]`, no path), `url` as the destination and `method` as the proposed method. This example proposes a JSON request with a CSRF header:

~~~bash
curl --silent --show-error --connect-timeout 5 --max-time 30 \
  --request OPTIONS --header "Origin: $origin" \
  --header "Access-Control-Request-Method: $method" \
  --header 'Access-Control-Request-Headers: content-type,x-csrf-token' \
  --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\n' "$url"
~~~

This sends no operation body or session cookie. An OPTIONS request with only Origin is not the same preflight. Check status, the permitted origin, method and requested headers. Credentialed browser access also needs `Access-Control-Allow-Credentials: true` and an exact permitted origin, not `*`; browser cookie rules still apply. JSON or `X-CSRF-TOKEN` triggers preflight even when the method is POST. Form encoding alone does not make a custom-header request simple.

Curl does not enforce CORS. Separate preflight permission, actual-request transmission, response readability and application outcome. A missing callback or failed subsequent login proves neither that a write was never sent nor that it rolled back. Confirm browser behavior with its network evidence when that is the requested conclusion. Keep the destination fixed while varying origins; an unexpected allow-origin response does not identify the underlying regex or validation implementation.

See [browser CORS rules](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS).
