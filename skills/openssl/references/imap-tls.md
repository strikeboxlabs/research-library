# Diagnose IMAP over TLS

Choose an authorized endpoint from its configuration and observed greeting. Conventional ports are IMAP STARTTLS 143, implicit-TLS IMAP 993 and implicit-TLS POP3 995; a custom port is possible. A successful TLS handshake does not identify the application protocol. IMAP greetings normally start `* OK` or `* PREAUTH`; POP3 uses `+OK`. Do not send IMAP commands to a POP3 endpoint.

Define `endpoint` as the selected `host:port`, `mail_host` as its expected certificate/SNI hostname, and `ca_bundle` as independently trusted CA certificates. For an interactive implicit-TLS session:

~~~bash
openssl s_client -connect "$endpoint" -servername "$mail_host" -verify_hostname "$mail_host" -verify_return_error -CAfile "$ca_bundle" -crlf -quiet
~~~

For an endpoint that starts in plaintext and upgrades using IMAP STARTTLS, use the same options with `-starttls imap` and the corresponding endpoint. Do not apply that switch to an implicit-TLS port. `-servername` selects SNI; `-verify_hostname` checks identity, and `-verify_return_error` stops on verification failure. Default diagnostic s_client behavior can continue despite verification errors. Resolve trust/hostname failures before supplying credentials.

Send these protocol lines interactively, waiting for the matching tagged response:

~~~text
A01 CAPABILITY
A02 LOGOUT
~~~

These are protocol commands, not Bash. Do not append shell comments. `-crlf` supplies protocol line endings; `-quiet` also ignores stdin EOF, so use LOGOUT or explicitly end a stuck process. Keep an overall session deadline in the harness. `NO`, `BAD`, `BYE`, timeout and a successful tagged `OK` imply different outcomes; a printed untagged response alone is not command completion.

## Once separately authenticated for the authorized mailbox

An `* OK` greeting is not login success. Use the service's approved authentication mechanism and current capabilities; do not infer account access from TLS success. For an already authenticated session, `LIST "" "*"` discovers mailbox names. An empty INBOX does not describe Drafts or other folders. Select the exact observed mailbox with `EXAMINE` for read-only inspection.

The following is **illustrative protocol input** after observing a mailbox called Drafts and a message UID of 42:

~~~text
A10 EXAMINE "Drafts"
A11 UID FETCH 42 (UID RFC822.SIZE BODYSTRUCTURE)
A12 UID FETCH 42 (BODY.PEEK[])
A13 LOGOUT
~~~

Wait for read-only EXAMINE completion, inspect size/structure, and fetch the full message only if it fits the task's acquisition limit. Discover actual UIDs using an appropriately scoped UID SEARCH; 42 is not a default. Keep mailbox and UIDVALIDITY with each UID; sequence numbers can change. `BODY.PEEK` avoids setting the Seen flag. Preserve the fetched literal's byte count and message bytes separately from protocol framing; terminal copy/paste is unsuitable for a reliable large/binary export. MIME attachments still require exact part decoding. A truncated literal or missing tagged completion is incomplete evidence.

See [s_client options](https://docs.openssl.org/3.5/man1/openssl-s_client/), [IMAP state and fetch rules](https://www.rfc-editor.org/rfc/rfc9051.html) and [mail TLS port conventions](https://www.rfc-editor.org/rfc/rfc8314.html).
