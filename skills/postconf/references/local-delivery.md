# Diagnose the selected local-delivery path

Use the selected instance and one authorized message's private SMTP/server evidence. Keep the envelope recipient distinct from the message's To header. DNS, a TCP listener, the queue and mailbox delivery are separate observations.

| Observed stage | Next decision |
|---|---|
| EHLO succeeds, STARTTLS receives 502 | TLS negotiation did not complete. Check advertised capabilities and service TLS configuration. |
| MAIL FROM receives 250, RCPT TO receives 550 unknown local recipient | Sender stage passed; this recipient was rejected. Check destination class and its recipient maps. This is not a queue receipt. |
| End of DATA receives a successful queue receipt | Correlate its ID with delivery logs and the intended mailbox/transport; acceptance alone does not prove final delivery. |

`myhostname` supplies server identity, not the whole destination-domain configuration. `mydestination` selects local domains; virtual/relay domains have their own maps/transports. `mynetworks` defines trusted relay clients, not mailbox existence. A whole private network can grant far more relay trust than the intended sender; retain exact approved scope.

For a local domain, inspect local_recipient_maps, aliases, transport and account lookup. An OS account can participate in the configured map, but creating it does not prove routing. Check the selected delivery agent's format, spool path, ownership/mode and locking contract before provisioning storage; an empty file plus chown is not a universal mailbox recipe.

Retain the relevant reply/log sequence, time and endpoints privately. Redact bodies and authentication/reset material. Quoted-printable bodies require MIME decoding: encoded equals signs and soft line breaks are not literal URL characters. Decode locally using the actual content-transfer encoding rather than uploading mail to a public converter.

See [Postfix parameters](https://manpages.debian.org/bookworm/postfix/postconf.5.en.html) and [SMTP sequencing](https://www.rfc-editor.org/rfc/rfc5321.html).
