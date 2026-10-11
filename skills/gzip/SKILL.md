---
name: gzip
description: Create, test or decompress GNU gzip streams while preserving the selected source. Use for log compression, misleading suffixes, nested members and partial output.
---

# Recover the selected gzip stream

Read this entire SKILL.md before acting; reuse complete current context. Select recovery below or source-preserving compression in the final section, establish input/output paths, and retain final status and artifact checks. Filename or header recognition alone cannot complete either task.

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

## Compress one selected file without replacing it

Define `input` as the selected readable regular file and `compressed` as a fresh absolute output beneath an owned private directory, distinct from the input. Use a stable snapshot when complete log coverage matters:

~~~bash
umask 077
(set -C; gzip -c -- "$input" > "$compressed")
status=$?
~~~

Check status/stderr, then `gzip -t -- "$compressed"`; keep a failed result marked incomplete. Stdout compression preserves the original. Shell redirection creates the new object's permissions and opens it before gzip reads; it does not preserve the input's filesystem owner/mode. Noclobber prevents replacing an existing ordinary file. Never redirect onto the input or an alias.

A growing or rotated log can change during reading. Compression does not select yesterday's records, rotate/delete the log or make a consistent application snapshot; a date in the output filename is only a label. Successful integrity checking establishes a valid stream, not expected contents or input completeness. Confirm decoded bytes against the selected stable snapshot when required. GNU gzip reports 1 for error and 2 for warning; inspect nonzero results rather than accepting the existence of a .gz file.

Reference: [GNU gzip manual](https://www.gnu.org/software/gzip/manual/gzip.html) and [packaged options/status](https://manpages.debian.org/bookworm/gzip/gzip.1.en.html); installed help resolves the actual implementation's supported options.
