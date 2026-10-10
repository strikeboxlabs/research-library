# LDAP-backed form encoding and a bounded response oracle

Use a trusted Python 3 environment with Requests already installed for the authorized HTTP form. Establish the captured route, field names, session/CSRF requirements and the backend filter context first. This is HTTP transport to an application, not a direct LDAP bind. A backend identity credential is not necessarily a web-user password.

## Keep transport encoding separate from LDAP syntax

Requests `data={...}` form-encodes values. If the observed application requires one further URL-decoding layer, apply `urllib.parse.quote(value, safe="")` once before form encoding; the outer serializer then encodes percent signs. Do not keep adding passes until a response changes. Preserve the actual wire body and known literal controls to identify which layer changed.

This **illustrative**, network-free preparation contrasts the bytes for a selected observed filter fragment. Define `url` as the scoped endpoint and use its actual field names when adapting:

~~~python
from urllib.parse import quote
import requests

fragment = "*)(uid=demo*"
once = requests.Request("POST", url, data={"inputUsername": fragment,
                                            "inputOTP": "invalid-control"}).prepare()
twice = requests.Request("POST", url, data={"inputUsername": quote(fragment, safe=""),
                                             "inputOTP": "invalid-control"}).prepare()
print(once.body)
print(twice.body)
~~~

The outer body's first form contains `%2A`; the pre-encoded form contains `%252A`. One ordinary form decode produces `*` in the former and the literal text `%2A` in the latter. Transport percent escapes are not LDAP filter escapes: literal assertion values use RFC 4515 escaping such as `\2a` for an asterisk. Presence `(attr=*)`, substring `(attr=prefix*)` and equality `(attr=value)` ask different questions. Match the complete enclosing filter; a fragment from another application can simply be malformed.

For an actual selected request, create `session = requests.Session()` with the required state. Select the reviewed unencoded or pre-encoded field values, including actual OTP/CSRF fields, as `chosen_fields`; build `prepared = session.prepare_request(requests.Request("POST", url, data=chosen_fields))`, then use `session.send(prepared, timeout=(5, 10), allow_redirects=False)`. Preparing through the session applies its cookies and headers; sending a bare `Request.prepare()` result does not attach that state. If the task relies on environment proxy/CA settings, merge the intended settings explicitly or use the ordinary session request API. Preserve status/content-type/body and reject redirects, rate-limit pages or unexpected formats as unresolved. Requests timeouts bound inactivity, not the entire download; the worker still needs a request/output/time budget. `response.text` is text in Python 3; searching a str marker in `response.content` bytes is not a faithful port of the Python 2 script.

## Distinguish the oracle from authentication

Calibrate with a known matching entry and a known nonmatch while holding an intentionally invalid OTP, route and session constant. For an **illustrative** application, `Cannot login` may mean an entry reached OTP checking and `not found` may mean no selected entry. It establishes a differential, not successful login or a universally valid query. Empty replies, parsing failures, both markers, block pages, redirects or changed controls must remain unknown rather than false. A one-second delay is not proof a ban policy is avoided.

Select one known entry before enumerating another attribute. Test presence, then a justified alphabet and prefix; a multi-valued attribute or several matching entries can yield multiple true branches. uid may be case-insensitive, and pager is a telephone-number attribute, not a universal numeric-only secret field. A false result can reflect filter grammar, permissions or application logic rather than a missing schema attribute. Retain request/response associations privately; don't print recovered token material as routine progress.

For a supported bounded prefix task, adapt these callbacks to the verified oracle: `prefix_matches(value)` tests the intended substring and `exact_matches(value)` independently tests equality for the same selected entry/attribute. Each must return bool only when the controls support that interpretation. This routine avoids the source script's no-match infinite loop and first-match ambiguity:

~~~python
def recover_prefix(prefix_matches, exact_matches, alphabet, max_chars, budget):
    used = 0

    def ask(test, value):
        nonlocal used
        used += 1
        if used > budget:
            raise RuntimeError("Request budget exhausted: incomplete")
        answer = test(value)
        if type(answer) is not bool:
            raise RuntimeError("Unknown response: recheck controls")
        return answer

    prefix = ""
    for _ in range(max_chars):
        if ask(exact_matches, prefix):
            return prefix
        matches = [ch for ch in alphabet if ask(prefix_matches, prefix + ch)]
        if len(matches) != 1:
            raise RuntimeError("No unique next character: incomplete or ambiguous")
        prefix += matches[0]
    if ask(exact_matches, prefix):
        return prefix
    raise RuntimeError("Length limit reached without exact-value evidence")
~~~

Deduplicate the alphabet and use the authorized maximum length/request count, adding pacing and periodic control checks in the transport callback. Stop on changed controls, time/output limits or uncertain responses. If equality is not available, report a recovered prefix or a separately validated fixed-format candidate; do not replace `exact_matches` with unconditional success. An 81-character ceiling from a token format is not proof that every character was recovered correctly. Validate the selected format using its intended parser without authenticating automatically.

Authentication, authorization and command execution are separate subsequent tests. A username/OTP success does not prove group-based command permission. Historical embedded-NUL truncation is a particular application/library boundary, not LDAP semantics: NUL is escaped as `\00` in an assertion value. If a task explicitly calls for reproducing an observed truncation condition, use the exact documented filter context and wire bytes in a controlled instance, compare an owned harmless action and capture actual effective identity/result. Without the enclosing filter and matching binding/version, keep that condition unresolved rather than claiming the historical bypass works everywhere. Never run a copied source loop or change to a larger enumeration automatically after a failure.

References: [Requests form construction](https://requests.readthedocs.io/en/latest/user/quickstart/#more-complicated-post-requests), [session preparation](https://requests.readthedocs.io/en/latest/user/advanced/#prepared-requests), [urllib encoding](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.quote), [LDAP filters](https://www.rfc-editor.org/rfc/rfc4515), [inetOrgPerson attributes](https://www.rfc-editor.org/rfc/rfc2798).
