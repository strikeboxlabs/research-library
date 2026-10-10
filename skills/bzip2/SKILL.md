---
name: bzip2
description: Test and decompress a selected bzip2 stream while preserving its source. Use for renamed artifacts, nested compression and partial-output or suffix-related failures.
---

# Recover one bzip2 layer

Read this entire SKILL.md before acting; reuse complete current context. Establish the actual bzip2 input and a fresh output path, preserve final status and inspect the decoded object's next format. A recognizable header or some decoded bytes is not complete recovery.

Define `compressed` as the existing absolute input and `decoded` as a fresh absolute file in an existing private directory. Select bzip2, not gzip, from the observed bytes/parser result:

~~~bash
umask 077
bzip2 --help
bzip2 -t -- "$compressed" &&
(set -C; bzip2 -dc -- "$compressed" > "$decoded") &&
file -E -h -- "$decoded"
~~~

Use the help banner for a passive version/options probe. Version/license flags can continue into normal compression on implementations such as bzip2 1.0.8; do not attach them to an unknown data stream.

`-t` tests the complete compressed stream without producing decoded output; `-d` decompresses and `-c` writes stdout, retaining the input. The two passes cost extra I/O; a bounded single `-dc` pass can also supply the result when its final status is captured and failed output stays partial. Shell noclobber protects the new destination; it does not bound expansion size. Apply the worker's byte/time budget and check available space.

A `BZh` header is a format lead, not a CRC/integrity result. Wrong format, truncated input, CRC error, unreadable source or an output-write failure require distinct recovery. Decompression can write a prefix before failing; preserve it separately and do not label it complete. Do not add `-f` as corruption repair: in stdout mode it can pass unrecognized input through unchanged.

Plain `bzip2 -d file` replaces/deletes the compressed file on success unless `-k` is selected. It derives an output name from recognized suffixes or uses `.out` when it cannot guess the original name. That message alone is not corrupt data. `-dc` with a selected output avoids suffix renaming and input deletion; do not repeatedly rename one artifact just to make a decompressor accept its extension.

The decoded object may be another compressed stream or a tar archive. Classify and validate the next layer independently, preserving each layer's path/status and the original acquisition. bzip2 is not a multi-file archive format. Stop when the requested object is recovered with supported integrity/coverage; a valid inner object does not repair an incomplete outer transfer. A known concatenated bzip2 stream can contain multiple members; do not assume its decoded bytes are one original file merely because decoding succeeded.

If results/options disagree with the invocation, inspect inherited `BZIP2` and `BZIP` settings: bzip2 processes those arguments before the command-line ones. An inherited force/output option can change the boundary being tested.

Reference: [upstream bzip2 manual](https://sourceware.org/bzip2/manual/manual.html).
