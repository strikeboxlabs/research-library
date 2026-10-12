---
name: gzrecover
description: Salvage readable regions of an owned damaged gzip stream with gzrt. Use after gzip reports integrity errors and ordinary decompression cannot recover the needed data.
---

# Recover partial gzip data

Read this entire SKILL.md before acting. Require an owned preserved compressed input, a trusted gzrt executable and fresh outputs in a private working directory. Finish with the recovered artifact, diagnostics and explicitly identified integrity gaps; readable text alone is not a complete recovered backup.

Define `compressed`, `recovered` and `diagnostics` as absolute paths, with the latter two nonexistent. Retain the original's size and SHA-256. Check help/version together before recovery:

~~~bash
gzrecover -V -h
(umask 077; set -C; gzrecover -v -p "$compressed" > "$recovered" 2> "$diagnostics")
~~~

In the reviewed gzrt implementation, `-V` prints a version but continues to input processing; adding `-h` exits through help. `-p` streams salvaged bytes to stdout and `-v` sends recovery diagnostics to stderr. Shell noclobber protects fresh outputs. Direct `-o` and default output creation can overwrite an existing file without truncating its old tail, so do not use them against existing artifacts.

Keep a failed or partial result labeled as such. Recovery can skip damaged compressed regions and still return zero; it does not repair missing records, establish ordering across gaps or validate an SQL/database backup. Compare recovered structure, expected record counts and independently known values with the actual consumer's non-executing validator. Do not import recovered SQL merely to see whether the text looks plausible. Apparent credential/token fragments can contain corruption and need independent validation.

A CRC/length error establishes failed gzip integrity, not its cause. Text-mode transfer is one possible cause only when transfer-mode evidence supports it. If recovery fails or the requested record crosses a damaged region, retain the original and identify that gap rather than fabricating missing bytes. A trusted complete backup is preferable when available.

Resolve implementation differences against [gzrt usage](https://github.com/arenn/gzrt/blob/master/README) and [output/version handling](https://github.com/arenn/gzrt/blob/master/gzrecover.c).
