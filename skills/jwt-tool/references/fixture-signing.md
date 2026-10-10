# Sign a controlled local fixture

Use the reviewed `jwt_script` absolute path and original compact `token` established in SKILL.md, with no target/request options.

For an authorized **local HS256 fixture**, define `key_file` as a private text file containing the exact known HMAC secret, with no accidental trailing newline:

~~~bash
python3 "$jwt_script" "$token" -T -S hs256 -kf "$key_file"
~~~

Change only the intended claim in the interactive menu and inspect the resulting JSON type. The reviewed implementation reads the entire key file for signing. A hex-looking secret remains literal text unless the application explicitly decodes it. `-T` without signing can leave the original signature attached to changed contents; printing a token does not make it valid. Verify the resulting signature and applicable issuer/audience/time requirements using the intended verifier.

Do not infer HS verification from `-V`: its reviewed path concerns asymmetric signatures/JWKS. `-t` or `-r` adds HTTP delivery, and scan modes can generate many requests; they are separate from this local procedure. Expiration, algorithm rejection, signature failure and application authorization failure need separate diagnoses. Do not extend timestamps or broaden claims just to hide an unexplained rejection.
