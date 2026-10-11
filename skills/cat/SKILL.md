---
name: cat
description: Read a selected acquired plaintext file with GNU cat and preserve unfiltered configuration evidence. Use when grep excerpts, presentation markers or read errors could be mistaken for complete effective policy.
---

# Read the selected text without dropping context

Read this entire SKILL.md before acting. Require the intended ordinary plaintext file and a display/capture suitable for its size and sensitivity. No conditional resources are required. Finish with complete output or the explicit read/capture gap; reading configuration does not establish that a service loaded it.

Confirm `cat --version` for GNU coreutils. Define `input` as the selected existing regular text file:

~~~bash
cat -- "$input"
status=$?
~~~

Preserve stderr and inspect status. A read failure can leave partial output; a terminal/tool capture can truncate successful output. Use a private fresh capture when the file exceeds the available display, never redirect onto the input or an alias. Unknown binary/device/FIFO inputs require their appropriate reader instead of this text procedure. Cat with no file reads standard input, potentially waiting; an empty path argument is different.

Keep full configuration context before applying a keyword filter: a matching line can be commented, inherited, overridden or for a different class. A snippet mentioning an authentication method does not establish effective policy for every account/service. Follow includes, class selection and the deployed process's configuration without changing authentication data.

When diagnosing text presentation, `cat -n -- "$input"` numbers all lines and `cat -vET -- "$input"` makes common control/tab/end markers visible. Those modes transform the display; `^I`, `^M` and end-of-line `$` markers are not literal original text and must not be copied back as configuration. A successful read establishes readable bytes at that time, not provenance, credential validity or policy enforcement.

Reference: [GNU cat manual](https://www.gnu.org/software/coreutils/manual/html_node/cat-invocation.html).
