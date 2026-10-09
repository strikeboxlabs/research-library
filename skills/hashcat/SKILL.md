---
name: hashcat
description: Select Hashcat modes and run bounded offline wordlist checks on NT/Kerberos records or Password Safe v3 files. Use when input formats, potfile behaviour, backend failures or exhausted runs need interpretation.
---

# Hashcat offline checks

Match the input representation to the mode, using its acquisition context and the installed version's examples. A 32-character hexadecimal string alone does not identify its algorithm.

| Known artifact | Mode |
|---|---|
| Raw NT hash from a SAM account | `1000` |
| Apache `$apr1$...` record from htpasswd | `1600`; not raw MD5 mode `0`. |
| `$krb5tgs$23$...` service-ticket material | `13100` |
| `$krb5asrep$23$...` AS-REP material | `18200` |

AES Kerberos records use different modes. Preserve each complete text record on one line; avoid shell expansion of `$` and PDF line wrapping. A full `username:RID:LM:NT:::` record is not a raw NT hash; extract the NT field into a separate working file and retain its account mapping. For htpasswd, separate the username from the complete `$apr1$` value and remove any HTML presentation wrapper; do not hash the rendered page or discard the salt.

Inspect `hashcat --version` and `hashcat -I` for backend/device availability. Define `mode` from the table or verified examples, `hashes` and `wordlist` as existing absolute paths, `pot` as a private case-specific file, `session` as a unique name, and `seconds` as the time budget:

~~~bash
umask 077
hashcat -m "$mode" -a 0 "$hashes" "$wordlist" --potfile-path "$pot" --session "$session" --runtime "$seconds" --status
hashcat -m "$mode" "$hashes" --show --potfile-path "$pot"
~~~

Use the same mode and pot when showing results. An existing pot can explain an immediate already-recovered result. Keep it instead of discarding recovery evidence with `--potfile-disable`.

**Password Safe v3 is a different input path.** Mode `5200` consumes the binary database itself, not an extracted text hash. Define `database` as its intact working copy and `recovered` as a fresh private output file; retain the database-to-output mapping:

~~~bash
hashcat -m 5200 -a 0 "$database" "$wordlist" --session "$session" --runtime "$seconds" --status --outfile "$recovered" --outfile-format 2
~~~

The reviewed 5200 module disables potfile support, so the pot/`--show` procedure above does not apply. Preserve the explicit output and final status. Verify a recovered candidate by opening a copy with a compatible Password Safe client. File-size/signature errors call for checking binary transfer and format/version, not treating the file as line-based hashes.

`Token length exception` or `Separator unmatched` usually calls for checking the mode and record representation, not a bigger wordlist. Fix reported backend/self-test failures before trusting a run; do not copy a walkthrough's `--force` as a routine solution. `Exhausted` means the selected candidate space was tried, not that the password is strong. Runtime aborts and skipped/rejected candidates limit coverage. Capture status, tested inputs and recovery count without reproducing secrets unnecessarily.

Documentation reviewed 2026-10-09; Linux execution untested. Cases: Active p. 9; Administrator pp. 7, 10; Alert p. 11. Sources: [mode examples](https://hashcat.net/wiki/doku.php?id=example_hashes), [CLI options/statuses](https://hashcat.net/wiki/doku.php?id=hashcat), [Password Safe v3 module](https://github.com/hashcat/hashcat/blob/master/src/modules/module_05200.c), [Apache APR1 module](https://github.com/hashcat/hashcat/blob/master/src/modules/module_01600.c).
