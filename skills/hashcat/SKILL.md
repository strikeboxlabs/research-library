---
name: hashcat
description: Select Hashcat modes and run bounded offline checks on application or NT/Kerberos records, Password Safe v3 files and LUKS1 images. Use when Grafana/Gitea PBKDF2 or salted SHA-1 conversion, binary inputs, potfile exceptions or exhausted runs need interpretation.
---

# Hashcat offline checks

Read this entire SKILL.md before acting; complete current context need not be re-read. Complete the applicable input checks before a bounded run; preserve status and report recovered, exhausted or incomplete honestly.

- Historical Grafana SQLite rows, literal salts or hardcoded converter cost: read [Grafana PBKDF2](references/grafana-pbkdf2.md) fully before conversion or full-verifier confirmation.
- Required for Gitea PBKDF2: read [record conversion](references/gitea-pbkdf2.md) before preparing input; use its parameter-preserving converter for the supported format.
- Required for Password Safe/LUKS1: read [binary containers](references/binary-containers.md) before choosing input or reporting recovery; the ordinary potfile procedure does not apply.
- For salted MD5/SHA-1 or a legacy OFBiz `$SHA$` record, read [salted digest formats](references/salted-digests.md) before conversion or salt encoding.
- For a MySQL/MariaDB native-password record, read [native-password input](references/mysql-native-password.md) before removing storage wrappers or choosing mode 300.
- Otherwise select the supported format below, then follow its interpretation and bounded run. Leave unrelated references unloaded; missing format parameters prevent a justified mode choice.

Match the input representation to the mode, using its acquisition context and the installed version's examples. A 32- or 40-character hexadecimal string alone does not identify its algorithm or salt handling.

| Known artifact | Mode |
|---|---|
| Raw NT hash from a SAM account | `1000` |
| Complete NetNTLMv2 `user::domain:challenge:response:blob` exchange | `5600`; retain all fields, not just the response hex. |
| Complete md5crypt `$1$salt$checksum` record | `500`; retain the prefix, salt and checksum, not the surrounding SQLite row. Different from raw MD5 `0` and Apache APR1 `1600`. |
| Complete sha512crypt `$6$[rounds=N$]salt$checksum` record | `1800`; retain optional rounds, salt and checksum. Not raw SHA-512 or an NT hash. |
| Apache `$apr1$...` record from htpasswd | `1600`; not raw MD5 mode `0`. |
| Drupal 7 `$S$...` password record | `7900` |
| Complete supported bcrypt `$2...` record | `3200` |
| Verified MySQL 4.1-style `mysql_native_password` record | `300`; prepare its storage representation as described in the linked native-password reference. Not single SHA-1. |
| Confirmed unsalted SHA-1 | `100`; raw hexadecimal digest. |
| Verified SHA-1 of password bytes followed by salt bytes | `110`; `hex_digest:literal_salt`, preserving the actual salt bytes. |
| Verified SHA-1 of salt bytes followed by password bytes | `120`; use the linked salted-digest procedure. |
| Raw MD5 established from the producing application | `0`; length alone is insufficient. |
| Verified MD5 of salt bytes followed by password bytes | `20`; `hex_digest:literal_salt`. |
| Verified MD5 of password bytes followed by salt bytes | `10`; same record layout, different digest computation. |
| Complete portable phpass `$P$...` or `$H$...` record | `400`; an application's name alone does not establish the format. |
| Verified PBKDF2-HMAC-SHA256 encoded as `sha256:iterations:base64_salt:base64_digest` | `10900`; preserve the actual cost and byte encodings. |
| Converted Ansible Vault `$ansible$...` record | `16900`; not the raw YAML or `$ANSIBLE_VAULT` file. |
| `$krb5tgs$23$...` service-ticket material | `13100` |
| `$krb5asrep$23$...` AS-REP material | `18200` |
| Verified `$krb5pa$18$...` AES256 encrypted-timestamp pre-authentication record | `19900`; not an AS-REP or service-ticket record. |

