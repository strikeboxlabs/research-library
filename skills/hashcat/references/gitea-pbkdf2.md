# Convert an acquired Gitea PBKDF2 record

Keep the selected account's `passwd_hash_algo`, `salt` and `passwd` together with its identity. For the supported modern hexadecimal-salt form, `pbkdf2$50000$50` means PBKDF2-HMAC-SHA256, 50,000 iterations and a 50-byte derived key. A shortened cost changes the computation. Bare `pbkdf2`, an empty algorithm, a legacy ten-byte literal salt or another algorithm requires the producing version's rules; do not substitute the server's current default.

Define `record` as a private UTF-8 JSON object exported from one verified row, with those three exact field names. Keep identity/source mapping separately. Define `hashes` as a new output path. This Python 3 conversion deliberately accepts explicit PBKDF2 parameters and modern hex salts only:

~~~bash
umask 077
python3 - "$record" "$hashes" <<'PY'
import base64, json, pathlib, re, sys
r = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
m = re.fullmatch(r'pbkdf2\$([1-9][0-9]{0,7})\$([1-9][0-9]*)', r['passwd_hash_algo'])
if not m:
    raise SystemExit('Expected explicit PBKDF2 cost and key length')
cost, keylen = map(int, m.groups())
salt_hex, digest_hex = r['salt'], r['passwd']
if not re.fullmatch(r'(?:[0-9a-fA-F]{2}){16,}', salt_hex):
    raise SystemExit('Expected a modern hexadecimal Gitea salt')
if not re.fullmatch(r'(?:[0-9a-fA-F]{2})+', digest_hex):
    raise SystemExit('Invalid hexadecimal digest')
salt, digest = bytes.fromhex(salt_hex), bytes.fromhex(digest_hex)
if len(digest) != keylen or not 16 <= keylen <= 192:
    raise SystemExit('Digest length disagrees with parameters or needs separate mode review')
b64 = lambda value: base64.b64encode(value).decode('ascii')
with open(sys.argv[2], 'x', encoding='ascii', newline='\n') as output:
    output.write(f'sha256:{cost}:{b64(salt)}:{b64(digest)}\n')
PY
~~~

Require successful conversion and one record before the bounded mode `10900` run and matching `--show` procedure in the skill. Base64 must encode the decoded bytes of **both** salt and digest, not their hexadecimal characters. Keep the full digest. Parser acceptance does not validate a copied cost or row association.

The upstream `gitea2hashcat.py` converter hardcodes 50,000 iterations and infers salt/hash order from lengths; inspect the installed script before using it with nondefault records. The reviewed mode 10900 parser compares a digest prefix; independently verify a recovered candidate against the full original derived key using the producer's parameters before claiming an exact application match. This still does not establish current online access.

Resolve version differences using Gitea's [PBKDF2 implementation](https://github.com/go-gitea/gitea/blob/v1.22.0/modules/auth/password/hash/pbkdf2.go), [salt and legacy-parameter handling](https://github.com/go-gitea/gitea/blob/v1.22.0/modules/auth/password/hash/hash.go), and Hashcat's [converter](https://github.com/hashcat/hashcat/blob/master/tools/gitea2hashcat.py) / [mode 10900 parser](https://github.com/hashcat/hashcat/blob/master/src/modules/module_10900.c).
