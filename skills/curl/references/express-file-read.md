# Selected file-read behavior in an Express download route

Use this when an authorized download handler accepts an encoded path and responses suggest that the route can read a selected server file. Require the observed route, existing session if needed and exact selected file. Express or Nginx fingerprinting alone does not establish a vulnerable handler. Keep the known successful ordinary download as a control and capture each status/header/body together.

Define `origin` as the scoped origin, `route` as the exact observed download prefix and `encoded_relative` as one reviewed relative-path string. An **illustrative** ../package.json encoded as ..%2fpackage.json is a selected application-file probe, not a universal path to /etc/passwd. `cookie_file` is a private curl cookie jar for the existing authorized session; `headers` and `body` are fresh private output files:

~~~bash
umask 077
curl --silent --show-error --connect-timeout 5 --max-time 15 --path-as-is --globoff --cookie "$cookie_file" --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\n' "$origin$route$encoded_relative"
~~~

Do not add --location while classifying the response. A redirect/login page, an Nginx-generated 400 and an application 404 represent different boundaries. A failed deep traversal does not prove a shallow relative read is denied; encoding and normalization can differ at the client, front proxy, router and file API. --path-as-is controls curl dot normalization, not downstream decoding or authorization. Preserve the transmitted spelling when comparing controls.

Check curl status and complete response bytes. A known uploaded PNG returning 200 establishes that download, not application-source disclosure. A coherent package manifest or JavaScript handler with expected structure supports the selected file read; fallback HTML with 200 does not. Inspect acquired code as text rather than importing it. A manifest author is an account lead, not proof of an OS account; package version ranges are not an installed lockfile.

If a selected app.js and router are accessible, connect the evidence: middleware name/keys/serialization, route input and file/query call, returned fields and service launch conditions. A disclosed signing key supports the exact signed-session task only after calibrating against a valid pair. Passing a session user object directly to a relation filter can expose predicate control even when select omits the sensitive field; do not relabel this as raw SQL injection without the corresponding SQL boundary.

Finish with the selected path, response evidence and confirmed handler behavior. Unknown working directory/base path, proxy decoding, truncated source or a changed session leaves the next path uncertain; choose a bounded discriminating probe rather than inferring arbitrary OS-file access. See [curl literal path and cookie options](https://curl.se/docs/manpage.html) and [Express cookie-session](https://expressjs.com/en/resources/middleware/cookie-session.html) for the selected implementation.
