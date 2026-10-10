# Historical Grafana PBKDF2 records

Use with a coherent database export and producing-version evidence. Grafana **8.0.0** `EncodePassword` uses PBKDF2-HMAC-SHA256, 10,000 iterations, a 50-byte derived key and the literal salt string's bytes; its stored password is hexadecimal. This is not Gitea's modern hex-salt format. Neither the SQLite writer version nor current Grafana defaults identifies an older row's parameters. `rands` is not passed into this derivation. Source rows, exporter headers and account labels are not Hashcat input.

If the reviewed installed iamaldi `grafana2hashcat.py` fits this verified 10,000-round format, prefer it to recreating the conversion. Define `converter` as its actual path, inspect `python3 "$converter" -h`, and prepare `input_records` with one **hex_digest,literal_salt** data line per selected row, no header/account/CSV quoting. Its simplistic comma splitting requires a representable salt; preserve identity separately. Define `hashes` as a fresh private output:

~~~bash
umask 077
python3 "$converter" "$input_records" -o "$hashes"
~~~

Use `-o`: stdout contains banners and suggested commands, and the script overwrites an existing output. It hardcodes 10,000 rounds. A different verified cost or salt containing delimiters needs a parameter-preserving approach, not relabeling the input. The following standard-library fallback consumes the selected **headered CSV** instead; it is useful when the converter is absent/incompatible. Define `records` as that export with `id,login,password,salt` columns (additional `rands` is allowed), `selected_id` as the exact numeric row ID, `iterations` and `key_bytes` as independently verified producer parameters, and `hashes` as a nonexistent private output:

~~~bash
umask 077
python3 - "$records" "$selected_id" "$iterations" "$key_bytes" "$hashes" <<'PY'
import base64, csv, pathlib, re, sys
path, row_id, cost_text, length_text, output = sys.argv[1:]
if not row_id.isdecimal() or not re.fullmatch(r'[1-9][0-9]*', cost_text):
    raise SystemExit('Expected a selected numeric ID and positive verified cost')
cost, length = int(cost_text), int(length_text)
if not 16 <= length <= 192:
    raise SystemExit('Derived-key length needs a separate mode review')
with open(path, encoding='utf-8', newline='') as source:
    reader = csv.DictReader(source)
    if not {'id', 'login', 'password', 'salt'} <= set(reader.fieldnames or []):
        raise SystemExit('Missing required Grafana export columns')
    rows = [r for r in reader if r['id'] == row_id]
if len(rows) != 1:
    raise SystemExit('Expected exactly one selected source row')
row = rows[0]
if not re.fullmatch(r'(?:[0-9a-fA-F]{2})+', row['password'] or ''):
    raise SystemExit('Invalid hexadecimal verifier')
salt, digest = row['salt'].encode('utf-8'), bytes.fromhex(row['password'])
if not salt or len(digest) != length:
    raise SystemExit('Missing salt or verifier length disagrees with producer')
b64 = lambda b: base64.b64encode(b).decode('ascii')
with open(output, 'x', encoding='ascii', newline='\n') as destination:
    destination.write(f'sha256:{cost}:{b64(salt)}:{b64(digest)}\n')
print('Converted one selected row; retain its identity mapping separately')
PY
~~~

Require successful conversion and exactly one complete output line. Independently base64-decode both fields and compare **salt bytes** and **full hex-decoded verifier bytes** with that row. Do not base64-encode the ASCII hexadecimal digest or trim salt whitespace. A header, wrapped line, missing `sys` import in an error branch or stale output is a preparation failure, not a wrong candidate.

Run the entrypoint's bounded dictionary procedure with `mode=10900`, a positional wordlist, the selected `hashes` and the same private potfile for `--show`. `Cracked`/potfile recovery is distinct from `Exhausted`, a runtime limit or a backend/parser error. Preserve the original 50 bytes: the reviewed module compares the first 16 derived-key bytes. Verify a recovered candidate against the **entire original record** using its actual cost before claiming an exact producer match. For one selected CSV row, define `records`, `selected_id` and verified `iterations`; the candidate is entered privately, not put in command arguments:

~~~bash
python3 - "$records" "$selected_id" "$iterations" <<'PY'
import csv, getpass, hashlib, hmac, sys
with open(sys.argv[1], encoding='utf-8', newline='') as source:
    rows = [r for r in csv.DictReader(source) if r['id'] == sys.argv[2]]
if len(rows) != 1:
    raise SystemExit('Expected exactly one selected row')
r = rows[0]
expected = bytes.fromhex(r['password'])
candidate = getpass.getpass('Recovered candidate: ').encode('utf-8')
actual = hashlib.pbkdf2_hmac('sha256', candidate, r['salt'].encode('utf-8'),
                             int(sys.argv[3]), dklen=len(expected))
if not hmac.compare_digest(actual, expected):
    raise SystemExit('Candidate does not match the full original verifier')
print('Full original verifier matched; online account access remains untested')
PY
~~~

This verifies the historical producer's byte convention, not every possible password normalization rule. A match belongs to that application row; an SSH login is a separately authorized reuse check with a selected OS account, endpoint and observed authentication/identity. No match calls for checking the row/cost/byte mapping before extending candidate coverage.

Resolve differences with [Grafana 8.0.0 derivation](https://github.com/grafana/grafana/blob/v8.0.0/pkg/util/encoding.go), [iamaldi converter](https://github.com/iamaldi/grafana2hashcat/blob/main/grafana2hashcat.py), [mode 10900 parser](https://github.com/hashcat/hashcat/blob/master/src/modules/module_10900.c) and [Python PBKDF2](https://docs.python.org/3/library/hashlib.html#hashlib.pbkdf2_hmac).
