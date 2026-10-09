---
name: xxd
description: Inspect exact file bytes and reconstruct deliberate hex artifacts with xxd. Use when offsets, endianness, partial dumps or reverse-mode patch behavior could corrupt binary evidence.
---

# Keep byte offsets and display formats distinct

Check `xxd -v` and local help; small reimplementations may support fewer options. Define `artifact` as an existing absolute working-copy path, `offset` as the observed byte offset and `length` as the number of bytes needed:

~~~bash
xxd -g 1 -c 16 -s "$offset" -l "$length" "$artifact"
~~~

`-g 1` exposes individual bytes and `-s` seeks in the **file**. It does not understand a debugger's virtual address or a decoded object's internal offset. Map those address spaces explicitly before comparing output. `-l` is a maximum; a shorter file can yield fewer bytes without supplying the requested region. Inspect the last offset and actual byte count.

The ASCII column is a convenience, not a faithful binary representation. Changing grouping or using `-e` changes displayed word order; it does not change the file or establish the structure's endianness. A key format's length prefixes and signed integers must be interpreted using that format, not inferred from one walkthrough's offsets. An OpenSSH private-key envelope and its public-key blob have different layouts.

For intentional reconstruction, define `dump` as a complete normal xxd-format dump and `reconstructed` as a fresh output path in a private directory:

~~~bash
umask 077
(set -C; xxd -r "$dump" > "$reconstructed")
~~~

Normal reverse mode uses the dump's addresses. A dump beginning at a nonzero offset can create a gap before its bytes; a selected region is not a complete original file. For a deliberately address-free plain hex stream, use `-r -p` instead. Do not feed a decorated screenshot or mixed prose to either parser and assume success means validity: reverse mode can silently skip material it does not parse, and plain mode can consume unintended hex pairs.

Passing an existing output filename directly to `xxd -r` can patch it without truncating its old tail. Use a new reconstruction artifact, check its length and compare its digest/bytes against an independent original or expected fixture. A correct prefix alone does not prove the rest of the file survived.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Attended pp. 30–31. Sources: [xxd manual](https://github.com/vim/vim/blob/master/runtime/doc/xxd.1), [OpenSSH envelope](https://github.com/openssh/openssh-portable/blob/master/PROTOCOL.key).
