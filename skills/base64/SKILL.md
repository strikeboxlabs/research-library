---
name: base64
description: Decode transferred binary artifacts and encode digest bytes or base64url text with GNU base64. Use when wrappers, line endings, partial output or alphabet/digest confusion causes corruption.
---

# Preserve the bytes behind the encoding

Read this entire SKILL.md before acting; reuse complete current context. Identify and isolate the encoding container, then check decode status and recovered bytes. For digest bytes, base64url or HTTP form fields, read [encoded fields](references/encoded-fields.md) fully before that procedure. Finish with the recovered artifact or field and its integrity/coverage limits; missing or abbreviated source bytes cannot be repaired by decoding.

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

This removes only the observed envelope and CRLF line endings. Other envelopes need their own exact extraction. GNU decoding accepts newlines; do not assume arbitrary spaces, prompts or carriage returns are acceptable. `--ignore-garbage` is not a repair for headers: many header letters are valid base64 characters and would be decoded as data. An `invalid input` error must not be dismissed merely because a file was produced. A transcript containing `<SNIP>`, an ellipsis or omitted lines is incomplete input: obtain the full body or another transfer, rather than deleting the marker and treating the remainder as complete. Even a successful decode can recover truncated but syntactically valid base64.

Compare decoded size/checksum with the sender when available; otherwise verify the expected file signature and parse it with the appropriate reader. A matching checksum proves transfer consistency, not that a captured file is authentic or safe to execute. Keep decoded binary in files, not shell variables or text APIs that strip/transform bytes.


Use the installed GNU `base64 --help` for option differences; [GNU documentation](https://www.gnu.org/software/coreutils/manual/html_node/base64-invocation.html) describes decoding and wrapping.
