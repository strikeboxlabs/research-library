# Salted digest formats and legacy OFBiz conversion

Read the applicable format section before preparing the input; use the main skill's bounded run only after resolving its mode and encoding.

## Salted MD5

A configured salt plus a 32-digit digest does not establish concatenation order. Verify the producer or a known synthetic pair: `md5(salt + password)` is mode `20`, while `md5(password + salt)` is `10`. These are different from md5crypt `500`, even though all names contain MD5. Preserve the literal salt after `:` and account mapping separately; use verified byte encoding and `--hex-salt` on both run and show when representing salt bytes as hex. A walkthrough's successful recovery supports its case, not every application's format.

The [mode 20 module](https://github.com/hashcat/hashcat/blob/master/src/modules/module_00020.c) and [mode 10 module](https://github.com/hashcat/hashcat/blob/master/src/modules/module_00010.c) include public self-test pairs for checking the distinction.

## Distinguish SHA-1 salt order

A database excerpt showing only a password digest may omit its salt. For example, historical [Bludit 3.10.0 code](https://github.com/bludit/bludit/blob/3.10.0/bl-kernel/users.class.php) computes `sha1(password + salt)`. Confirm the actual producing version and complete user record before selecting a mode: a nonempty appended salt maps to `110`, while confirmed unsalted or empty-salt hashing maps to `100`. Missing salt evidence is not evidence of an empty salt. The OFBiz procedure below uses the opposite order, mode `120`.

For mode `110`, preserve literal salt bytes after the digest separator. If delimiters or non-ASCII data make that representation ambiguous, encode the salt bytes as hex and add `--hex-salt` to both the run and `--show`; establish the application's byte encoding first. Do not reuse the OFBiz record decoder for a different application's storage format.

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

Require successful conversion before using the output. For this file, set `mode=120` and add **`--hex-salt` to both the bounded run and `--show` commands in SKILL.md**. Without it, hexadecimal characters become the literal salt and the candidates will not match. A known candidate can be checked independently against the original application's byte formula; no recovery result establishes that an online account accepts it.
