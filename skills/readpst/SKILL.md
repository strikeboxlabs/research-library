---
name: readpst
description: Convert a local Outlook PST into searchable mail files on Linux using readpst. Use when examining exported mail without Outlook and when conversion filters or MIME encoding may hide relevant content.
---

# Readpst mail extraction

Define `pst` as the original PST's absolute path and `destination` as a new output directory. For email inspection with one `.eml` file per message:

~~~bash
readpst -V
mkdir -m 700 "$destination" && readpst -e -t e -o "$destination" "$pst"
~~~

`-o` requires an existing directory. `-e` keeps message boundaries; attachments remain MIME parts inside messages. `-t e` selects email only. Omit the type filter when appointments, contacts or journals matter. The walkthrough's `-t ea` includes email and appointments; `-m` also generates `.msg` output and is unnecessary for ordinary text review.

Inspect conversion errors and the generated folder tree before searching. Plain-text search is useful triage, but MIME transfer encodings, HTML and attachments can hide text. Use an email/MIME parser for relevant messages; retain folder, message headers, dates and source identity with any excerpt. A subject or isolated line is not enough to interpret a conversation.

An old message mentioning a credential is historical evidence, not a successful current login. No search matches may reflect the selected item types or conversion failure. Deleted items need an explicit `-D` pass if relevant; they are not included by default. Use a separate output directory for another pass. Avoid `-w`: with `-S`, it can remove existing destination files.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Access PDF p. 7. Maintenance source: upstream [readpst manual, libpst 0.6.76](https://www.five-ten-sg.com/libpst/rn01re01.html).
