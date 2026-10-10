# Recover a copied pswm vault without resetting it

Require an authorized bounded vault copy, the compatible installed Python/cryptocode dependencies and a selected candidate list/budget. Preserve the original ciphertext and do not import the pswm application to obtain its decrypt function: its module-level store lookup creates directories. The cryptographic library is the intended existing implementation; do not replace it with a homemade cipher or silently install missing dependencies.

## Identify the envelope and plaintext contract

The compatible cryptocode envelope has four Base64 fields separated by literal asterisks: ciphertext, salt, nonce, authentication tag. The reviewed implementation uses scrypt N=16384/r=8/p=1 with a 32-byte derived key, then AES-GCM; salt, generated nonce and tag are 16 bytes. This is not an OpenSSL Salted__ blob or a password hash that can be passed directly to an unrelated cracking mode. Confirm the acquired program's actual format/version before using these facts.

Preserve padding and field order. A PDF/terminal line wrap is not automatically a newline in the file; acquire the complete original bytes. Strict Base64/length checks detect truncation or a different envelope before treating every candidate as wrong. Older cryptocode versions return False for broad internal errors, while the reviewed current source separates malformed/unauthentic data from some runtime/dependency exceptions. A False result alone therefore does not universally establish a wrong password. Verify the selected library with an owned encrypt/decrypt marker when its behavior is uncertain.

Authenticated plaintext uses newline-separated alias, username and password fields separated by tabs. The pswm parser skips malformed rows, strips trailing whitespace and replaces earlier duplicate aliases; a displayed table can therefore omit or change distinctions in the original plaintext. Its reserved pswm record stores the vault's master credential. Validate the actual records privately; do not conflate a successful GCM tag check with successful SSH authentication.

## Try the selected candidates offline

Define `python_bin` as the trusted interpreter with the existing compatible cryptocode module, `vault_copy` and `wordlist` as private existing UTF-8 files, `limit` as a positive maximum candidate count and `result` as a **fresh** private JSON destination. This adaptable bounded procedure retains spaces in candidate passwords, reads the ciphertext once and stops at the first authenticated plaintext:

~~~bash
umask 077
"$python_bin" -I - "$vault_copy" "$wordlist" "$limit" "$result" <<'PY'
import base64, json, sys
from pathlib import Path
import cryptocode

vault, words, budget, destination = sys.argv[1:]
budget = int(budget)
if budget <= 0:
    raise SystemExit("A positive candidate budget is required")
token = Path(vault).read_text(encoding="utf-8").rstrip("\r\n")
fields = token.split("*")
if len(fields) != 4:
    raise SystemExit("Incomplete or incompatible envelope")
decoded = [base64.b64decode(v, validate=True) for v in fields]
if any(len(v) != 16 for v in decoded[1:]):
    raise SystemExit("Check this format's salt/nonce/tag lengths")
tested = 0
with open(words, encoding="utf-8", newline="") as candidates:
    for raw in candidates:
        if tested >= budget:
            break
        password = raw.rstrip("\r\n")
        tested += 1
        plaintext = cryptocode.decrypt(token, password)
        if plaintext is False:
            continue
        with open(destination, "x", encoding="utf-8") as output:
            json.dump({"candidate_index": tested,
                       "master_password": password,
                       "plaintext": plaintext}, output, ensure_ascii=False)
        print(f"Authenticated plaintext saved; candidate index {tested}")
        raise SystemExit(0)
print(f"No authenticated plaintext among {tested} tested candidates")
raise SystemExit(1)
PY
~~~

Zero establishes authenticated plaintext saved to that fresh destination; inspect its expected record shape before choosing a credential. One reports no hit **within this list/budget**, not an unbreakable vault. Syntax/import/encoding/permission/output-collision or other exceptions leave the attempt incomplete. An empty decrypted string is not False, although it is not a useful pswm record set. -I excludes current-directory/user-site shadowing; the selected environment must still provide the intended module. Choose an explicit appropriate wordlist encoding when UTF-8 is wrong rather than using errors=ignore; strip() would alter passwords with leading/trailing spaces.

Each candidate performs a costly KDF; use the worker's time/resource budget as well as the count and checkpoint progress privately if interrupted. Do not continue through the full list after success or print every recovered secret to logs. Keep the original unchanged, track working-copy/result retention and perform a separately selected authorized service/OS authentication test only when needed. See [cryptocode API](https://github.com/gdavid7/cryptocode), [cipher/KDF implementation](https://github.com/gdavid7/cryptocode/blob/main/cryptocode.py) and [pswm record handling](https://github.com/Julynx/pswm/blob/main/pswm).
