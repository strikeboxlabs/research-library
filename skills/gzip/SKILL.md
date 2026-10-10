---
name: gzip
description: Test and decompress GNU gzip data into a selected new file without deleting its source. Use for misleading suffixes, nested compression, concatenated streams and truncated output.
---

# Recover the selected gzip stream

Read this entire SKILL.md before acting; reuse complete current context. Identify the actual gzip input and output destination, retain final integrity/decompression status and inspect the decoded object. Filename or header recognition alone cannot complete recovery.

Define `compressed` as the existing absolute input and `decoded` as a fresh absolute output in an existing private directory:

~~~bash
umask 077
gzip --version
gzip -t -- "$compressed" &&
(set -C; gzip -dc -- "$compressed" > "$decoded") &&
file -E -h -- "$decoded"
~~~

`-t` tests the stream, including integrity checks; `-d` decompresses and `-c` writes stdout while keeping the input. Stdout mode lets the input have an unusual suffix without renaming it. A single bounded `-dc` pass can save the extra test read if its final status is retained and failed output stays incomplete. Noclobber protects the new output; expansion still needs the worker's space/byte/time budget.

Ordinary file-mode `gzip -d` removes the compressed file after successful replacement unless `-k` is used. Recognized suffixes and the saved original name/time affect naming; `-N` is not needed for controlled stdout recovery. Do not add overwrite/force options merely to resolve a wrong format or collision. `-f` together with stdout can copy non-gzip input unchanged rather than prove decompression.

A failed CRC/trailer or truncated member can leave substantial decoded bytes. Keep them as partial evidence, check source acquisition and select a fresh output for a retry. Quiet or an existing output file is not success. A format error after one successful layer may mean the next object is bzip2, tar or plain data; classify that file before choosing another parser.

GNU gzip decodes concatenated members in order. This is not a tar member list, and successful concatenation does not prove that the resulting bytes were one original object. `gzip -l` is a summary, not full validation or reliable aggregate size for every multi-member/very large stream. Inspect actual decoded bytes and final status rather than treating an embedded filename as an extraction instruction.

Reference: [GNU gzip manual](https://www.gnu.org/software/gzip/manual/gzip.html); installed help resolves the actual implementation's supported options.
