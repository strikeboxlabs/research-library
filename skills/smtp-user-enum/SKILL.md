---
name: smtp-user-enum
description: Compare SMTP recipient responses using smtp-user-enum without treating its positive labels as verified mailboxes. Use for scoped RCPT checks, sender-policy failures and ambiguous enumeration results.
---

# Compare the protocol responses

This skill targets pentestmonkey's Perl `smtp-user-enum`. Confirm local help and implementation before using a similarly named program. Choose the SMTP method that the server actually permits; disabled VRFY is not evidence that a user is absent.

Define `server` and `port` for the authorized SMTP endpoint, `sender` as a permitted envelope sender, `candidate` as one address under investigation, and `control` as a deliberately nonexistent address in the same domain. Use bare addresses in those variables; the command supplies literal angle brackets required by this implementation:

~~~bash
smtp-user-enum -M RCPT -m 1 -t "$server" -p "$port" -f "<$sender>" -u "<$candidate>"
smtp-user-enum -M RCPT -m 1 -t "$server" -p "$port" -f "<$sender>" -u "<$control>"
~~~

This performs two targeted protocol probes, not message delivery. `-m 1` bounds concurrency; it does not set a request rate or prove absence of server throttling. Keep the sender, domain and connection conditions comparable. Do not turn a single uncertain result into a large username-list run.

The reviewed implementation labels broad `2xx` responses positively and `5xx` responses negatively. These are tool classifications, not established account facts. `252` explicitly leaves verification unresolved; `250` at RCPT may reflect catch-all routing, deferred recipient validation or an accepted alias. A `550` can express recipient rejection or policy restrictions. If candidate and control both succeed, the method has not distinguished them.

Inspect the SMTP dialogue when labels are ambiguous. Rejection at HELO or MAIL FROM means the intended recipient test may never have happened. A temporary `4xx`, timeout or disconnect is inconclusive. For a server requiring STARTTLS/authentication that this tool cannot negotiate appropriately, use a client with those capabilities; do not interpret transport failure as a missing mailbox.

Report the method, exact response stage/code, candidate/control difference and limitations. Neither recipient acceptance nor a username-looking string establishes an operating-system login or permission to deliver a message.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Attended p. 4. Sources: [implementation](https://github.com/pentestmonkey/smtp-user-enum/blob/master/smtp-user-enum.pl), [SMTP response meanings](https://www.rfc-editor.org/rfc/rfc5321.html#section-4.2).
