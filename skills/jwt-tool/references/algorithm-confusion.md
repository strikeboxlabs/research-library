# Test an algorithm/key mismatch without assuming RS256 is broken

Establish the original issuer/token, allowed algorithm, current verification key and one scoped action/control account. A public JWKS supplies public verification material; it does not make an HMAC secret. Algorithm confusion requires a verifier that improperly accepts an HMAC algorithm while treating asymmetric public-key bytes as its HMAC key. A service that pins RS256 and checks key type rejects that candidate.

Match the JWK by `kid`, algorithm and intended use, and obtain the corresponding verified public-key file using a trusted installed conversion facility when necessary. Exact PEM/DER representation, headers and newline bytes can matter to a confused verifier. Do not submit private tokens/keys to an online converter. Preserve the original compact token; decoding or a local signature success is separate from remote acceptance.

For a permitted local HS256 candidate using the already defined `jwt_script` and original `token`, set `public_key_file` to the exact reviewed public-key text representation:

~~~bash
python3 "$jwt_script" "$token" -T -S hs256 -kf "$public_key_file"
~~~

Use the interactive menu to change only the intended fixture claim and inspect its JSON type. Current jwt_tool signing reads a file with `-kf`; historical `-k filename` screenshots are not current flag guidance. Read the installed help and signing branch when the version differs. No target/request option is supplied here; keep its token-bearing output/logs private.

Compare the original authorized token and candidate against the same permitted, preferably non-mutating application action with the actual authentication carrier. An API may use `x-access-token` rather than Bearer. Record signature/algorithm rejection separately from expiration, issuer/audience, session state and role-based denial. A create operation's 403 can follow successful authentication; distinguish that from invalid-token responses. Candidate acceptance must be tied to a meaningful changed authorization result, not merely to a decoded role or a token printed by a signing tool. If a selected state-changing operation is necessary, scope its object and confirm resulting state/cleanup. See [jwt_tool signing and parser](https://github.com/ticarpi/jwt_tool/blob/master/jwt_tool.py) and [JWT algorithm verification guidance](https://www.rfc-editor.org/rfc/rfc8725.html#section-3.1).
