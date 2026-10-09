---
name: readpst
description: Convert local Outlook PST or supported OST files into searchable mail on Linux using readpst. Use when conversion errors, item filters, MIME encoding or image attachments may hide relevant content.
---

# Readpst mail extraction

Define `pst` as the source PST's absolute path (or an OST format supported by the installed libpst) and `destination` as a new output directory. For email inspection with one `.eml` file per message:

~~~bash
readpst -V
mkdir -m 700 "$destination" && readpst -e -t e -o "$destination" "$pst"
~~~

`-o` requires an existing directory. `-e` keeps message boundaries; attachments remain MIME parts inside messages. `-t e` selects email only. Omit the type filter when appointments, contacts or journals matter. The walkthrough's `-t ea` includes email and appointments; `-m` also generates `.msg` output and is unnecessary for ordinary text review.

Inspect conversion errors and the generated folder tree before searching. Plain-text search is useful triage, but MIME transfer encodings, HTML and attachments can hide text. Use an email/MIME parser for relevant messages; retain folder, message headers, dates and source identity with any excerpt. A subject or isolated line is not enough to interpret a conversation.

Libpst includes support for the Outlook 2013-era 64-bit OST layout; that does not establish compatibility with every OST. An unsupported/truncated file and a successfully converted mailbox with no matches are different outcomes. Relevant image attachments need visual inspection or checked OCR; searching `.eml` text cannot find words drawn inside an image. Preserve the attachment-to-message mapping and verify ambiguous characters against the image.

An old message mentioning a credential is historical evidence, not a successful current login. No search matches may reflect the selected item types or conversion failure. Deleted items need an explicit `-D` pass if relevant; they are not included by default. Use a separate output directory for another pass. Avoid `-w`: with `-S`, it can remove existing destination files.

Documentation reviewed 2026-10-09; Linux execution untested. Cases: Access p. 7; Arkham pp. 14–15. Sources: upstream [readpst manual, libpst 0.6.76](https://www.five-ten-sg.com/libpst/rn01re01.html), [libpst file layouts](https://www.five-ten-sg.com/libpst/devel/structpst__file.html).
