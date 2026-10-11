---
name: imap-enumeration
description: Enumerate mailboxes over IMAPS with Python imaplib.
---

# IMAP mailbox enumeration

Use when webmail or mail credentials are obtained and message contents, other users' mailboxes, or mail-derived intelligence (internal hostnames, further credentials) are needed. Prefer IMAP over scraping webmail UIs.

## Environment (verified 2026-10-11)

Local client: Python `imaplib` over SSL (no CLI MUA needed). No skill-specific binaries.

## Login

~~~python
import imaplib
m = imaplib.IMAP4_SSL(host, 993)
m.login(user, password)
~~~

Dovecot on port 143 typically advertises `LOGINDISABLED` — plaintext-port logins fail with "no auth mechanism"; use 993 (imaps). When probing MANY username candidates against Dovecot, each failed login can incur a multi-second server-side delay (throttling): use one fresh connection per attempt with a socket timeout (5–8 s), not a shared session. A `read timed out` on probe is NOT evidence the user exists; only `OK`/`AUTHENTICATIONFAILED` distinguish. Successful logins for other users indicate credential reuse — enumerate that user's folders and messages immediately.

## Enumeration

`m.list()` shows folders (personal namespace only; `NAMESPACE` returning `(("" "/")) NIL NIL` means no shared/other-user namespaces, so cross-user reading requires ACL grants or a master-user config, absent by default). `m.select("INBOX", readonly=True)` then `m.search(None, "ALL")` for uids. Fetch full source with `m.uid("FETCH", uid, "(BODY[])")` — headers like `X-Original-To`, `Delivered-To` and `Received` reveal the internal mail stack (e.g. Postfix on localhost) and internal hostnames. Fetch a single message's size via `(RFC822.SIZE)` before pulling large bodies.

## Delivering mail without SMTP

When no SMTP port is exposed but an account is compromised, `m.append("INBOX", "", imaplib.Time2Internaldate(time.time()), raw_email_bytes)` injects a message into the mailbox (works on Dovecot). Useful to stage HTML/phishing content that a victim user (or the same webmail account) will render. Note: fetching by sequence number vs UID differs after APPEND; re-run SEARCH before addressing new messages.

## Injection testing from IMAP

If a webmail CVE claims IMAP command injection, remember you already hold an authenticated IMAP session as that user: reproduce the injected command directly (e.g. `CREATE`, `LIST`) to separate "Roundcube passes it through" from "Dovecot accepts it" before building web-side payloads.
