# Record the HTTP protocol actually used

Use for a selected read-only request when a product banner or requested protocol obscures the transport result. Read the curl entrypoint and this entire reference. Establish the exact authorized URL, fresh private header/body files and installed curl's protocol features before choosing a version option.

~~~bash
umask 077
curl --silent --show-error --connect-timeout 5 --max-time 30 --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\nhttp_version=%{http_version}\npeer=%{remote_ip}\n' "$url"
status=$?
~~~

Keep the exit status with the same request's headers, body and write-out values. A `Server: Microsoft-HTTPAPI/2.0` header identifies advertised software; its `2.0` is not evidence of HTTP/2. `%{http_version}` reports the version effectively used; curl's labels include `1` for HTTP/1.0 and `2` for HTTP/2. Preserve the emitted label rather than assuming every version has a decimal suffix. An HTTP/1 response has a textual status line; HTTP/2 does not send an HTTP/1-style status line on the wire even if curl formats one in saved headers.

If the selected diagnostic requires `--http2`, first confirm HTTP2 in `curl --version` and support in local help, then add that option to the capture command. For HTTPS it negotiates via TLS ALPN; a supported curl normally attempts this by default. For cleartext HTTP it requests an HTTP/1.1 Upgrade. A server can retain HTTP/1.1: a completed request or adding the flag does not establish HTTP/2. Inspect the recorded version. Unsupported builds fail locally; that failure says nothing about the server. `--http2-prior-knowledge` changes the exchange and is not a repair for an unverified banner.

Retain URL, selected option, curl version/features, exit status and observed protocol. Report an incomplete transfer or unavailable feature explicitly. A protocol result does not establish application authorization or successful behavior; assess status and body separately. See the [curl option and write-out reference](https://curl.se/docs/manpage.html).
