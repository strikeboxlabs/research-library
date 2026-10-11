---
name: flask-unsign
description: Decode an acquired Flask client-session cookie locally without validating its signature or contacting a service. Use when encoded session data is mistaken for encrypted data or a JWT, and separate readable claims from authenticated state.
---

# Inspect a captured Flask session

Read this entire SKILL.md before acting. Use the local decoding task below with a bounded acquired cookie and the installed trusted tool. Finish with the decoded fields, diagnostics and signature-verification gap. Decoding does not authenticate the cookie or establish the application's accepted session state.

Check `flask-unsign --version` and `flask-unsign --help`. Define `cookie_file` as a private text file containing the selected cookie value, and `decoded`/`diagnostic` as fresh private output paths. Keep the cookie out of command arguments and external decoder websites:

~~~bash
umask 077
flask-unsign --decode --cookie < "$cookie_file" > "$decoded" 2> "$diagnostic"
status=$?
printf 'decoder status: %s\n' "$status"
~~~

The final argumentless `--cookie` reads stdin in the documented upstream implementation; confirm that contract in the installed release. If unsupported, stop and select a supported private input mechanism rather than silently supplying an empty cookie. Inspect both status and diagnostic before interpreting the output. Missing input, malformed encoding, decompression or JSON errors leave the decoding task incomplete.

Flask's default client session is signed, not encrypted. This tool handles its payload encoding and optional leading-dot compression marker; a three-part appearance does not establish JWT format. The CLI displays a Python representation, which may contain single quotes, tuples or tagged values; do not feed it to a JSON parser or evaluate it as Python. Preserve the original value separately when byte comparison matters.

Readable `logged_in`, username or role fields are unverified claims. This decoding mode does not check the secret, timestamp acceptance, server-side authorization or which serializer the deployed application uses. `--unsign` is a candidate-secret search, distinct from decoding; neither it nor signing a replacement session is needed for this inspection task.

See the [upstream CLI](https://github.com/Paradoxis/Flask-Unsign/blob/master/flask_unsign/__main__.py) for stdin/version/error behavior and [decoder implementation](https://github.com/Paradoxis/Flask-Unsign/blob/master/flask_unsign/session.py) for encoding and tagged-value handling. For application-specific session validation, inspect the acquired Flask configuration and consuming route separately.
