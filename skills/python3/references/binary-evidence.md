# Inspect binary evidence without text conversion

Select a trusted `python_bin` before using the standard-library helper.

When a script constructs a file or request body, check the bytes before changing the receiving service. Python 3 `str` holds Unicode; `"\x89"` is a character, while `b"\x89"` is one byte. Encoding the former as UTF-8 produces `c2 89`. Use bytes literals or binary file reads for binary content; choose an encoding only for a genuinely textual field.

When reviewing an input-length validator, trace the selected field through normalization, concatenation, encoding and the consuming API. `len(text)` counts Unicode code points, while `len(text.encode('utf-8'))` counts encoded bytes; neither necessarily counts displayed glyphs. ASCII code points occupy one UTF-8 byte, with other valid code points taking two to four. An earlier character limit does not establish a later byte limit. Reproduce only owned nonsecret examples, retaining the encoding and consumer/version contract. For pyca bcrypt, `hashpw` in5.0.0 raises ValueError above72bytes; older releases silently truncated. That is not a universal71bytes-plus-NUL rule or evidence for an unknown wrapper. A failed comparison alone cannot identify hidden preprocessing. Inspect the exact implementation before changing stored-data compatibility; silently slicing or prehashing input changes that contract. See [Python Unicode encoding](https://docs.python.org/3.12/howto/unicode.html) and [bcrypt change history](https://github.com/pyca/bcrypt/blob/main/CHANGELOG.rst).

Define `artifact` as a local regular working-copy file and inspect only its first 16 bytes with that trusted interpreter:

~~~bash
"$python_bin" -I -S - "$artifact" <<'PY'
import sys

with open(sys.argv[1], 'rb') as source_file:
    prefix = source_file.read(16)
signature = bytes.fromhex('89504e470d0a1a0a')
print('prefix_bytes:', len(prefix))
print('hex:', prefix.hex(' '))
print('png_signature:', prefix.startswith(signature))
PY
~~~

An **illustrative** prefix `c2 89 50 4e 47 0d 0a 1a 0a` suggests the PNG signature passed through UTF-8 text encoding. Trace where the bytes became text and where they were encoded; do not blindly strip `c2` from the artifact. Fewer than eight bytes cannot contain the complete PNG signature. `png_signature: True` establishes only that prefix, even for an eight-byte file with no image chunks. Validate the complete artifact with its intended decoder before claiming a usable image. `prefix_bytes` is the bounded read length, not the file size.

For multipart clients, inspect the prepared part's bytes, not just its declared MIME type or the script's unconditional success message. A local file check alone does not prove the transmitted body was identical; library encoding and application acceptance need separate evidence.

For a text-producing protocol handler, compare character count with the final encoded bytes. `len(body)` on a string is not necessarily an HTTP Content-Length in octets; binary bodies interpolated into a text template can become a representation instead of original bytes. A single `recv(1024)` also need not contain a complete request, and `send` can write fewer bytes than supplied. A UTF-8 character can span received chunks, so decoding each chunk independently can fail even for valid text. Preserve bytes until the framed message is complete or use the intended incremental decoder. A read loop waiting for EOF is incomplete on a kept-open connection and needs size/time bounds; closing in a finally/context manager also matters on exceptions. Review framing, decoding, serialization and complete-send handling separately. See [HTTP content length](https://www.rfc-editor.org/rfc/rfc9110.html#name-content-length) and [socket I/O](https://docs.python.org/3.12/library/socket.html).

For a finite artifact download, a single `recv(8192)` is an upper bound for that call, not evidence of a complete file. Establish protocol framing, accumulate the bounded payload and verify its expected length/digest before replacing an existing artifact. Header/status recognition, printing a new filename and a successful later copy do not establish body completeness. Keep protocol diagnostics separate from a filename returned on stdout; the consumer must check producer status before treating nonempty output as a path.

For a custom character transformation, `ord`/`chr` operate on Unicode code points rather than UTF-8 bytes. Preserve the exact modulus and accepted input domain: reducing modulo 255 discards information for unrestricted Unicode input and differs from byte arithmetic modulo 256. Empty repeating inputs and mismatched lengths can fail before output; text-mode newline conversion can alter otherwise valid encoded data. Validate an intended round trip with owned nonsecret examples before interpreting a recovered string, rather than silently repairing copied arithmetic or executing acquired scripts.

For an operation pairing byte sequences, ordinary `zip` stops at the shortest input without reporting omitted bytes. Establish the intended length contract first; require equal lengths when every byte must have a partner, or record the selected covered prefix explicitly. Python3.10+ `zip(..., strict=True)` reports a mismatch during iteration. A shorter plausible output does not prove complete recovery. See [zip length behavior](https://docs.python.org/3/library/functions.html#zip).

For an acquired complete byte array transformed with one known XOR byte, preserve the operand and integer range: with `data` as bytes and `mask` in0–255, `decoded = bytes(value ^ mask for value in data)` preserves every resulting byte. Joining `chr(...)` instead produces Unicode text; later UTF-8 encoding can change values above127 into several bytes. Keep the decoded bytes/length and choose a character encoding only when the consumer establishes it. A readable result does not prove execution or authenticate the acquired array, and this fixed known transformation is separate from searching for a secret key.

See Python's [binary versus text I/O](https://docs.python.org/3.12/library/functions.html#open), [bytes and encoding](https://docs.python.org/3.12/library/stdtypes.html#bytes-objects) and the [PNG signature specification](https://www.w3.org/TR/png-3/#5PNG-file-signature).

## Decode a complete hex capture to fresh binary output

Require a complete selected hex-only capture, a trusted Python 3.7+ interpreter and a fresh output path in an owned directory. Define `hex_file` and `output` as absolute paths. Remove display labels, length lines and truncation markers by selecting the actual captured field; do not guess omitted bytes. For a bounded capture:

~~~bash
"$python_bin" -I -S - "$hex_file" "$output" <<'PY'
import hashlib
import sys

with open(sys.argv[1], 'rb') as source_file:
    encoded = source_file.read(1048577)
if len(encoded) > 1048576:
    sys.exit('capture exceeds this 1 MiB input bound')
data = bytes.fromhex(encoded.decode('ascii'))
with open(sys.argv[2], 'xb') as output_file:
    output_file.write(data)
print('decoded_bytes:', len(data))
print('sha256:', hashlib.sha256(data).hexdigest())
PY
status=$?
~~~

`bytes.fromhex` accepts paired hex digits and ignores ASCII whitespace in Python 3.7+. Nonhex content, odd digits or non-ASCII text fail before output is created. `xb` refuses an existing output, including a dangling symlink; a write failure can leave a partial fresh file, so retain the status and use another fresh path after resolving it. Empty input decodes to empty bytes and needs the task's expected-length check.

`print(bytes.fromhex(...))` produces a representation such as **illustrative** `b'\x00A'`, not those original binary bytes on stdout. Binary output above avoids that conversion. Compare the decoded length/digest with independent acquisition expectations, then use the format's actual reader on a coherent working copy. A magic signature does not establish a complete SQLite snapshot or preserved WAL state, and a syntactically valid hex string does not prove the capture was complete.
