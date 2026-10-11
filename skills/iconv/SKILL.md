---
name: iconv
description: Convert captured text between explicit character encodings with iconv. Use for UTF-16 artifacts, unexpected NUL bytes, byte-order questions or failed conversions where deleting bytes would corrupt evidence.
---

# Decode characters after recovering the bytes

Read this entire SKILL.md before acting. Require the original bytes, evidence for the input encoding, the consumer's output-encoding contract and a fresh output path. Select decoding or conversion for that contract below; both require immediate status and byte/content checks. Finish with the input/output encodings, complete converted artifact and its limits, or the specific malformed/unsupported encoding gap.

First separate the representation from the encoding: hex/base64 decoding recovers bytes; `iconv` interprets those bytes as characters. A Windows origin or alternating zeros is a clue, not proof of UTF-16LE. Establish the encoding from the producing format, byte-order mark or other evidence. Check supported names with `iconv -l`.

Name both encodings explicitly: when `-f` or `-t` is omitted, that side defaults from the current locale. For a consumer requiring UTF-16LE bytes without a BOM, define `input` as confirmed UTF-8 text and `output` as a fresh file:

~~~bash
if iconv -f UTF-8 -t UTF-16LE "$input" > "$output"; then
    xxd -g 1 "$output"
else
    printf '%s\n' 'Conversion failed; output may be partial.' >&2
    false
fi
~~~

The illustrative UTF-8 bytes `41 c4 81 e2 82 ac` become `41 00 01 01 ac 20`. Base64, if a transport requires it, is a separate encoding of these resulting bytes. UTF-16LE is this consumer's contract, not a universal Windows text encoding. Preserve binary in a file and apply the failure rules below to either direction.

For confirmed **UTF-16LE without a BOM**, define `raw` as the recovered binary file and `text` as a fresh output path:

~~~bash
if iconv -f UTF-16LE -t UTF-8 "$raw" > "$text"; then
    xxd -g 1 "$text"
else
    printf '%s\n' 'Conversion failed; output may be partial.' >&2
    false
fi
~~~

An **illustrative** input `41 00 01 01 ac 20` represents `Aā€`; its UTF-8 result is `41 c4 81 e2 82 ac`. Deleting `00` bytes or hex pairs does not perform this conversion. UTF-16 uses two-byte code units and sometimes surrogate pairs; characters do not all occupy one byte or one code unit.

For a BOM-bearing UTF-16 stream, use `-f UTF-16` with an implementation that consumes the BOM; inspect the result before using it. An explicit endian decoder can preserve the BOM as a character. A NUL string terminator is separate from byte order: conversion can preserve it, so remove it only according to the enclosing field's format. Keep intermediate binary in files.

On failure, check for truncated code units, malformed surrogates and the wrong declared encoding. Do not accept partial output or retry with `-c`, `//IGNORE` or `//TRANSLIT` when exact identity matters: those options discard or approximate data. Successful conversion alone does not establish that the selected encoding was correct; compare meaningful content with the producing format.

See the [iconv manual](https://man7.org/linux/man-pages/man1/iconv.1.html) for options and the [Unicode encoding/BOM FAQ](https://www.unicode.org/faq/utf_bom.html) for byte-order distinctions.
