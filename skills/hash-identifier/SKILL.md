---
name: hash-identifier
description: Classify the textual format of an owned checksum or digest with Blackploit Hash Identifier. Use when several algorithms share an encoding and length, and preserve candidates without claiming a proven algorithm.
---

# Classify a digest's textual form

Read this entire SKILL.md before acting. Require the installed Blackploit/Zion3R Hash Identifier implementation and the complete digest text, with its origin and encoding known where possible. Complete with the candidate list and corroborating format evidence, or the specific unresolved ambiguity. No conditional resources are required for this narrow task.

Start the interactive classifier and enter one owned checksum at its `HASH:` prompt:

~~~bash
hash-identifier
~~~

Keep the value separate from a filename, username prefix, surrounding quotes, wrapped display or trailing whitespace. Preserve the original artifact rather than silently changing case or stripping a structured format's salt/delimiters. Exit the interactive loop with Ctrl-C. The reviewed implementation also accepts its first argument as a value, but interactive input avoids placing that value in shell history and process arguments.

`Possible Hashs` and `Least Possible Hashs` are pattern candidates, not cryptographic tests or measured probabilities. For example, 128 mixed alphanumeric characters can produce SHA-512 and Whirlpool candidates even though the implementation does not strictly validate hexadecimal membership. Its ordering comes from internal identifiers. Several HMAC/plain-digest formats share the same length. A candidate cannot establish whether a salt, keyed construction or additional encoding was used.

`Not Found` means none of its rules matched. It does not prove the input is not a digest: digits-only or letters-only values, modern formats, missing bytes and formatting differences can defeat these legacy heuristics. Resolve the actual algorithm from the producer's documented format or reviewed calculation code. If that evidence is absent, finish with candidates and an unresolved algorithm rather than guessing.

Implementation and attribution: [Blackploit Hash Identifier by Zion3R](https://github.com/blackploit/hash-identifier), distinct from the `hashid` project. Use the installed program's implementation when behavior differs; do not treat a similarly named utility as equivalent.
