---
name: wc
description: Count bytes or newlines in a selected local artifact with GNU wc. Use when transfer sizes, encoded versus decoded data, or text record assumptions need an exact measured count.
---

# Count the selected artifact

Read this entire SKILL.md before acting. Select the existing regular file and the representation to count; confirm GNU coreutils with `wc --version`. No conditional resources are required. Finish with the measured count, selected input, exit status and relevant limits; a failed read is not a zero-byte file.

Define `file` as the selected path. Read it directly, without an extra text conversion:

~~~bash
LC_ALL=C wc -c < "$file"
status=$?
~~~

`-c` counts bytes; stdin redirection avoids a filename column and handles spaces or leading hyphens. Retain stderr and check `status` before accepting the count. A redirection failure can prevent `wc` from running. A file changing during the read may produce a count that differs from a later observation.

Count an encoded file and its successfully decoded output separately when comparing representations. A base64 file's length includes its whitespace; the binary output can include a format header or salt as well as payload. Block alignment alone does not identify a cipher, key size, mode or KDF. An expected byte count does not prove complete or authentic contents; use independent digest or format checks when the task requires them.

For a text task, `wc -l < "$file"` counts newline characters, so a final unterminated record is not included in that count. `-m` counts characters according to the active locale and is not a substitute for `-c` on binary data. Choose the count that answers the question instead of interpreting the default newline/word/byte columns as one value.

See the packaged [GNU wc manual](https://manpages.debian.org/bookworm/coreutils/wc.1.en.html).
