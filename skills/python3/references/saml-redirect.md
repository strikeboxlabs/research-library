# Decode a captured SAML Redirect request offline

Use this only for a captured HTTP Redirect URL containing `SAMLRequest` with the DEFLATE encoding. HTTP POST binding normally carries base64 XML without this compression step. Preserve the original URL privately: re-encoding query fields can change bytes needed for signature verification. Do not send authentication material to an online decoder.

Select a trusted `python_bin` and save the complete, still URL-encoded URL as ASCII in the existing local `capture` file. Define `decoded` as a fresh private output path. This helper accepts at most 1 MiB of input and output, decodes once, requires one complete raw DEFLATE stream and writes bytes without parsing XML:

~~~bash
umask 077
"$python_bin" -I -S - "$capture" "$decoded" <<'PY'
import base64, binascii, sys, urllib.parse, zlib

limit = 1024 * 1024
with open(sys.argv[1], 'rb') as source:
    raw = source.read(limit + 1)
if len(raw) > limit:
    raise SystemExit('Capture exceeds the 1 MiB limit')
try:
    url = raw.decode('ascii').rstrip('\r\n')
    if any(ord(c) < 33 or ord(c) == 127 for c in url):
        raise ValueError('Whitespace/control bytes in URL; recapture it')
    parts = urllib.parse.urlsplit(url)
    if parts.scheme not in ('http', 'https') or not parts.netloc:
        raise ValueError('Expected a complete HTTP(S) Redirect URL')
    pairs = urllib.parse.parse_qsl(parts.query, keep_blank_values=True,
                                  errors='strict', max_num_fields=32)
    requests = [v for k, v in pairs if k == 'SAMLRequest']
    encodings = [v for k, v in pairs if k == 'SAMLEncoding']
    expected = 'urn:oasis:names:tc:SAML:2.0:bindings:URL-Encoding:DEFLATE'
    if len(requests) != 1 or (encodings and encodings != [expected]):
        raise ValueError('Need one SAMLRequest and the DEFLATE encoding')
    packed = base64.b64decode(requests[0], validate=True)
    stream = zlib.decompressobj(wbits=-15)
    data = stream.decompress(packed, limit + 1)
    if len(data) > limit or not stream.eof or stream.unused_data or stream.unconsumed_tail:
        raise ValueError('Oversize, truncated or trailing compressed data')
except (ValueError, UnicodeError, binascii.Error, zlib.error) as error:
    raise SystemExit(str(error))
with open(sys.argv[2], 'xb') as output:
    output.write(data)
print('Decoded bytes:', len(data))
PY
~~~

On a base64 error, check whether `%2B` was decoded earlier into `+` and then changed to a space. Reacquire the raw URL; do not guess replacements or silently strip invalid characters. A DEFLATE error calls for checking binding, encoding and capture completeness. Negative `wbits` selects raw DEFLATE, not a zlib/gzip wrapper. The limits deliberately reject oversized captures; a decoding failure leaves no newly decoded output. An existing destination is never overwritten.

Inspect the resulting bytes in a text viewer with the document's declared encoding. Successful decoding does not establish well-formed XML, signature validity, trust or accepted authentication. An `AuthnRequest` requests authentication; it is not an issued assertion. Its `ID` identifies the request, while `AssertionConsumerServiceURL` names the requested response destination. An application identifier embedded in that URL's path is not the request ID. The request's `Issuer` identifies its sender (typically the service provider); do not substitute it for a configured identity-provider issuer. URI-shaped entity identifiers need not be fetchable endpoints, and changing their scheme changes the identifier.

Use [SAML binding sections 3.4–3.5](https://docs.oasis-open.org/security/saml/v2.0/saml-bindings-2.0-os.pdf), [SAML core section 3.4.1](https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf), and Python's [URL parser](https://docs.python.org/3.12/library/urllib.parse.html), [strict base64 decoder](https://docs.python.org/3.12/library/base64.html) and [bounded decompressor](https://docs.python.org/3.12/library/zlib.html) to resolve variant inputs. Signature verification is a separate operation using trusted metadata and the preserved original capture.
