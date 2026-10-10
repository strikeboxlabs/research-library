---
name: username-anarchy
description: Generate username candidates from known names using username-anarchy format plugins. Use to prepare a bounded candidate list while preserving compound names and distinguishing guessed identifiers from verified accounts.
---

# Preserve names and choose candidate formats

Read this entire file before acting. Choose formats using known naming evidence. Finish with the candidate file, input assumptions and selected formats; generation does not verify account existence.

Set `tool` to the installed executable script; use its verified Ruby interpreter invocation if it is not executable. Inspect its supported plugins:

~~~bash
"$tool" --list-formats
"$tool" --input-file "$names_file" --select-format 'flast,lfirst,f.last' > "$candidates_file"
~~~

The three formats are examples, not a universal organization standard. Define the two file paths first. Supported input includes CSV or tabular name fields; retain complete surnames, initials and missing-field distinctions. Do not extract only the first two whitespace-separated tokens from a full-name field and assume that preserves every name. Check a few generated rows against the actual input before using the full list.

For one person's known first and last names, positional arguments can produce candidate variants:

~~~bash
"$tool" 'Alex' 'Example'
~~~

Those names are illustrative. Case folding, punctuation removal and truncation can collapse distinct people into the same candidate. Deduplicate only after preserving the input-to-candidate relationship needed for the task. Keep an observed directory username as stronger evidence than any generated variant.

An empty or implausible output calls for input-format and plugin checks, not automatic generation of a huge global name list. Candidate generation is offline; later account enumeration or authentication has its own scope and result interpretation. Review [upstream formats and input examples](https://github.com/urbanadventurer/username-anarchy) when a name structure is ambiguous.
