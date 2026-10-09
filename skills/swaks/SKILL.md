---
name: swaks
description: Inspect MIME construction and diagnose a specific SMTP transaction with Swaks. Use for attachment encoding, TLS verification, recipient-stage probes and distinguishing submission from delivery.
---

# Choose the SMTP stage deliberately

Check `swaks --version` and `swaks --support` for installed TLS/authentication capabilities. Define `server` as the intended SMTP hostname, `port` as its actual service port, `sender` and `recipient` as verified single addresses, `subject` as a single-line value, `body_text` as the message text, `attachment` as an existing absolute file and `preview` as a fresh private output path.

Inspect the proposed MIME message without sending it:

~~~bash
umask 077
swaks --server "$server" --port "$port" --from "$sender" --to "$recipient" --header "Subject: $subject" --body "$body_text" --attach "@$attachment" --dump-mail > "$preview"
~~~

`@` explicitly selects file content for the attachment. Check status, headers, MIME boundaries, filename and encoding in the result. `--header 'Hello'` is not a complete header field; use `Name: value` syntax and reject embedded CR/LF in values. `--dump-mail` prints the constructed message instead of submitting it. Avoid using broad `--dump` as a shareable diagnostic: its configuration output can expose authentication secrets.

For a server requiring STARTTLS, a separately authorized recipient-stage test can stop before DATA:

~~~bash
swaks --server "$server" --port "$port" --from "$sender" --to "$recipient" --tls --tls-verify --quit-after RCPT
~~~

Use `--tls-on-connect` instead of `--tls` for implicit TLS when that is the endpoint's policy. TLS negotiation alone does not require certificate validation by default; `--tls-verify` adds CA and target-name checks. A numeric address can fail hostname verification; use the intended service identity and trusted CA configuration. Configure authentication separately when required, without putting reusable passwords in shared command logs.

An explicit `--server` avoids silently choosing a destination through recipient-domain MX lookup. To actually submit the reviewed message, use its construction arguments with the verified transport/authentication options, omitting `--dump-mail` and any early-stop option, only when delivery is requested.

Record the last successful SMTP phase and response. RCPT acceptance is not mailbox proof; DATA acceptance is not inbox delivery or attachment execution. Diagnose connection, TLS, AUTH, recipient policy and post-submission behavior separately.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Axlle p. 4. Source: [Swaks manual](https://github.com/jetmore/swaks/blob/develop/doc/base.pod).
