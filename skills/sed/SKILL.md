---
name: sed
description: Apply a selected small text substitution to a preserved local file with GNU sed. Use for an anchored suffix correction where regex syntax, line endings or successful no-op output affect the result.
---

# Make the selected transformation reviewable

Read this entire SKILL.md before acting. Establish the exact intended text change and record boundaries, preserve the input and write a separate candidate. No conditional resources are required. Finish with the changed bytes, status and verified transformation; a zero status does not prove any match occurred.

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

Reference: [GNU sed packaged manual](https://manpages.debian.org/bookworm/sed/sed.1.en.html); consult its fuller manual when selecting a different transformation.
