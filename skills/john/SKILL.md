---
name: john
description: Run bounded offline checks with John the Ripper Jumbo on NT, NetNTLMv2, Kerberos, ZIP, KeePass, OpenPGP secret keys, bcrypt, phpass, raw MD5/SHA-256, sha512crypt or HS256 JWT artifacts. Use to choose formats, preserve records and interpret session results.
---

# John the Ripper offline checks

Read this entire SKILL.md before acting. Select the actual artifact/format and any applicable converter below before the bounded run. Preserve full records, use the same private pot for recovery display, and finish with loaded count/termination and supported recovery evidence. A missing conversion/key component or failed load is unresolved, not a negative password result.

Check the installed build: these formats/options assume Jumbo. Inspect `john --list=build-info` and `john --list=formats`; a core-only package may not support the task. Use an existing hash artifact, not an account login endpoint.

Choose `format` from the artifact's origin and verified parser:

| Input | Format decision |
|---|---|
| Local SAM NT hash or supported pwdump records | `NT`; distinguish the NT field from LM and NetNTLMv2 data. |
| AS-REP encrypted reply material | `krb5asrep`; retain the complete record in a representation accepted by that build. |
| Service-ticket material | A different Kerberos format; do not reuse `krb5asrep` merely because both are Kerberos. |
| Captured NTLMv2 challenge/response | `netntlmv2`; keep the complete username/domain/challenge/response record, not just an NT hash field. |
| Unsalted MD5 established from the producing application | `Raw-MD5`; 32 hex characters also fit other formats and do not distinguish MD5 from NT. |
| Unsalted SHA-256 established from the producing application | `raw-sha256`; 64 hex characters alone do not identify it. |
| Original compact JWT using confirmed HS256 | `HMAC-SHA256` in a Jumbo build supporting JWT input. |
| Complete application bcrypt record such as `$2b$12$...` | `bcrypt` when supported by the installed build; preserve the revision, cost, salt and checksum. Cost 12 represents 4096 iterations, not twelve candidate attempts. |
| Complete `$6$` password verifier from a selected SSSD/Linux record | `sha512crypt` in a supporting Jumbo build; retain its salt, optional rounds and checksum plus the original account mapping. |
| Complete portable phpass `$P$...` or `$H$...` record | `phpass`; preserve its cost, salt and checksum. An application's name alone does not establish this format. |

