---
name: binwalk
description: Identify embedded signatures, inspect entropy and extract selected data from firmware or binary files.
---

# Binwalk signature scan and extraction

Read this entire SKILL.md before acting. Define `input` as the acquired file; preserve it and use a fresh `outdir` for extraction. Scan first, then extract only the selected matches when required. Finish with offsets, verified file types, produced artifacts and any extraction failures; a signature match alone does not establish a valid embedded structure.

## Installed implementation

`/usr/bin/binwalk` is Binwalk 2.4.3, the Python implementation of the 2.x CLI. Rust Binwalk 3.x documentation uses different options. Extraction can invoke companion utilities; a missing extractor can prevent unpacking even when the signature is correct.

## Signature scan

~~~bash
/usr/bin/binwalk "$input"
~~~

Illustrative output for an ELF file:

~~~text
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             ELF, 64-bit LSB shared object, AMD x86-64, version 1 (SYSV)
~~~

Treat the description as a hypothesis. Inspect the carved bytes or extracted structure before accepting it. Repeated or overlapping matches may be false positives or nested data; their presence alone does not distinguish those cases. For a filesystem match such as SquashFS, retain the decimal offset and reported format/version when choosing an extractor.

## Entropy and extraction

Use `/usr/bin/binwalk -E -N "$input"` for entropy analysis without a plot. High entropy can reflect compression or encryption; entropy alone cannot identify either, locate a key or prove that a signature is genuine.

On this image, the entropy path can report a Numba `TypingError` for `str2bytes` while still exiting with status zero. If that diagnostic appears, retry with `NUMBA_DISABLE_JIT=1 /usr/bin/binwalk -E -N "$input"` to disable JIT compilation for this invocation only. Check the resulting rows and remaining warnings rather than treating the exit status as proof of a completed analysis.

For extraction using the configured rules, run as an unprivileged user with read access to `input` and write access to `outdir`:

~~~bash
/usr/bin/binwalk -e "$input" -C "$outdir"
~~~

This implementation refuses extraction when launched as root without an explicit `--run-as`. If launching as root is necessary, define `extract_user` as an existing unprivileged account and use `/usr/bin/binwalk --run-as "$extract_user" -e "$input" -C "$outdir"`; ensure that account can traverse the paths and write the output. The option changes external extractor privileges, not the identity of Binwalk itself.

`-C` chooses the output base directory; without it the base is the current working directory. Binwalk normally creates an input-specific `_filename.extracted` directory underneath that base. For targeted carving without invoking an unpacker, use `/usr/bin/binwalk --dd 'squashfs:raw' -z "$input" -C "$outdir"`. The first `--dd` field is a regular expression matching descriptions, and `raw` is the carved file extension. The root `--run-as` requirement still applies to carving.

Inspect the actual output and diagnostics per selected signature. A carved blob is not an unpacked filesystem, and an absent artifact may mean no matching extraction rule, an extractor failure or a false positive. Missing companion utilities are prerequisites to report, not evidence that the image was fully extracted.
