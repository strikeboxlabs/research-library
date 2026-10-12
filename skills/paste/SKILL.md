---
name: paste
description: Join acquired line records into a delimiter-separated line with GNU paste. Use when serial versus parallel merging, blank records or retained carriage returns change a generated argument list.
---

# Join the selected records

Read this entire SKILL.md before acting. Require the complete selected text records, their known boundaries and the consumer's delimiter contract. All instructions are inline. Finish with paste's status and the exact joined records; incomplete producer output cannot become a complete inventory through joining.

Define `records` as the existing one-record-per-line file and `joined` as a fresh output path. For one comma-separated line:

~~~bash
paste --version
paste -s -d ',' -- "$records" > "$joined"
status=$?
~~~

Inspect status, stderr and the produced bytes. `-s` processes each file serially, replacing its intervening line separators with the selected delimiter and retaining a final output newline. Multiple input files produce separate joined lines. Without -s, paste merges corresponding lines from its inputs instead.

This is record joining, not validation or CSV escaping. Blank input records remain empty fields; a comma within a record remains ambiguous, and CRLF input can retain carriage returns. Verify that the selected consumer actually wants this representation. For a service-port list, filter and validate complete protocol/state/port records before joining; finding a word such as open in a partial scan is not that validation. Keep producer errors and coverage separately from paste's result.

With several delimiter characters, paste cycles through them rather than treating the string as a multi-character separator. An empty source and an unreadable file are different outcomes. Do not pass an unexamined joined line onward as executable shell text.

Reference: [GNU paste serial/delimiter behavior](https://manpages.debian.org/bookworm/coreutils/paste.1.en.html).