For an SSSD cache, first associate the value with its structured user record and attribute. A `$6$` verifier can use mode `1800`; a string found somewhere in the file does not identify its account. Check the [sha512crypt module](https://github.com/hashcat/hashcat/blob/master/src/modules/module_01800.c) for the complete representation. Recovery confirms a candidate against that cached verifier, not a current directory password, account access, NTLM pass-the-hash material or a Kerberos ticket.

A Responder NTLMv2-SSP capture is challenge-response material, not a raw NT hash. Keep its username/domain inside the complete record; those fields are part of mode `5600` input, not a removable display label. Truncated blobs and copied log prefixes are malformed inputs. See the [NetNTLMv2 module and self-test format](https://github.com/hashcat/hashcat/blob/master/src/modules/module_05600.c).

For mode `19900`, confirm that the ciphertext came from PA-ENC-TIMESTAMP in an AS-REQ and that its own encryption type is 18. Preserve the full converter record and principal association. The [mode 19900 implementation](https://github.com/hashcat/hashcat/blob/master/src/modules/module_19900.c) distinguishes default AD user salt derivation from explicit-salt input; supported layouts vary by release. Do not invent a realm, change username case or discard a nondefault salt to make the loader accept a line. Compare installed examples and the converter's format before a bounded run. A successfully loaded record establishes parser acceptance, not correct packet/identity/salt association or a current usable password.

AES Kerberos records use different modes. Preserve each complete text record on one line; avoid shell expansion of `$` and PDF line wrapping. A full `username:RID:LM:NT:::` record is not a raw NT hash; extract the NT field into a separate working file and retain its account mapping. For htpasswd, separate the username from the complete `$apr1$` value and remove any HTML presentation wrapper; do not hash the rendered page or discard the salt.

A JSON field can contain base64 of a bcrypt record. Decode the field as defined by the application's format, require a successful decode, and preserve the resulting full bcrypt prefix/cost/salt/digest. The base64 wrapper is not a hash algorithm. Password-hash checking is candidate verification, not decryption.

For Ansible Vault, extract each complete header/ciphertext block from inline YAML into its own file and convert using Jumbo's `ansible2john.py`. Remove only its filename prefix before the `$ansible$` record for this Hashcat input; retain the variable/file mapping separately. Check that a record was emitted. Recovery yields a vault password, not the decrypted variable value; verify it with `ansible-vault decrypt` into a fresh private output.

Inspect `hashcat --version` and `hashcat -I` for backend/device availability. Define `mode` from the table or verified examples, `hashes` and `wordlist` as existing absolute paths, `pot` as a private case-specific file, `session` as a unique name, and `seconds` as the time budget:

~~~bash
umask 077
hashcat -m "$mode" -a 0 "$hashes" "$wordlist" --potfile-path "$pot" --session "$session" --runtime "$seconds" --status
hashcat -m "$mode" "$hashes" --show --potfile-path "$pot"
~~~

Use the same mode and pot when showing results. An existing pot can explain an immediate already-recovered result. Keep it instead of discarding recovery evidence with `--potfile-disable`.

## Other inputs and incomplete runs

**Binary containers:** follow the reference linked at the top for Password Safe v3 (`5200`) or supported LUKS1 (`14600`). Those modules disable potfiles; the text-record pot/`--show` procedure does not apply. LUKS2 is not supported by that LUKS1 module.

`Token length exception` or `Separator unmatched` usually calls for checking the mode and record representation, not a bigger wordlist. Fix reported backend/self-test failures before trusting a run; do not copy a walkthrough's `--force` as a routine solution. `Exhausted` means the selected candidate space was tried, not that the password is strong. Runtime aborts and skipped/rejected candidates limit coverage. Capture status, tested inputs and recovery count without reproducing secrets unnecessarily.
