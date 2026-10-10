# Inspect binary evidence without text conversion

Select a trusted `python_bin` before using the standard-library helper.

When a script constructs a file or request body, check the bytes before changing the receiving service. Python 3 `str` holds Unicode; `"\x89"` is a character, while `b"\x89"` is one byte. Encoding the former as UTF-8 produces `c2 89`. Use bytes literals or binary file reads for binary content; choose an encoding only for a genuinely textual field.

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

See Python's [binary versus text I/O](https://docs.python.org/3.12/library/functions.html#open), [bytes and encoding](https://docs.python.org/3.12/library/stdtypes.html#bytes-objects) and the [PNG signature specification](https://www.w3.org/TR/png-3/#5PNG-file-signature).
