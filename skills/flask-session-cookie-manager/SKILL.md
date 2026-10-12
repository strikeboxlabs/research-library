---
name: flask-session-cookie-manager
description: Decode an acquired Flask client-session cookie locally with the Python3 Flask Session Cookie Manager. Use when compressed payloads, tagged bytes or successful exit status obscure what the decoder actually recovered.
---

# Decode the selected session representation

Read this entire SKILL.md before acting. Require the trusted installed Python3 manager script, its compatible Flask/itsdangerous environment and the complete small acquired cookie. All instructions are inline. Finish with decoded bytes and diagnostics, retaining the signature/authentication gap; missing dependencies or malformed data leave decoding incomplete.

Define `python_bin` as that interpreter and `manager_script` as the verified absolute flask_session_cookie_manager3.py file. Inspect the actual implementation: packaged console entry points can differ from direct script execution. These commands identify its subcommand contract without a cookie:

~~~bash
"$python_bin" "$manager_script" --help
"$python_bin" "$manager_script" decode --help
~~~

For a deliberately public test specimen in `specimen`, direct decoding is:

~~~bash
"$python_bin" "$manager_script" decode -c "$specimen"
~~~

That CLI puts its input in process arguments. For a private captured value, define `cookie_file` as its private ASCII file and `decoded` as a fresh private output file. The following calls the installed tool's decode API without running its CLI main block or placing the cookie in argv:

~~~bash
umask 077
"$python_bin" - "$manager_script" "$cookie_file" > "$decoded" <<'PY'
import pathlib, runpy, sys
manager, source = sys.argv[1:]
raw = pathlib.Path(source).read_bytes()
cookie = raw.decode('ascii').strip()
if not cookie or any(c.isspace() for c in cookie):
    raise SystemExit('Missing or split cookie')
tool = runpy.run_path(manager, run_name='owned_cookie_decoder')
result = tool['FSCM'].decode(cookie)
if not isinstance(result, bytes):
    raise SystemExit(str(result))
sys.stdout.buffer.write(result)
PY
status=$?
~~~

Check status and errors before using the output. Loading the script imports trusted code/dependencies; it is not passive source reading. Unknown implementation/API needs inspection rather than guessing an equivalent name. Use the worker's resource limits for untrusted compressed input: the decoder has no expanded-size cap.

Without a secret, this implementation recovers payload bytes, including leading-dot zlib compression, without verifying the signature or timestamp. Its CLI catches errors and can print a decoding-error string with exit zero. A Python bytes display such as b'...' is not itself JSON. Tagged byte objects inside the recovered JSON require their format-aware decoder before interpreting nested base64/XML; do not evaluate printed Python or parse XML with external entities enabled. A field named lxml does not identify the installed parser version.

Decoding establishes representation, not server acceptance, identity or authorization. Retain the original cookie separately when byte comparison matters. Signing replacements and secret searching are outside this inspection task.

References: [upstream usage and authors Wilson Sumanang/Alexandre ZANNI](https://github.com/noraj/flask-session-cookie-manager), [Python3 decoding implementation](https://github.com/noraj/flask-session-cookie-manager/blob/master/flask_session_cookie_manager3.py).
