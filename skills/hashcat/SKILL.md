---
name: hashcat
description: Select Hashcat modes and run bounded offline checks on application or NT/Kerberos records, Password Safe v3 files and LUKS1 images. Use when salted SHA-1 conversion, binary inputs, potfile exceptions or exhausted runs need interpretation.
---

# Hashcat offline checks

Match the input representation to the mode, using its acquisition context and the installed version's examples. A 32-character hexadecimal string alone does not identify its algorithm.

| Known artifact | Mode |
|---|---|
| Raw NT hash from a SAM account | `1000` |
| Apache `$apr1$...` record from htpasswd | `1600`; not raw MD5 mode `0`. |
| Drupal 7 `$S$...` password record | `7900` |
| Complete supported bcrypt `$2...` record | `3200` |
| Verified SHA-1 of salt bytes followed by password bytes | `120`; encode digest and salt as described below. |
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

## Convert a verified legacy OFBiz record

For the legacy `$SHA$salt$base64url_digest` format, first confirm the producing version's [HashCrypt implementation](https://github.com/apache/ofbiz-framework/blob/release18.12/framework/base/src/main/java/org/apache/ofbiz/base/crypto/HashCrypt.java): it hashes UTF-8 salt bytes followed by password bytes, then stores unpadded base64url. This maps to mode `120`, `sha1(salt.pass)`. An application's current default hash setting does not prove the format of an older stored record; other OFBiz formats need different handling.

Define `record` as a UTF-8 file containing one complete verified record and `hashes` as a new output file. This conversion requires Python 3 and writes `hex_digest:hex_salt`; hex salt preserves delimiters and non-ASCII bytes without ambiguity:

~~~bash
umask 077
python3 - "$record" "$hashes" <<'PY'
import base64, pathlib, re, sys
parts = pathlib.Path(sys.argv[1]).read_text(encoding='utf-8').rstrip('\r\n').split('$')
if len(parts) != 4 or parts[:2] != ['', 'SHA']:
    raise SystemExit('Expected one complete legacy $SHA$ record')
salt, encoded = parts[2:]
if not re.fullmatch(r'[A-Za-z0-9_-]{27}', encoded):
    raise SystemExit('Expected unpadded base64url of a 20-byte SHA-1 digest')
digest = base64.b64decode(encoded + '=', altchars=b'-_', validate=True)
if len(digest) != 20 or base64.urlsafe_b64encode(digest).decode().rstrip('=') != encoded:
    raise SystemExit('Invalid or noncanonical digest encoding')
with open(sys.argv[2], 'x', encoding='ascii', newline='\n') as output:
    output.write(digest.hex() + ':' + salt.encode('utf-8').hex() + '\n')
PY
~~~

Require successful conversion before using the output. For this file, set `mode=120` and add **`--hex-salt` to both the bounded run and `--show` commands above**. Without it, hexadecimal characters become the literal salt and the candidates will not match. A known candidate can be checked independently against the original application's byte formula; no recovery result establishes that an online account accepts it.

## Other inputs and incomplete runs

**Binary containers need a different input and result path.** For Password Safe v3 (`5200`) or supported LUKS1 (`14600`), read [binary container checks](references/binary-containers.md). Both reviewed modules disable potfiles; the text-record pot/`--show` procedure does not apply. LUKS2 is not supported by that LUKS1 module.

`Token length exception` or `Separator unmatched` usually calls for checking the mode and record representation, not a bigger wordlist. Fix reported backend/self-test failures before trusting a run; do not copy a walkthrough's `--force` as a routine solution. `Exhausted` means the selected candidate space was tried, not that the password is strong. Runtime aborts and skipped/rejected candidates limit coverage. Capture status, tested inputs and recovery count without reproducing secrets unnecessarily.
