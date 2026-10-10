# Distinguish digest bytes, alphabets and outer transport encoding

For a format requiring base64 of a SHA-512 **binary digest**, define `artifact` as the input file and `digest` as a new temporary file:

~~~bash
openssl dgst -sha512 -binary "$artifact" > "$digest" && base64 --wrap=0 "$digest"
~~~

Encoding the printed hexadecimal digest gives different bytes. JSON-wrapped bcrypt records likewise need decoding to the complete `$2...` record before selecting a hash mode; base64 itself is not that mode.

For an endpoint specifically requiring **unpadded base64url**, define `path_text` as the exact textual value, without NUL bytes:

~~~bash
printf '%s' "$path_text" | base64 --wrap=0 | tr '/+' '_-' | tr -d '='
~~~

Quoting and `printf` preserve spaces without adding a newline; GNU `--wrap=0` avoids its default line wrapping. The translated alphabet is different from ordinary base64 and HTTP percent encoding. Remove padding only when the consuming format specifies that convention. Decoding unpadded base64url requires reversing the alphabet and restoring valid padding; `--ignore-garbage` cannot perform that conversion.

## Keep HTTP form encoding outside base64

For an `application/x-www-form-urlencoded` capture, parse the actual body and select the intended field, undoing form encoding once **before** base64 decoding. `%2B` becomes a literal base64 `+`; a raw `+` in a form represents a space. Do not run a second form decode on the recovered value or use `--ignore-garbage` to hide this corruption. A `%3D` sequence is percent-encoded padding, not a different base64 alphabet. Duplicate fields need the application's selection rules; do not silently concatenate them.

For an authorized endpoint that expects a base64 value in a form field named `data`, define `payload` as the exact reviewed input file, `encoded` as a fresh file, `url` as the endpoint, and `headers`/`response` as fresh response files:

~~~bash
base64 --wrap=0 "$payload" > "$encoded" &&
curl --silent --show-error --connect-timeout 5 --max-time 30 --data-urlencode "data@$encoded" --dump-header "$headers" --output "$response" "$url"
~~~

Curl performs the outer form encoding, including `+`, `/` and `=`; give it unescaped base64, not an already percent-encoded string. The file form avoids shell newline transformations and an added `echo` newline. Check curl's exit status and the application's response separately. Decoding a response to XML or PHP bytes establishes the recovered representation, not that a database write or code execution occurred. Preserve bytes and their declared character encoding before displaying them as text.

References: [GNU base64](https://www.gnu.org/software/coreutils/manual/html_node/base64-invocation.html), [curl form encoding](https://curl.se/docs/manpage.html#--data-urlencode), [form decoding semantics](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.unquote_plus) and [RFC 4648 alphabets](https://www.rfc-editor.org/rfc/rfc4648.html).
