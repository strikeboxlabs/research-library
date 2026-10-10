# Django PBKDF2-SHA256 records and full candidate confirmation

Use mode `10000` for a verified complete `pbkdf2_sha256$iterations$salt$base64_digest` Django record. Retain the actual decimal iterations, literal salt and 44-character base64 SHA-256 digest (32 decoded bytes). This is different from generic mode 10900's colon layout/base64 salt. A historical cost of 12000 is a record parameter, not a timeless Django default. Keep the selected database row/account mapping separately; `is_staff` permits applicable application-admin access and does not mean OS root.

Acquire the full field through a structured export with status/encoding evidence, removing only presentation wrapping. Do not pass a PostgreSQL username column, table borders, screenshot line breaks or an ellipsis into the loader. Do not expand `$` inside an unquoted shell assignment. A Django unusable-password marker or other algorithm needs its actual semantics rather than this mode. Check the installed Hashcat examples/parser for supported lengths; unfamiliar salts must not be shortened to fit.

Run the entrypoint's bounded offline procedure with `mode=10000`, a task-specific session/pot and a chosen existing candidate list. Do not inherit `--force`: it suppresses warnings rather than fixing a backend. Loading success, candidate coverage and recovery are distinct. Exhaustion covers only that attempted space; an abort/time budget/skip leaves partial coverage. `--show` must use the same mode and pot, preserving the original account association.

For one recovered candidate, verify all 32 digest bytes independently against the original selected record. Save this standard-library `confirm_django.py` and supply a file with exactly one complete verifier; the password is read privately from a prompt:

~~~python
import base64
import getpass
import hashlib
import hmac
from pathlib import Path
import sys

lines = Path(sys.argv[1]).read_text(encoding='utf-8').splitlines()
if len(lines) != 1:
    raise ValueError('need exactly one complete selected verifier')
algorithm, cost, salt, encoded = lines[0].split('$')
if algorithm != 'pbkdf2_sha256' or not cost.isascii() or not cost.isdecimal() or not salt:
    raise ValueError('unsupported or incomplete record')
iterations = int(cost)
if not 1 <= iterations <= 10000000:
    raise ValueError('cost outside this local confirmation budget')
expected = base64.b64decode(encoded, validate=True)
if len(expected) != 32:
    raise ValueError('incomplete SHA-256 digest')
candidate = getpass.getpass('Candidate: ').encode('utf-8')
actual = hashlib.pbkdf2_hmac('sha256', candidate, salt.encode('utf-8'), iterations, dklen=32)
match = hmac.compare_digest(actual, expected)
print('full_digest_match:', match)
raise SystemExit(0 if match else 1)
~~~

The ten-million cost ceiling is this helper's explicit resource bound, not a Django/Hashcat format limit. For a valid higher-cost record, choose a reviewed budget before changing it; never substitute a lower cost. Non-UTF-8 input/custom application normalization requires its actual password/salt byte contract. A match confirms this candidate against this stored verifier, not a current Linux/SSH password, active user or unrestricted access. A changed digest tail must fail even when an earlier prefix matches.

See [Django 1.6.11 hasher](https://github.com/django/django/blob/1.6.11/django/contrib/auth/hashers.py), [byte derivation](https://github.com/django/django/blob/1.6.11/django/utils/crypto.py), [Hashcat mode 10000](https://github.com/hashcat/hashcat/blob/master/src/modules/module_10000.c) and [Python PBKDF2](https://docs.python.org/3/library/hashlib.html#hashlib.pbkdf2_hmac).
