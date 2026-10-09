---
name: base64
description: Decode transferred binary artifacts and encode digest bytes or base64url text with GNU base64. Use when wrappers, line endings, partial output or alphabet/digest confusion causes corruption.
---

# Preserve the bytes behind the encoding

Base64 describes a representation, not encryption or a password-hash algorithm. Preserve the captured input and identify its container before decoding. Do not run decoding over an entire JSON object, mail message or terminal transcript; extract the actual field/body first.

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

Documentation reviewed 2026-10-09; Linux execution untested. Cases: Arkham pp. 13–14; Artificial p. 11; Atom p. 11; BackendTwo pp. 10–11, 16. Sources: [GNU base64](https://www.gnu.org/software/coreutils/manual/html_node/base64-invocation.html), [OpenSSL dgst](https://docs.openssl.org/3.5/man1/openssl-dgst/), [RFC 4648 base64url](https://www.rfc-editor.org/rfc/rfc4648.html).
