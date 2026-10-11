---
name: xxd
description: Inspect exact bytes and reconstruct hex artifacts with xxd. Use when offsets, partial dumps, reverse-mode patching or hex-versus-text encoding could corrupt binary evidence.
---

# Keep byte offsets and display formats distinct

Read this entire SKILL.md before acting; reuse complete current context. Choose inspection, plain-hex rendering, normal-dump reconstruction or plain-hex decoding below, with fresh outputs for conversion. Preserve offsets, final status and resulting byte/format evidence; a parsed prefix or successful reverse exit alone is not complete recovery.

Check `xxd -v` and local help; small reimplementations may support fewer options. Define `artifact` as an existing absolute working-copy path, `offset` as the observed byte offset and `length` as the number of bytes needed:

~~~bash
xxd -g 1 -c 16 -s "$offset" -l "$length" "$artifact"
~~~

`-g 1` exposes individual bytes and `-s` seeks in the **file**. It does not understand a debugger's virtual address or a decoded object's internal offset. Map those address spaces explicitly before comparing output. `-l` is a maximum; a shorter file can yield fewer bytes without supplying the requested region. Inspect the last offset and actual byte count.

The ASCII column is a convenience, not a faithful binary representation. Changing grouping or using `-e` changes displayed word order; it does not change the file or establish the structure's endianness. A key format's length prefixes and signed integers must be interpreted using that format, not inferred from one walkthrough's offsets. An OpenSSH private-key envelope and its public-key blob have different layouts.

## Render acquired bytes as plain hex

For a format requiring the hexadecimal representation of an already acquired byte file, define `hex_output` as a fresh distinct path:

~~~bash
umask 077
xxd -p -c 256 "$artifact" > "$hex_output"
status=$?
~~~

`-p` omits addresses and the ASCII column; `-c 256` displays up to **256 input bytes per line**, not 256 hex characters or a total-size limit. Longer input wraps onto more lines; nonempty output includes a line ending. Each byte becomes two hex digits, including leading zero bytes. **Illustrative:** the three bytes `00 41 ff` become `0041ff` followed by a newline. Preserve the full result rather than assuming it is one line or deleting arbitrary whitespace from an unknown container.

When the input was Base64, first isolate and decode the complete field into a separate byte file, check that decoder's status, then render it. Base64 decoding followed by xxd is a representation change, not another hash, encryption or proof of authentication. A pipeline whose final xxd succeeds can conceal a failed/partial decoder. Retain input byte count and expected format alongside status; plain hex has no offsets and does not identify the byte format by itself.

For intentional reconstruction, define `dump` as a complete normal xxd-format dump and `reconstructed` as a fresh output path in a private directory:

~~~bash
umask 077
(set -C; xxd -r "$dump" > "$reconstructed")
~~~

Normal reverse mode uses the dump's addresses. A dump beginning at a nonzero offset can create a gap before its bytes; a selected region is not a complete original file. For a deliberately address-free plain hex stream, use `-r -p` instead. Do not feed a decorated screenshot or mixed prose to either parser and assume success means validity: reverse mode can silently skip material it does not parse, and plain mode can consume unintended hex pairs.

Passing an existing output filename directly to `xxd -r` can patch it without truncating its old tail. Use a new reconstruction artifact, check its length and compare its digest/bytes against an independent original or expected fixture. A correct prefix alone does not prove the rest of the file survived.

A normal dump of compressed bytes reconstructs the compressed object, not its final plaintext. A leading `42 5a 68` is an **illustrative** bzip2 header lead; validate that stream with the format's actual integrity test. For nested bzip2/gzip/tar, save each complete decoded layer to a separate new file, classify it and select its own parser. Do not infer a fixed decompression sequence from a similar walkthrough or treat a header as whole-file validation. A readable inner member does not prove complete outer acquisition.

## Hex bytes are not yet decoded text

For a captured registry value, isolate just its complete hex payload into `hex_file`; choose a fresh `raw` output. Check for an even number of hex digits and only the expected whitespace before decoding:

~~~bash
(set -C; xxd -r -p "$hex_file" > "$raw") && xxd -g 1 "$raw"
~~~

In an **illustrative** field, `41000101ac20` becomes `41 00 01 01 ac 20`. If the producing format establishes UTF-16LE, those bytes encode `Aā€`; the zeros are part of the encoding. Deleting `00` with `sed` before decoding corrupts the value and can even remove pairs across byte boundaries. Preserve bytes first, then use an encoding-aware decoder such as `iconv -f UTF-16LE -t UTF-8`. Treat a trailing NUL according to the field format, not as permission to strip every zero. A registry value named `PasswordHash` does not establish a hash algorithm.

Consult the [xxd manual](https://github.com/vim/vim/blob/master/runtime/doc/xxd.1) for reverse-mode caveats and the [OpenSSH envelope specification](https://github.com/openssh/openssh-portable/blob/master/PROTOCOL.key) when interpreting that format.
