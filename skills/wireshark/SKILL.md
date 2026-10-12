---
name: wireshark
description: Review saved DNS, HTTP, SMTP or authentication traffic in Wireshark with packet-tree and conversation context. Use when queries, stream contents, broad filters or nested Kerberos fields support a misleading interpretation.
---

# Inspect saved protocol evidence

Read this entire SKILL.md before acting. Require an existing authorized capture, trusted installed analyzer and usable graphical session. For a captured HTTP request/response or transferred source file, read [HTTP stream evidence](references/http-streams.md) fully before that review. DNS, SMTP and authentication tasks below require no additional resources. Keep the original capture and selected frame/conversation identity; finish with observed protocol/field evidence and capture limits.

Define `wireshark_bin` as the installed executable and `capture` as the absolute path to the selected local pcap/pcapng. Launch saved-file review without starting live capture:

~~~bash
"$wireshark_bin" --version
"$wireshark_bin" -n -r "$capture" -Y 'kerberos || ntlmssp'
~~~

`-r` reads the capture; `-n` disables name resolution. `-Y` is a display filter, distinct from the capture-filter syntax of `-f`. The filter hides other packets, rather than proving the capture contains only authentication. Inspect total/displayed counts and file/dissection diagnostics; clear or narrow the display filter to review surrounding requests/replies. No match can reflect missing packets, disabled dissectors, encapsulation or an analyzer-version issue.

Select a frame and expand its protocol tree. Retain frame number, capture time, source/destination, transport ports, conversation and the field's full parent hierarchy. **Illustrative:** neighboring SMB Session Setup/NTLMSSP and TCP port 88 Kerberos AS-REQ packets are separate exchanges; an AS-REQ is not NTLM authentication transmitted inside SMB merely because both appear under one filter. A packet's client principal is a capture-time claim, not proof of a completed login or present credentials.

For saved DNS traffic, replace the example display filter with `dns`, then select the actual query name/type and its matching response. `dns.qry.name`, `dns.qry.type`, `dns.flags.response` and response-code/answer fields distinguish A/AAAA questions, replies and returned addresses. Retain the transaction and endpoints; one visible DNS question proves a request for that name, not successful resolution, TCP/TLS connection or the originating app. Correlate replies and application timing separately. A screenshot clipped before answer fields leaves resolution unresolved. No DNS matches can also reflect caching, encrypted DNS or capture scope. See [DNS fields](https://www.wireshark.org/docs/dfref/d/dns.html).

For saved SMTP/TCP evidence, use `tcp.port == 25` as a display filter and select the matching TCP conversation, flags, acknowledgements and reply sequence. A port alone is not proof of protocol, and packet row color is a configurable rule rather than proof of a dropped connection. Follow the stream with capture/truncation context: successful EHLO, attempted STARTTLS, envelope acceptance and final DATA/queue receipt are separate stages. An observed 502 to STARTTLS does not establish encryption; a 550 unknown recipient rejects that recipient even if MAIL FROM received 250. Correlate a successful queue receipt with the server delivery evidence before claiming mailbox delivery. Keep message bodies/tokens private. See [SMTP fields](https://www.wireshark.org/docs/dfref/s/smtp.html) and [TCP fields](https://www.wireshark.org/docs/dfref/t/tcp.html).

For saved LDAP traffic, use the `ldap` display filter and correlate each request/reply by conversation and LDAP message ID. Inspect BindRequest authentication choice, BindResponse result, then the separate SearchRequest base/scope/filter and SearchResultDone. Bind success does not imply a later search succeeded. `noSuchObject` (32) concerns a requested directory object, distinct from zero returned entries and `invalidCredentials` (49). Retain matched DN and diagnostic text when present; a wrong search base can explain this result without proving a broken client implementation. A requested .NET authentication enum is not wire evidence of the actual provider method. Redact simple-bind password fields in excerpts. See [LDAP result semantics](https://www.rfc-editor.org/rfc/rfc4511.html).

For Kerberos, distinguish AS-REQ, AS-REP and KRB-ERROR. Within AS-REQ, PA-DATA type 2 is PA-ENC-TIMESTAMP: inspect that encrypted value's own encryption type separately from the request body's supported-encryption list. An initial request may use another pre-authentication method or omit the timestamp before a KDC response. Its ciphertext is not a plaintext password, NT hash or generic timestamp hash. Retain principal/realm association and relevant exchange context without converting or replaying secrets.

Check truncated frames, missing TCP segments and capture start/end before asserting completeness. Exported text/screenshots can omit fields or truncate bytes; preserve the original private capture and frame references. A GUI launch, valid display filter or selected decrypted field alone does not prove an application's authentication success. File analysis needs ordinary file access; do not elevate to root or start live capture to work around a GUI/session problem.

Use the [Wireshark CLI manual](https://www.wireshark.org/docs/man-pages/wireshark.html), [display-filter guide](https://www.wireshark.org/docs/wsug_html_chunked/ChWorkBuildDisplayFilterSection.html), [Kerberos fields](https://www.wireshark.org/docs/dfref/k/kerberos.html) and [Kerberos exchange definitions](https://www.rfc-editor.org/rfc/rfc4120.html) to resolve version/field questions.
