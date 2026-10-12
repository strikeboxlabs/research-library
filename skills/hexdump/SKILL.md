---
name: hexdump
description: Inspect a selected binary region with util-linux hexdump in canonical byte form. Use when repeated-line suppression, offsets or word display obscure exact artifact bytes.
---

# Inspect bytes at their file offsets

Read this entire SKILL.md before acting. Require the acquired ordinary file and selected byte region. No conditional resources are required. Finish with status, actual covered offsets and the format-supported interpretation; a partial region cannot establish a whole object.

Check `hexdump --version` and local options. Define `artifact` as the working-copy path, `offset` as a nonnegative byte offset and `length` as the positive byte budget:

~~~bash
hexdump -C -v -s "$offset" -n "$length" -- "$artifact"
status=$?
~~~

`-C` shows individual hex bytes and an ASCII approximation. `-v` prevents repeated groups becoming a single asterisk. The default/two-byte word views differ from canonical bytes and must not establish a format's endianness. `-s` skips file bytes; it does not interpret runtime addresses. `-n` is a maximum, so an early EOF can yield fewer bytes. Check the final offset and diagnostics.

Decode a complete encoded field into a separate file first and retain that decoder's status. A successful final hexdump cannot repair an earlier failed pipeline. Interpret length prefixes using the actual format rather than copying screenshot offsets.

Source: [util-linux hexdump](https://manpages.debian.org/bookworm/bsdextrautils/hexdump.1.en.html).
