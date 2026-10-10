---
name: base64
description: Decode transferred binary artifacts and encode digest bytes or base64url text with GNU base64. Use when wrappers, line endings, partial output or alphabet/digest confusion causes corruption.
---

# Preserve the bytes behind the encoding

Base64 describes a representation, not encryption or a password-hash algorithm. Preserve the captured input and identify its container before decoding. Do not run decoding over an entire JSON object, mail message or terminal transcript; extract the actual field/body first.

For a MIME email attachment, select the exact part by its headers and boundary context; confirm that part's `Content-Transfer-Encoding` is `base64`. Decode only its body, excluding MIME headers and boundary delimiters. A MIME parser may already have decoded the payload, so check its API before applying another base64 pass. An `.enc` filename or an `X-Attached` header alone establishes neither transfer encoding nor encryption. After decoding, inspect the resulting file/container; a PEM private key can still be encrypted independently of its mail transport. See [MIME encoding](https://www.rfc-editor.org/rfc/rfc2045) and [multipart boundaries](https://www.rfc-editor.org/rfc/rfc2046).

For a Windows certutil-style transfer using exactly the certificate envelope below, define `captured` as the original text and `body` and `decoded` as new working-file paths:

~~~bash
sed 's/\r$//; /^-----BEGIN CERTIFICATE-----$/d; /^-----END CERTIFICATE-----$/d' "$captured" > "$body" &&
if base64 --decode "$body" > "$decoded"; then
    wc -c -- "$decoded"
    sha256sum -- "$decoded"
else
    printf '%s\n' 'Decode failed; output may be partial and must not be used.' >&2
    false
fi
~~~

This removes only the observed envelope and CRLF line endings. Other envelopes need their own exact extraction. GNU decoding accepts newlines; do not assume arbitrary spaces, prompts or carriage returns are acceptable. `--ignore-garbage` is not a repair for headers: many header letters are valid base64 characters and would be decoded as data. An `invalid input` error must not be dismissed merely because a file was produced.

Compare decoded size/checksum with the sender when available; otherwise verify the expected file signature and parse it with the appropriate reader. A matching checksum proves transfer consistency, not that a captured file is authentic or safe to execute. Keep decoded binary in files, not shell variables or text APIs that strip/transform bytes.

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
