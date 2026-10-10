# A URL-checking form can become several backend arguments

Require the scoped application route, its observed form/session contract and an owned marker receiver or selected authorized server-side file. Curl below is the worker's HTTP client; the application's backend curl is a different process/build/identity. A captured curl-shaped User-Agent is a lead that can be customized, not proof of the complete backend invocation.

## Trace decoding, validation and the backend transfer

An application can accept a string beginning http:// or https://, then pass it into a command string where whitespace makes several arguments. Curl accepts multiple URL arguments; an HTTP-looking first value does not constrain a later file:// transfer. This is argument/protocol selection, not necessarily shell-metacharacter execution. In contrast, a whole space-containing value passed as one argv element normally remains one malformed URL. Establish that boundary from acquired source or controlled results instead of assuming every URL filter behaves this way.

For an observed POST field named url, define `checker_url` as its exact scoped route, `server_file_uri` as the complete encoded file:/// URI of the selected authorized **backend-side** marker/file, and `headers`/`body` as fresh private captures:

~~~bash
value="http:// $server_file_uri"
curl --silent --show-error --connect-timeout 5 --max-time 30 \
  --data-urlencode "url=$value" --dump-header "$headers" --output "$body" \
  --write-out 'status=%{http_code}\n' "$checker_url"
~~~

This encodes one form field containing a literal space; server form decoding and subsequent command construction decide what backend arguments result. Literal + in an application/x-www-form-urlencoded body decodes as space, while %2B represents a plus; do not pre-encode and then encode again. Use the actual cookies/CSRF fields when required. Capture the known control, exact submitted bytes and returned marker/content from the same attempt. A UI "down" label, HTTP200 or reflected submitted filename is insufficient evidence of a read.

FILE reads with the backend process's filesystem authority and namespace. A conventional document-root pathname is a hypothesis, not Apache configuration proof. If source is acquired, distinguish HTML presentation escaping from PHP source bytes and inspect it without executing it. An actual identity/route or marker validates that instance's result, not every file's readability.

## Separate transfer results and protocol policy

Without --fail-early, a multi-transfer curl invocation can encounter an initial malformed URL and finish with a later successful transfer; the overall exit can describe the last transfer. Bodies can concatenate on stdout. Record per-transfer URL/status/stderr when interpreting a wrapper. --fail-early stops on an earlier transfer error; it does not validate an application's untrusted arguments. HTTP status alone also does not describe a FILE transfer.

For an owned local marker on the worker, define `marker_uri` as that file's encoded absolute file:/// URI and `output` as a fresh destination. A direct diagnostic isolates FILE support from the web application:

~~~bash
curl -q --proto '=file' --output "$output" "$marker_uri"
~~~

This reads locally on the **worker**, not on the remote server. For a reviewed HTTP-only backend design, --proto '=http,https' constrains actual transfers and --proto-redir '=http,https' separately constrains followed redirects. Safe argv boundaries, one parsed intended URL, destination policy and control of subsequent options/configuration still matter; adding a prefix test or one shell quote is not that complete policy. Gopher/other schemes require actual build support and a separate selected protocol task, not an automatic next probe.

See [multiple curl URLs](https://curl.se/docs/httpscripting.html#multiple), [protocols/status/options](https://curl.se/docs/manpage.html) and [curl URL syntax](https://curl.se/docs/url-syntax.html). A missing feature, protocol denial, parser error, transport timeout and successful selected file content are different outcomes.
