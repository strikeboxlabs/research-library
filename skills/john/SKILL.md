---
name: john
description: Run bounded offline checks with John the Ripper Jumbo on NT, NetNTLMv2, Kerberos, ZIP, raw SHA-256 or HS256 JWT artifacts. Use to choose formats, preserve records and interpret session results.
---

# John the Ripper offline checks

Check the installed build: these formats/options assume Jumbo. Inspect `john --list=build-info` and `john --list=formats`; a core-only package may not support the task. Use an existing hash artifact, not an account login endpoint.

Choose `format` from the artifact's origin and verified parser:

| Input | Format decision |
|---|---|
| Local SAM NT hash or supported pwdump records | `NT`; distinguish the NT field from LM and NetNTLMv2 data. |
| AS-REP encrypted reply material | `krb5asrep`; retain the complete record in a representation accepted by that build. |
| Service-ticket material | A different Kerberos format; do not reuse `krb5asrep` merely because both are Kerberos. |
| Captured NTLMv2 challenge/response | `netntlmv2`; keep the complete username/domain/challenge/response record, not just an NT hash field. |
| Unsalted SHA-256 established from the producing application | `raw-sha256`; 64 hex characters alone do not identify it. |
| Original compact JWT using confirmed HS256 | `HMAC-SHA256` in a Jumbo build supporting JWT input. |

For HS256, retain the original `header.payload.signature` token on one line, without a Bearer prefix. Re-serializing decoded JSON changes the signed bytes. This checks candidate HMAC secrets offline; it does not test arbitrary JWT algorithms or establish that a service still accepts the token. Check parser limits on rejection instead of changing its contents. Keep private password records/tokens out of public hash-identification services.

For an encrypted ZIP, define `archive` as an intact working copy and `hashes`/`conversion_log` as fresh private files. The Jumbo `zip2john` helper converts the archive; stdout and diagnostics must stay separate:

~~~bash
umask 077
zip2john "$archive" >"$hashes" 2>"$conversion_log"
~~~

Inspect the converter's record type and installed formats before choosing `format`: traditional PKZIP and WinZip AES use different parsers. Preserve full output, including filename/colon fields, and retain the archive because some records refer back to it. No usable record can mean unencrypted entries, unsupported encryption or damaged input. Verify any recovered candidate by testing/decrypting the relevant archive entries; different entries can use different passwords.

Define `hashes` and `wordlist` as existing absolute paths, `pot` as a private case-specific pot file, and `session` as a unique session name/path. Choose `seconds` for the task's time budget:

~~~bash
umask 077
john --format="$format" --wordlist="$wordlist" --pot="$pot" --session="$session" --max-run-time="$seconds" "$hashes"
john --show --format="$format" --pot="$pot" "$hashes"
~~~

The pot stores recovered values and suppresses repeated work. Reuse the same format/pot for `--show`. `john --restore="$session"` resumes saved state; do not silently launch an unlimited default attack when a bounded wordlist run ends.

`No password hashes loaded` suggests a format/build/input problem. Check wrapped lines, copied banners and parser compatibility. `No password hashes left to crack` can mean results already exist in the pot; inspect `--show`. A completed wordlist with no recovery says only that the tested candidates failed. A timed-out run is incomplete. Record loaded count, chosen format, candidate source and termination condition; recovered values need not appear in the user-facing report.

Documentation reviewed 2026-10-09; Linux execution untested. Cases: Absolute p. 6; Acute p. 16; Anubis p. 10; APT p. 7; Awkward pp. 8–9, 14–15. Sources: [Jumbo options](https://github.com/openwall/john/blob/bleeding-jumbo/doc/OPTIONS), [AS-REP parser](https://github.com/openwall/john/blob/bleeding-jumbo/src/krb5_asrep_fmt_plug.c), [usage examples](https://www.openwall.com/john/doc/EXAMPLES.shtml), [ZIP converter](https://github.com/openwall/john/blob/bleeding-jumbo/src/zip2john.c), [NetNTLMv2 parser](https://github.com/openwall/john/blob/bleeding-jumbo/src/NETNTLMv2_fmt_plug.c), [raw SHA-256](https://github.com/openwall/john/blob/bleeding-jumbo/src/rawSHA256_fmt_plug.c), [HMAC/JWT parser](https://github.com/openwall/john/blob/bleeding-jumbo/src/hmacSHA256_fmt_plug.c).
