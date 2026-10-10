# Helpdesk email routing and domain-based signup trust

Use for an authorized helpdesk/signup assessment when a public ticket offers a company-domain reply address and a separate service treats that domain as a membership signal. A ticket-address workflow can let an external requester read mail delivered to a ticket; it does not provide a complete employee mailbox. This is the TicketTrick trust-boundary hypothesis, not a universal osTicket or Mattermost vulnerability.

Identify the actual creation/status routes, ownership check, mail routing and signup policy. The meaningful chain is:

1. Create one owned test ticket through the observed supported form and retain its actual ticket ID, access mechanism and reply address.
2. Register the owned test account on the scoped service using that address only when this signup action is authorized.
3. Read that same ticket and correlate the delivered verification message with the requested recipient and signup account.
4. Review the verification link's destination/token context, follow it once through the expected application flow and verify the new account's state.
5. Inspect the actual team/channel permissions granted to that account. Email verification, account creation, an invitation and access to an internal team are distinct results.

Use the deployment's actual forms, field names, CSRF/session requirements and browser flow. Do not invent a helpdesk API, bypass CAPTCHA or substitute another user's ticket. Curl can reproduce captured supported HTTP requests and preserve responses; it does not execute a browser's JavaScript or establish delivered mail by itself. Account/ticket creation and a verification GET can change server state even when the surrounding reads are passive.

For an already authorized owned ticket view, define `ticket_url` as the observed URL, `ticket_jar` as its private session jar when needed, and `headers`/`body` as fresh private outputs:

~~~bash
umask 077
curl --silent --show-error --connect-timeout 5 --max-time 30 \
  --cookie "$ticket_jar" --cookie-jar "$ticket_jar" \
  --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\n' "$ticket_url"
status=$?
~~~

Omit cookie options when the actual view does not use them. A ticket-number/contact-email pair or tokenized access URL is sensitive too; preserve it privately rather than treating an HTTP 200 as ownership proof. Require successful transport and the selected ticket/message, not a login/fallback page. Do not enumerate adjacent IDs.

For a verification URL recovered from that owned ticket, inspect the complete scheme/host/path and token before use. Preserve the intended hostname/TLS identity with an explicit mapping when DNS differs, as described in the entrypoint. Use a separate signup-service session jar; do not carry the helpdesk's headers/cookies to another origin. Curl can fetch an observed verification route with the same bounded response capture, but review Location before following redirects and check resulting state before retrying a consumed/expired token.

A corporate-domain address alone can be a routing alias controlled through ticket creation. Ask which identity assertion the receiving service actually made: proof of mail delivery, domain allowlist, an explicit staff invitation or an independently provisioned organization identity. The useful finding requires the observed mail route and resulting unauthorized organizational access, not merely a new public account. If registration is allowed but the internal team is closed, report that narrower boundary. If no verification mail arrives, distinguish ticket permissions, mail delivery/filtering, service policy and token lifetime rather than guessing a successful bypass.

Accessible internal messages may reveal service credentials or a password-family clue. Preserve their context/identity privately; a hint supports a bounded candidate hypothesis, while a displayed credential still needs the separately selected service/account check to establish reuse. Do not infer that every employee, application and OS account shares it.

Finish with the owned ticket/message/signup correlation and actual account/team-access result, including any broken link in the chain. Preserve browser evidence when a browser-only procedure supplies the result. Read [API construction](api-requests.md) or [session handling](session-and-preflight.md) fully if using those respective procedures. See [osTicket mail configuration](https://docs.osticket.com/en/latest/Admin/Emails/Emails.html), [Mattermost signup and verification settings](https://docs.mattermost.com/administration-guide/configure/authentication-configuration-settings) and [curl's request/cookie options](https://curl.se/docs/manpage.html).
