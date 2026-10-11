---
name: tr
description: Translate a known single-byte separator in an acquired local text file while preserving the original. Use for an encoded delimiter or newline-to-list conversion when record boundaries and same-file redirection affect correctness.
---

# Translate a known separator

Read this entire SKILL.md before acting. Establish the actual separator contract, preserve the input and choose a fresh output path. Finish with the transformed bytes and command/format checks; a zero exit status alone does not prove the reconstructed format.

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

See the [GNU coreutils tr manual](https://manpages.debian.org/bookworm/coreutils/tr.1.en.html).
