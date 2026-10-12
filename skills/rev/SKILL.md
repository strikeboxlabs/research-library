---
name: rev
description: Reverse characters within each complete line of a selected nonsecret text artifact with util-linux rev. Use when line reversal must be distinguished from reversing record order or decoding an acquired representation.
---

# Reverse the selected text lines

Read this entire SKILL.md before acting. Require installed util-linux rev, a preserved bounded nonsecret text input and its encoding/line-boundary contract. Follow the transformation below; finish with status and verified output bytes. No conditional resources are required. Reversed text does not establish a credential, decrypted value or correct earlier decoding.

Check `rev --version`. Define `input` as the existing text file and `output` as a fresh distinct path. This example assumes complete newline-terminated ASCII records:

~~~bash
LC_ALL=C rev < "$input" > "$output"
status=$?
~~~

Rev reverses characters within each line and preserves line order. The **illustrative** record `ABC-12` becomes `21-CBA`; reversing a whole file's byte stream or record order is a different task. This does not decode base64 or decide whether a source's earlier transformation was correct.

Check status, stderr and the intended per-line transformation against the preserved input. A failed read/write can leave partial output. Same-file redirection would truncate the source before reading; aliases/hard links can cause the same problem.

The implementation buffers a whole wide-character line, so a huge input without line breaks can exhaust memory. For non-ASCII input, require the actual locale/encoding and intended character semantics; visual glyphs can contain multiple characters. Keep binary artifacts with their binary reader instead of reversing them as text.

Reference: [util-linux rev manual](https://manpages.debian.org/bookworm/util-linux/rev.1.en.html).
