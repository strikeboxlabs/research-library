---
name: hashcat
description: Select Hashcat modes and run bounded offline checks on application or NT/Kerberos records, Password Safe v3 files and LUKS1 images. Use when encoding, binary inputs, potfile exceptions or exhausted runs need interpretation.
---

# Hashcat offline checks

Match the input representation to the mode, using its acquisition context and the installed version's examples. A 32-character hexadecimal string alone does not identify its algorithm.

| Known artifact | Mode |
|---|---|
| Raw NT hash from a SAM account | `1000` |
| Apache `$apr1$...` record from htpasswd | `1600`; not raw MD5 mode `0`. |
| Drupal 7 `$S$...` password record | `7900` |
| Complete supported bcrypt `$2...` record | `3200` |
| Raw MD5 established from the producing application | `0`; length alone is insufficient. |
| Complete portable phpass `$P$...` or `$H$...` record | `400`; an application's name alone does not establish the format. |
| Verified PBKDF2-HMAC-SHA256 encoded as `sha256:iterations:base64_salt:base64_digest` | `10900`; preserve the actual cost and byte encodings. |
| Converted Ansible Vault `$ansible$...` record | `16900`; not the raw YAML or `$ANSIBLE_VAULT` file. |
| `$krb5tgs$23$...` service-ticket material | `13100` |
| `$krb5asrep$23$...` AS-REP material | `18200` |

AES Kerberos records use different modes. Preserve each complete text record on one line; avoid shell expansion of `$` and PDF line wrapping. A full `username:RID:LM:NT:::` record is not a raw NT hash; extract the NT field into a separate working file and retain its account mapping. For htpasswd, separate the username from the complete `$apr1$` value and remove any HTML presentation wrapper; do not hash the rendered page or discard the salt.

A JSON field can contain base64 of a bcrypt record. Decode the field as defined by the application's format, require a successful decode, and preserve the resulting full bcrypt prefix/cost/salt/digest. The base64 wrapper is not a hash algorithm. Drupal/bcrypt password checking is candidate verification, not decryption.

For a compatible Grafana export, confirm parameters against the producing version: converters may hardcode 10,000 iterations. The usual historical conversion base64-encodes the literal salt's bytes and the hex-decoded digest, not the hexadecimal digest text. Keep usernames mapped separately and exclude converter banners from the hash file. Supply the wordlist positionally as below; `--wordlist` is not its documented input option.

For Ansible Vault, extract each complete header/ciphertext block from inline YAML into its own file and convert using Jumbo's `ansible2john.py`. Remove only its filename prefix before the `$ansible$` record for this Hashcat input; retain the variable/file mapping separately. Check that a record was emitted. Recovery yields a vault password, not the decrypted variable value; verify it with `ansible-vault decrypt` into a fresh private output.

Inspect `hashcat --version` and `hashcat -I` for backend/device availability. Define `mode` from the table or verified examples, `hashes` and `wordlist` as existing absolute paths, `pot` as a private case-specific file, `session` as a unique name, and `seconds` as the time budget:

~~~bash
umask 077
hashcat -m "$mode" -a 0 "$hashes" "$wordlist" --potfile-path "$pot" --session "$session" --runtime "$seconds" --status
hashcat -m "$mode" "$hashes" --show --potfile-path "$pot"
~~~

Use the same mode and pot when showing results. An existing pot can explain an immediate already-recovered result. Keep it instead of discarding recovery evidence with `--potfile-disable`.

**Binary containers need a different input and result path.** For Password Safe v3 (`5200`) or supported LUKS1 (`14600`), read [binary container checks](references/binary-containers.md). Both reviewed modules disable potfiles; the text-record pot/`--show` procedure does not apply. LUKS2 is not supported by that LUKS1 module.

`Token length exception` or `Separator unmatched` usually calls for checking the mode and record representation, not a bigger wordlist. Fix reported backend/self-test failures before trusting a run; do not copy a walkthrough's `--force` as a routine solution. `Exhausted` means the selected candidate space was tried, not that the password is strong. Runtime aborts and skipped/rejected candidates limit coverage. Capture status, tested inputs and recovery count without reproducing secrets unnecessarily.

Documentation reviewed 2026-10-09; Linux execution untested. Cases: Active p. 9; Administrator pp. 7, 10; Alert p. 11; Arkham p. 5; Armageddon pp. 7–8; Artificial pp. 6, 11; Authority pp. 5–8; BigBang pp. 11–14. Sources: [mode examples](https://hashcat.net/wiki/doku.php?id=example_hashes), [CLI options/statuses](https://hashcat.net/wiki/doku.php?id=hashcat), [Apache APR1](https://github.com/hashcat/hashcat/blob/master/src/modules/module_01600.c), [Drupal 7](https://github.com/hashcat/hashcat/blob/master/src/modules/module_07900.c), [bcrypt](https://github.com/hashcat/hashcat/blob/master/src/modules/module_03200.c), [Ansible parser](https://github.com/hashcat/hashcat/blob/master/src/modules/module_16900.c), [Ansible converter](https://github.com/openwall/john/blob/bleeding-jumbo/run/ansible2john.py), [phpass](https://github.com/hashcat/hashcat/blob/master/src/modules/module_00400.c), [PBKDF2-SHA256](https://github.com/hashcat/hashcat/blob/master/src/modules/module_10900.c), [Grafana converter](https://github.com/iamaldi/grafana2hashcat/blob/main/grafana2hashcat.py).
