---
name: tr
description: Translate a known single-byte separator or remove confirmed line terminators from an acquired local field while preserving the original. Use when record boundaries, CRLF or same-file redirection affect correctness.
---

# Translate a known separator

Read this entire SKILL.md before acting. Select separator translation or the single-field unwrapping below, establish its actual byte contract, preserve the input and choose a fresh output path. Finish with the transformed bytes and command/format checks; a zero exit status alone does not prove the reconstructed format.

Check `tr --version` for GNU coreutils. Define `input` as the acquired local file and `output` as a distinct fresh path that does not alias it. For a contract that uses literal dollar bytes as line separators:

~~~bash
umask 077
LC_ALL=C tr '$' '\n' < "$input" > "$output"
status=$?
~~~

This replaces every dollar byte with a newline. It does not decode backslash-n text, parse fields or understand quoting. Use it only when genuine data cannot contain that separator. The C locale makes the operation byte-oriented; it is not Unicode case conversion.

For an acquired, already validated one-value-per-line list that cannot contain embedded newlines or commas, the opposite framing task is:

~~~bash
LC_ALL=C tr '\n' ',' < "$input" > "$output"
status=$?
~~~

Every newline becomes a comma, including the final terminator. Empty records produce adjacent commas, and an unterminated final record produces no trailing comma. Inspect that framing before deliberately removing a trailing delimiter. This is not CSV serialization or a completeness check on the producing command. Command substitution can also change trailing-newline handling; preserve a file when exact bytes matter.

Do not redirect output to the input file or an alias: the shell opens/truncates the destination before tr reads it. Check status and retain an incomplete output on failure as such. Translation sets are character arrays, not strings to substitute; `-d` deletes and `-s` squeezes repetitions, so neither belongs in this one-for-one transformation.

Compare the expected separators, line endings and format against the preserved input before handing the new file to a parser. For this byte-for-byte replacement, output length should equal input length; length alone cannot establish correctness. Keep the original until that check completes.

## Remove line wrapping from one complete field

Use this only when the acquired input is one complete textual field whose format explicitly treats the observed newlines as transport wrapping. It must exclude banners, diagnostics and other records. With the same preserved input and fresh output:

~~~bash
LC_ALL=C tr -d '\n' < "$input" > "$output"
status=$?
~~~

This deletes every LF byte, including a final terminator; it leaves CR bytes intact. For confirmed CRLF wrapping, select `tr -d '\r\n'` instead. Neither operation removes the literal characters backslash and n. Deleting all whitespace would also change spaces/tabs that can belong to the field.

Check status and the recovered field's own length/alphabet/parser contract. Joining lines does not validate producer success, repair omitted bytes or establish that every line belonged to one field. Prefer a captured file with the producer's status and separate stderr over a pipeline that merges unrelated output. A zero-length input succeeds and is not evidence of a complete field.

See the [GNU coreutils tr manual](https://manpages.debian.org/bookworm/coreutils/tr.1.en.html).