For a Jenkins password field beginning with `#jbcrypt:`, that exact prefix is application metadata. Remove only the marker in a working record and retain the complete 60-character bcrypt value, including revision, cost, salt and checksum. XML/display wrapping and diagnostic suffixes are not hash bytes; verify the original field rather than guessing missing characters from a screenshot. Other Jenkins encoders exist, including PBKDF2 in FIPS mode, so the application name alone does not justify `--format=bcrypt`. See the [password encoder implementation](https://github.com/jenkinsci/jenkins/blob/master/core/src/main/java/hudson/security/HudsonPrivateSecurityRealm.java) when the stored field differs.

For raw MD5 exported from a database, preserve the row-to-account association and select the actual digest field. A reviewed `username:digest` record can retain a simple label; replacing every pipe in an arbitrary table dump can corrupt fields or pass unrelated columns to the loader. Parse the export and validate the intended fields first. When provenance cannot resolve a 32-hex value, a narrowly budgeted `Raw-MD5` run may test an explicit format hypothesis; keep that uncertainty separate from a candidate matching this interpretation, and verify any requested application/OS use separately. Use the bounded run and matching `--show` below with `format=Raw-MD5`; compare loaded records and prior pot results before interpreting a count discrepancy. See the [Jumbo raw MD5 implementation](https://github.com/openwall/john/blob/bleeding-jumbo/src/rawMD5_fmt_plug.c) for accepted encodings.

For an SSSD `cachedPassword` `$6$` value, recover the complete attribute through LDIF parsing, including folded/base64 forms and DN/name association. A nearby `strings` username is insufficient to assign ownership. Use `format=sha512crypt` with the bounded command below; a match establishes this offline cached verifier, which can be stale. GSSAPI authentication does not necessarily cache a password, and neither a cache filename nor recovery proves present AD login access. See [Jumbo sha512crypt parser](https://github.com/openwall/john/blob/bleeding-jumbo/src/sha512crypt_fmt_plug.c).

For HS256, retain the original `header.payload.signature` token on one line, without a Bearer prefix. Re-serializing decoded JSON changes the signed bytes. This checks candidate HMAC secrets offline; it does not test arbitrary JWT algorithms or establish that a service still accepts the token. Check parser limits on rejection instead of changing its contents. Keep private password records/tokens out of public hash-identification services.

For an encrypted ZIP, define `archive` as an intact working copy and `hashes`/`conversion_log` as fresh private files. The Jumbo `zip2john` helper converts the archive; stdout and diagnostics must stay separate:

~~~bash
umask 077
zip2john "$archive" >"$hashes" 2>"$conversion_log"
~~~

Inspect the converter's record type and installed formats before choosing `format`: traditional PKZIP and WinZip AES use different parsers. Preserve full output, including filename/colon fields, and retain the archive because some records refer back to it. No usable record can mean unencrypted entries, unsupported encryption or damaged input. Verify any recovered candidate by testing/decrypting the relevant archive entries; different entries can use different passwords.

For a KeePass database whose master key includes a key file, define `database` and `keyfile` as intact acquired copies, with fresh private `hashes` and `conversion_log` outputs:

~~~bash
umask 077
keepass2john -k "$keyfile" "$database" >"$hashes" 2>"$conversion_log"
~~~

Omit `-k` only for a password-only database. A saved configuration association is a lead; it can be stale. An arbitrary key file, including a PNG, contributes its exact bytes: opening and re-saving the image can change the key without visibly changing the picture. Compare transfer digests before testing candidates. Missing key components cannot be repaired by trying more passwords.

Inspect diagnostics and require a complete record accepted by the installed KeePass format. Converter exit zero alone is insufficient; unsupported input can produce diagnostics without a usable record. KDBX version, KDF and key-file support depend on the installed Jumbo build. Use `format=keepass` only when that format accepts the converted record. Confirm any recovered password by opening a copy with the same key components in a compatible KeePass reader. An exhausted wordlist can also reflect the wrong key file; it does not prove the database has no recoverable password.

For a passphrase-protected OpenPGP secret key, define `key` as one complete acquired key file, with fresh `hashes` and `conversion_log` paths:

~~~bash
umask 077
gpg2john "$key" >"$hashes" 2>"$conversion_log"
~~~

Require a usable `$gpg$` record and set `format=gpg` only if the installed Jumbo build accepts it. Preserve converter labels and the complete record. A public key, unprotected secret key, incomplete armor or unsupported packet/cipher can leave no usable record; a larger wordlist cannot fix that. `gpg2john -S` includes subkeys when those are relevant; keep their records associated with the original key and do not assume all packets use the same passphrase.

If armor came from JSON in a browser-storage artifact, decode the actual string field using its serialization format. A `strings | grep` hit may be truncated, escaped or stale; replacing every backslash sequence globally can corrupt it. Preserve the armor headers, body and footer in a separate working file. A recovered candidate unlocks the corresponding secret-key material; it is not a login password or proof of permission to recover an online account. Confirm against that key copy in an appropriate offline reader before drawing a recovery conclusion.

Define `hashes` and `wordlist` as existing absolute paths, `pot` as a private case-specific pot file, and `session` as a unique session name/path. Choose `seconds` for the task's time budget:

~~~bash
umask 077
john --format="$format" --wordlist="$wordlist" --pot="$pot" --session="$session" --max-run-time="$seconds" "$hashes"
john --show --format="$format" --pot="$pot" "$hashes"
~~~

The pot stores recovered values and suppresses repeated work. Reuse the same format/pot for `--show`. `john --restore="$session"` resumes saved state; do not silently launch an unlimited default attack when a bounded wordlist run ends.

On Unix, optional `--fork=N` creates N processes, not N threads. Formats using OpenMP can add threads per process; budget their combined CPU/memory use instead of copying a walkthrough's process count. Keep the same bounded candidate/time scope. Restore using the saved session, without adding `--fork` again; its recorded settings include the child sessions.

`No password hashes loaded` suggests a format/build/input problem. Check wrapped lines, copied banners and parser compatibility. `No password hashes left to crack` can mean results already exist in the pot; inspect `--show`. A completed wordlist with no recovery says only that the tested candidates failed. A timed-out run is incomplete. Record loaded count, chosen format, candidate source and termination condition; recovered values need not appear in the user-facing report.

Consult the [OpenPGP converter](https://github.com/openwall/john/blob/bleeding-jumbo/src/gpg2john.c) for packet support and [Jumbo options](https://github.com/openwall/john/blob/bleeding-jumbo/doc/OPTIONS) for session controls, the [KeePass converter](https://github.com/openwall/john/blob/bleeding-jumbo/src/keepass2john.c) for installed-format differences, and [KeePass key components](https://keepass.info/help/base/keys.html) when recovery requires more than a password.

For bcrypt revision/cost parsing, consult the installed build and upstream [bcrypt format implementation](https://github.com/openwall/john/blob/bleeding-jumbo/src/BF_fmt.c). A recovered candidate matches that offline record; it does not establish current application login access.
