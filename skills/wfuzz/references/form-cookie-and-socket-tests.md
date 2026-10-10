# Form, cookie and service-side socket comparisons

Use when the same HTTP application exposes several independent authentication checks or a TCP testing endpoint. Start with actual method/field/cookie evidence, a small selected payload set and known controls. Preserve complete coverage and individual responses that change the next decision; keep raw credential material private.

## Match the authentication boundary

For `login_url`, `selected_user` and `candidates`, this form example applies only when observed fields are `username`, `password`, `submit`, with no changing CSRF token. The user value and candidate file must already use the required form encoding; `&`, `+` and `%` are data/encoding boundaries, not harmless literal password characters:

~~~bash
wfuzz -w "$candidates" -t 1 -s 0.5 -d "username=$selected_user&password=FUZZ&submit=Login" "$login_url"
~~~

Begin unfiltered; learn stable line/word/character counts from an invalid control. After observing them, `--hl N`, `--hw N` or `--hh N` can hide those counts. Do not adopt a walkthrough's values. A 302 redirect is an authentication candidate, while a 500 may be a parser/backend error; neither alone is success. Re-fetch the selected candidate with the same form/session, inspect Location/cookies and confirm a protected operation with a negative control. Expired/rotating CSRF state requires a request flow that maintains it, not a larger candidate list.

An independent service may return HTTP 200 for both missing and incorrect cookies. If the observed gate specifically requires `password`, define its `gate_url` separately:

~~~bash
wfuzz -w "$candidates" -t 1 -s 0.5 -H 'Cookie: password=FUZZ' "$gate_url"
~~~

Retain other required cookies when applicable, without duplicating/conflicting Cookie headers. A different word count or disappearance of an access-denied message is a lead; confirm actual protected behavior. A login cookie on one service is not evidence that another service's gate has passed.

## Vary one socket parameter from the application's vantage

Only for a verified endpoint exposing a server-side TCP connection, define `socket_url` as its exact route, `cookie_value` as the selected private gate value, and `ports` as a small selected list of decimal ports. Here the observed query fields are `port` and `cmd`, and the destination host is fixed by that application:

~~~bash
wfuzz -w "$ports" -t 1 -s 0.5 -H "Cookie: password=$cookie_value" "${socket_url}?port=FUZZ&cmd=test"
~~~

This probes **from the web service's process/network context**. It is not the client's external scan, and its HTTP status is not a raw TCP port state. Compare refusal, timeout, application filter errors and protocol-shaped replies. HTTP 500 does not establish an open port; an empty accepted command can be silent. Confirm a promising port with a small command appropriate to the independently supported protocol.

If the task concerns a command filter, use a finite, explicitly encoded character/control set and vary only `cmd` at one known port. Inspect the actual emitted HTTP request and decoded server input before interpreting `%2F`, `+` or spaces. A filter may apply before or after URL decoding. Accepting spaces while rejecting punctuation still permits protocols whose read commands need only letters, digits and spaces, such as Memcached's `stats slabs` and `get key`. It does not prove shell syntax is available. Tests of one list are not proof that every useful character is rejected.

Keep a known backend response visible when adding count filters; HTTP wrappers can add dynamic diagnostics and conceal a valid backend result behind the same count. Stop or reduce requests on throttling/unstable controls; missing/failed requests are not completed negative coverage. Finish with the confirmed authentication distinction or socket/protocol response and the tested set, not just a filtered table.

See [Wfuzz request, cookie and pacing options](https://wfuzz.readthedocs.io/en/latest/user/basicusage.html) and [filter definitions](https://github.com/xmendez/wfuzz/blob/master/src/wfuzz/ui/console/clparser.py).
