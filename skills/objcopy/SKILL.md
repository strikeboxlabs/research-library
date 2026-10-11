---
name: objcopy
description: Extract a selected object's section bytes with GNU objcopy for offline format analysis. Use when a section must become a raw artifact and extraction must preserve the input executable.
---

# Extract one observed section

Read this entire SKILL.md before acting. Use an acquired object, an observed section name and fresh distinct destinations. Finish with status, extracted byte count and parser result or the missing-section/format limitation.

Define `binary` as the acquired absolute path, `section` as its exact selected section name, and `section_file` and `copy_file` as new separate output paths. Preserve the original fingerprint:

~~~bash
objcopy --version
umask 077
objcopy --dump-section "$section=$section_file" "$binary" "$copy_file"
~~~

The explicit object output prevents the usual in-place replacement when output is omitted. It is a rewritten object copy, not a promise of byte-identical preservation. Keep it separate from both the original and extracted raw section. Check status, stderr, section-file size and unchanged original fingerprint before accepting extraction.

The dumped bytes have no applied relocations. A missing section, unsupported object or truncated input needs a separate diagnosis; an old output file is not success. Parse the raw section using its established format. A section name resembling a signature or a matching organization string does not verify the executable's cryptographic integrity. This task does not modify deployment artifacts or attach signature sections.

See [GNU objcopy](https://sourceware.org/binutils/docs/binutils/objcopy.html) for dump-section and input/output behavior.
