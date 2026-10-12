---
name: zcat
description: Expand a selected compressed ordinary file to stdout with GNU zcat, preserve the source and distinguish decompression success from complete archive extraction.
---

# Decompression to a separate stream

Read this entire SKILL.md before acting. Require the selected ordinary input, a fresh output and sufficient bounded storage. Define `zcat_bin` as the verified trusted GNU executable, `compressed` as the absolute input and `expanded` as the fresh absolute output. Finish with status, diagnostics and the resulting data's format; partial output is not a completed artifact.

~~~bash
"$zcat_bin" --version
"$zcat_bin" -- "$compressed" > "$expanded"
expand_status=$?
printf 'expand_status=%s\n' "$expand_status"
~~~

GNU zcat behaves as gunzip -c: it writes decompressed bytes to stdout and preserves the compressed input. A .gz suffix is unnecessary when the format is recognized. No input argument means reading stdin; a pipeline's last status can hide a failed decompressor. Avoid -f for format diagnosis: with stdout it can pass unrecognized data through unchanged.

Zero normally means success, 1 an error and 2 a warning. A failed decode can leave useful but incomplete bytes in the output; retain the diagnostic and prevent that partial artifact from being accepted downstream. Compression integrity does not authenticate provenance or validate the archive inside.

A gzip-labelled initrd file may hold an initramfs cpio archive, not a kernel executable. Modern initramfs buffers can combine uncompressed and compressed archives with padding; this simple whole-file decode does not establish complete coverage of such a buffer. Select its actual format reader and preserve boundaries. See [GNU gzip/zcat semantics](https://manpages.debian.org/bookworm/gzip/zcat.1.en.html) and [Linux initramfs format](https://www.kernel.org/doc/html/latest/driver-api/early-userspace/buffer-format.html).
