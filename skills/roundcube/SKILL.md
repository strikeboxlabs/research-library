---
name: roundcube
description: Enumerate and exploit Roundcube Webmail instances.
---

# Roundcube Webmail testing

Use when a Roundcube instance is identified (login page title "Roundcube Webmail", cookies named roundcube_sessid). Separate version detection, plugin enumeration and authenticated actions; verify each response instead of assuming.

## Environment (verified 2026-10-11)

- No Roundcube binary locally; all interaction is HTTP against the target.

## Version detection

The version is NOT in the unauthenticated login page. After logging in (any valid webmail credential), fetch `?_task=settings&_action=about` and read `Roundcube Webmail <version>` from the page body. CTF boxes often pin a version with known CVEs (e.g. 1.6.x line: IMAP command injection fixed in 1.6.18, markasjunk cmd_learn RCE fixed in 1.6.18, several stored-XSS/SSRF fixes in 1.6.16/17).

## Login flow (scripted)

1. GET `/?_task=login`, parse `name="_token" value="..."` (CSRF token).
2. POST `/?_task=login` with `_user`, `_pass`, `_token`, `_task=login`, `_action=login` using a cookie jar. The form field names are `_user`/`_pass`/`_token` — NOT `user`/`pass`/`csrf` (a 401 with 5 error elements usually means wrong field names).
3. A logged-in session serves pages mentioning `_task=logout`; sessions expire quickly (minutes). Re-login rather than debugging dead sessions.

## Plugin enumeration

Plugin directories ship with the source tree, so directory probing (`/plugins/<name>/` → 403/301 vs catch-all 200) proves files exist, NOT that a plugin is enabled. To test if a plugin action is registered, request `?_task=settings&_action=plugin.<name>` with a valid session: an enabled plugin renders its UI; an unknown/unregistered action returns the generic `SERVER ERROR!` page with `Error No. [524]`. Compare against a deliberately bogus plugin name to establish the error baseline.

## Reading mail without a browser

The Elastic skin loads message lists via XHR: GET `?_task=mail&_action=list&_mbox=INBOX&_remote=1&_unlock=1` with header `X-Requested-With: XMLHttpRequest` returns JSON whose `exec` field contains `add_message_row(<uid>, {...})` calls. Message UIDs are NOT sequential from 1 — use the listed uid in `?_task=mail&_mbox=INBOX&_action=show&_uid=<uid>`; a wrong uid yields "Could not load message from server". Direct IMAP (same credentials, imaps port 993) is usually simpler when the backend allows it.

## IMAP injection notes (search-based CVEs)

For the CVE-2026-35538/75002 family: `_filter` values are CRLF-stripped since 1.6.14/1.6.16 (`search.php` applies `preg_replace('/[\r\n]+/',' ',$search_str)`), but `_q` reached the IMAP socket unsanitized in 1.6.16 via `search_input()`. Verify a claimed injection with an observable effect (e.g. injected IMAP command creating a mailbox visible via a parallel direct-IMAP session), not with HTTP status codes: Roundcube 500s on malformed search responses even when injection succeeded, and plugin `prepare` calls can block ~20s on failed outbound cURL (SDI service unresolvable), which mimics time-based proofs.

## python-requests multipart gotcha

When an exploit requires special characters (quotes, `$()`, semicolons) in an uploaded FILENAME, python-requests percent-encodes `"` as `%22` inside the `Content-Disposition` header, silently breaking filename-based injection. Build the multipart body manually with a raw string and post it via `session.post(url, data=body, headers={"Content-Type": "multipart/form-data; boundary=..."})`, or use curl. Verify the transmitted bytes with a local socket listener before blaming the target.
