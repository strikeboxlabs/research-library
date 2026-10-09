---
name: jwt-tool
description: Inspect and modify controlled JWT fixtures with ticarpi jwt_tool. Use when claim types, signing algorithms, key-file bytes or confusing decoded claims with verified identity causes mistakes.
---

# Inspect the token before selecting a mode

Use ticarpi's `jwt_tool.py`, not an unrelated package with a similar name. Check its help and version banner. Define `jwt_script` as the reviewed script's absolute path and `token` as the original compact JWT without its Bearer prefix:

~~~bash
python3 "$jwt_script" "$token"
~~~

This decodes locally when no target/request options are supplied. The first invocation may initialize configuration/keys and exit with status 1; inspect that setup message and rerun rather than diagnosing a token failure. The three segments are base64url-encoded header, payload and signature bytes; decoding does not verify the signature or establish that the service accepts the claims. Preserve the original string. Tokens appear in process arguments and this tool can retain them in local logs under `~/.jwt_tool`; use private fixture material and inspect its configuration before working with sensitive captures.

Read `alg`, claim types and timestamps, then establish the service's actual allowed algorithm and key source independently. A field named `API_KEY` is not necessarily the signing secret; BackendTwo established the connection through the application's settings. A changed account record also does not rewrite an already issued token. Obtain a fresh authorized login token when testing updated account state.

For an authorized **local HS256 fixture**, define `key_file` as a private text file containing the exact known HMAC secret, with no accidental trailing newline:

~~~bash
python3 "$jwt_script" "$token" -T -S hs256 -kf "$key_file"
~~~

Change only the intended claim in the interactive menu and inspect the resulting JSON type. The reviewed implementation reads the entire key file for signing. A hex-looking secret remains literal text unless the application explicitly decodes it. `-T` without signing can leave the original signature attached to changed contents; printing a token does not make it valid. Verify the resulting signature and applicable issuer/audience/time requirements using the intended verifier.

Do not infer HS verification from `-V`: its reviewed path concerns asymmetric signatures/JWKS. `-t` or `-r` adds HTTP delivery, and scan modes can generate many requests; they are separate from this local procedure. Expiration, algorithm rejection, signature failure and application authorization failure need separate diagnoses. Do not extend timestamps or broaden claims just to hide an unexplained rejection.

Documentation reviewed 2026-10-09; Linux execution untested. Cases: Backend pp. 15–16; BackendTwo pp. 13–15. Sources: [tool implementation](https://github.com/ticarpi/jwt_tool/blob/master/jwt_tool.py), [JWT specification](https://www.rfc-editor.org/rfc/rfc7519.html).
