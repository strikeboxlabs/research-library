# Compare Origin policy on one endpoint

Use this when the question is which supplied origins change a known endpoint's CORS response. An `Origin` value describes the caller's origin; it does not choose the destination virtual host. Keep the URL, HTTP Host/TLS SNI, method and session constant. A match is a policy observation on the responding endpoint, not proof the origin hostname exists or is reachable.

Define `url` as the scoped endpoint and `origins` as a small local file of complete origins (`scheme://host[:port]`, no path). Include a known allowed origin when available and an unrelated negative control. First inspect unfiltered results:

~~~bash
wfuzz -w "$origins" -t 1 -s 0.5 -H 'Origin: FUZZ' "$url"
~~~

After retaining controls, the advanced filter can select responses containing the allow-origin header:

~~~bash
wfuzz -w "$origins" -t 1 -s 0.5 -H 'Origin: FUZZ' \
  --filter "r.headers.response~'Access-Control-Allow-Origin'" "$url"
~~~

Check installed filter support/casing against a known positive. A header-name match does not check its value. Confirm candidates individually with the same request state. Define `origin` as one candidate and `headers`/`body` as fresh paths:

~~~bash
curl --silent --show-error --connect-timeout 5 --max-time 20 \
  --header "Origin: $origin" --dump-header "$headers" --output "$body" "$url"
~~~

Check curl status and actual HTTP status, ACAO value, `Access-Control-Allow-Credentials` and `Vary: Origin`. Use GET here; `-I` changes the request to HEAD. Do not follow redirects automatically while comparing policy. Keep the existing authenticated state only if required and authorized; a failed/expired session is a different baseline.

CORS policy is directional: A permitting caller B to read its response says nothing about B permitting caller A. Credentialed browser reads need the applicable exact origin rather than `*`, credentials permission and the browser's actual cookie policy. `withCredentials` does not create a login or bypass cookie restrictions. Non-simple requests may need a successful preflight for their method/headers. Curl displays responses without enforcing browser CORS, and a denied browser read does not establish that the request was never sent or had no effect. Stop at a header-policy finding unless the intended browser context is actually verified.

See [Wfuzz result fields and filters](https://wfuzz.readthedocs.io/en/latest/user/advanced.html#filtering-results), [browser CORS rules](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS) and [curl request options](https://curl.se/docs/manpage.html).
