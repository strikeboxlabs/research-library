---
name: hashid
description: Identify candidate hash formats offline and obtain Hashcat or John format hints. Use when a captured value has an uncertain encoding, several possible algorithms or an unrecognized bcrypt prefix.
---

# Identify a candidate format

Read this entire SKILL.md before acting. Preserve the original record, identify candidate formats and corroborate their meaning with the producer/receiving parser. Finish with candidate evidence and unresolved ambiguity; a label is not verification of the algorithm or password.

Check `hashid --version` and `hashid -h`. HashID compares strings with patterns; it does not verify a digest against a password or prove which application produced it. Preserve the complete original record, including prefix, salt, cost and separators. Separate database labels or framework wrappers only when their meaning is known.

Define `hashes` as an existing text file containing one complete record per line and `report` as a fresh private output path:

~~~bash
umask 077
hashid -m -j <"$hashes" >"$report"
~~~

`-m` adds Hashcat mode hints and `-j` adds John format names. Reading through stdin makes a missing file a shell error; a nonexistent positional filename can otherwise be treated as a literal hash. The report echoes input values, so it can contain sensitive authentication material.

Interpret candidate lists with the producing application's schema and encoding. **Illustrative:** a bcrypt-shaped record can return `Blowfish(OpenBSD)`, `Woltlab Burning Board 4.x` and `bcrypt`. These labels do not establish three independent algorithms or identify the application. Similarly, a 32-character hexadecimal value alone cannot distinguish MD5 from NTLM or several other formats. Validate the chosen format with the receiving tool's parser and the producer's documentation before spending an audit budget on it.

An `Unknown hash` result is not proof of corruption or a novel algorithm. The upstream bcrypt pattern recognizes `$2a$`, `$2x$` and `$2y$`, but omits `$2b$`; a valid `$2b$` record may therefore be missed. Check the installed version and actual format support; do not rewrite the stored prefix just to make an identifier accept it. Extended mode `-e` widens candidates, not confidence.

Inspect the report as well as process status: upstream can print `Unknown hash` and still exit normally. Truncation, line wrapping, a username prefix or a database encoding can explain a mismatch. Retain the original bytes and resolve those conditions before selecting a recovery format.

Use the [HashID usage and examples](https://github.com/psypanda/hashID) and [recognition patterns](https://github.com/psypanda/hashID/blob/master/hashid.py) to investigate unsupported inputs.
