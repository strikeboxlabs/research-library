# Contact-mail routing and browser HTML evidence

Use for a scoped application whose contact endpoint sends mail and accepts recipient/content fields. Recover the actual form action, field names, session/CSRF requirements and encoding first. A browser's hidden field is still client input; an observed `recipient` parameter is a lead, not proof the server accepts arbitrary destinations.

Select one controlled recipient mailbox and a unique harmless marker, define `send_url`, `recipient`, `reply_address`, `marker`, and fresh `headers`/`body`. Adapt the observed fields; these field names are **illustrative**:

~~~bash
umask 077
curl --silent --show-error --connect-timeout 5 --max-time 30 \
  --data-urlencode 'name=controlled-mail-test' --data-urlencode "email=$reply_address" \
  --data-urlencode "recipient=$recipient" --data-urlencode "message=$marker" \
  --data-urlencode 'content=text/plain' \
  --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\n' "$send_url"
~~~

Use the actual application session/CSRF mechanism where present. Record delivered mailbox/message identity and marker, not only HTTP 200. A changed recipient that is accepted establishes recipient-control behavior; calling it IDOR additionally requires the relevant unauthorized object/recipient access model. Do not silently substitute an uncontrolled recipient or bulk-enumerate messages.

For an approved browser HTML/sanitizer test, reuse this request with `content=text/html` and `--data-urlencode "message@$html_file"`, where `html_file` is the reviewed single-message test body. Replace the previous message argument, rather than sending two competing fields. This sends text; curl does not render it or execute script. Verify the actual webmail version/path and the message's browser-rendered DOM. A simple formatting marker establishes HTML rendering, not XSS.

Roundcube's CVE-2024-42009 concerns a post-sanitization transformation of a `body` element into a `div` that could reintroduce an event attribute. The relevant condition is the vulnerable rendering/transformation, not merely a message labelled HTML. In an explicitly scoped test, use a harmless event marker in the owned mailbox/browser and retain the event/DOM evidence; do not treat curl's send result or a stored string as browser execution. Consult the primary [Roundcube vulnerability analysis](https://www.sonarsource.com/blog/government-emails-at-risk-critical-cross-site-scripting-vulnerability-in-roundcube-webmail/) for the affected transformation and versions before selecting a diagnostic body.

If browser execution is actually established and reading a selected owned test message is in scope, a same-origin mail request uses the browser's session/UID and may expose that selected response. UID ranges are not a mailbox inventory; stop at the selected message. A cross-origin callback using `no-cors` has an opaque response and does not bypass response-reading policy. Match the expected marker/body and the intended callback route; network ingress, application failure and browser policy are separate evidence. A base64 wrapper is encoding, not safety or authentication; decode for review without eval.

Preserve raw body and encoding before field extraction. The webmail UI, password-reset email and token lifetime remain application-specific observations. A fresh token can expire between delivery and use; do not infer no delivery from an expired token or reproduce a walkthrough's fixed five-minute assumption. Finish with the specific routing/rendering/action result and missing browser evidence where applicable. For redirects, URL encoding and transfer status, use [curl's manual](https://curl.se/docs/manpage.html); for browser-only errors use [the session reference](session-and-preflight.md).
