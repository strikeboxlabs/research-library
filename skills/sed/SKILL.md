---
name: sed
description: Apply a reviewed text substitution, suffix correction or removal of one confirmed final record with GNU sed. Use when regex syntax, line endings, in-place backups or successful no-op output affect the result.
---

# Make the selected transformation reviewable

Read this entire SKILL.md before acting. Select reviewed substitution, suffix correction or confirmed final-record removal below, establish the exact text change and record boundaries, preserve the input and review a separate candidate. No conditional resources are required. Finish with the changed bytes, status and verified transformation; a zero status does not prove any match occurred.

Check `sed --version` and installed help for GNU sed. Define `input` as the existing text file and `output` as a fresh distinct path. For a format that permits removal of one comma immediately before each line ending:

~~~bash
umask 077
LC_ALL=C sed 's/,$//' -- "$input" > "$output"
status=$?
~~~

The comma is literal and `$` anchors the match to the end of the current pattern space. The empty replacement removes that matched comma only. Ordinary sed processes lines without their terminating newline; this command retains the lines, including unmatched ones. It does not remove interior commas, all repeated trailing commas or a comma followed by a carriage return in CRLF input.

The **illustrative** input `alpha,beta,` becomes `alpha,beta`; `alpha,beta,,` becomes `alpha,beta,`. Review the candidate against the original with the task's text/byte comparison before using it. Removing a delimiter does not validate the list's fields, eliminate empty records or repair a truncated upstream command.

Default expressions use basic regular expressions; `-E` changes that grammar. Replacement `&` and backreferences have special meaning. Single quoting protects the shown expression from the shell; it does not make arbitrary inserted values literal sed syntax. Choose a parser or properly escaped fixed transformation for external data instead of interpolating it into a program.

Check status and stderr; a read or write failure can leave a partial candidate. A normal no-match transformation succeeds with unchanged data. Avoid same-file redirection, which truncates the input before it is read. Do not use `-i` for this review task: it changes the source and has backup/symlink semantics that differ from saving a separate result.

For an acquired sed script, review it before loading it with `-f`: sed can run commands or read/write other files through its program. GNU `--sandbox` disables those e/r/w features when supported; it does not make an arbitrary transformation correct. A short selected substitution does not need an external program.

## Apply a selected substitution

For an owned text artifact with a confirmed exact token change, define `program` as the reviewed sed expression, not arbitrary external input:

~~~bash
LC_ALL=C sed -e "$program" -- "$input" > "$output"
status=$?
~~~

The **illustrative** expression `s/OLD_TOKEN/NEW_TOKEN/g` changes every matching occurrence on each line; without `g`, only the first occurrence per line changes. Require the expected locations/count and resulting bytes before using the candidate. Global replacement can change unrelated text, comments or quoted strings. Sed is not an HTML parser: stripping tags or all whitespace does not reliably extract table columns or preserve mailbox values. Use the relevant structured parser when the selected task needs those semantics. Review an in-place change's backup/link/concurrency requirements below before replacing an original.

## Remove one confirmed final record

For a stable owned regular text file, first establish that its final line is exactly the record selected for removal. `$d` targets the last line by position; it does not identify a hosts mapping, comment or record by content. A blank final line is a different subject, and concurrent appends invalidate the selection.

Preview into a fresh distinct output:

~~~bash
LC_ALL=C sed '$d' -- "$input" > "$output"
status=$?
~~~

Review that candidate against the original and require successful reading/writing. If the approved task requires replacing this file, keep it stable, verify that `$input.bak` does not already exist and that the file is neither a symlink nor a hard-linked object, then use GNU sed's backup form:

~~~bash
LC_ALL=C sed -i.bak '$d' -- "$input"
status=$?
~~~

This changes the original pathname and keeps its previous bytes at the backup pathname; it does not commit the earlier candidate atomically with the review. In-place editing uses a replacement file and can break link identity; metadata/access-policy requirements need their own suitable update method. Check status, the backup and actual resulting content before acceptance. A failure can leave partial/replacement state; inspect before retrying. Preserve the backup for the task's recovery decision. Do not delete the final line of a shared system configuration merely because a walkthrough appended its own record there earlier.

Reference: [GNU sed packaged manual](https://manpages.debian.org/bookworm/sed/sed.1.en.html); consult its fuller manual when selecting a different transformation.
