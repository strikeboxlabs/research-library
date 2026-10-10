# Reproduce an acquired AES-CTR comparison

Use exact acquired key, initial counter block and ciphertext bytes, with the producing implementation's counter increment convention and input encoding established. The selected trusted Python environment must already contain `cryptography`; do not replace the installed library with a home-written cipher. Preserve the byte lengths and source ranges privately. An ASCII hex string is a representation, not the key bytes, and a hex-to-base64-to-bytes round trip adds no cryptographic operation.

For AES, key lengths are 16/24/32 bytes. `modes.CTR` takes the complete 16-byte AES initial counter block, not an arbitrarily short nonce. Confirm whether the producer uses big-endian full-block increment, a restricted counter suffix, a different starting block or prior consumed keystream. The reviewed rust-crypto CtrMode encrypts the supplied counter then increments from its final byte with carry; resolve an actually different compiled library separately. CTR uses no padding and preserves length.

Define `key_file`, `counter_file` and `ciphertext_file` as private files containing the exact raw bytes, and `plaintext_file` as a fresh output. Save this reviewed `recover_ctr.py`:

~~~python
from pathlib import Path
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

key, counter, ciphertext = [Path(p).read_bytes() for p in sys.argv[1:4]]
if len(key) not in (16, 24, 32) or len(counter) != 16 or not ciphertext:
    raise ValueError('need an AES key, full 16-byte counter and nonempty ciphertext')
cipher = Cipher(algorithms.AES(key), modes.CTR(counter))
dec = cipher.decryptor()
plaintext = dec.update(ciphertext) + dec.finalize()
enc = Cipher(algorithms.AES(key), modes.CTR(counter)).encryptor()
if enc.update(plaintext) + enc.finalize() != ciphertext:
    raise ValueError('round trip mismatch')
with open(sys.argv[4], 'xb') as output:
    output.write(plaintext)
print('bytes:', len(plaintext), 'round_trip: match')
~~~

With `python_bin` selecting that environment:

~~~bash
umask 077
"$python_bin" recover_ctr.py "$key_file" "$counter_file" "$ciphertext_file" "$plaintext_file"
~~~

Check status and the reported/output byte length. Existing output, malformed key/counter or missing dependency is a prerequisite/input error; do not patch the length with guessed bytes. Re-encryption checks internal consistency only: decrypting with a wrong key and re-encrypting with that same key also round-trips. Interpret recovered bytes against the observed full comparison and input transformation, or a separately known test vector/correctness condition. Printable output alone is weak evidence. CTR has no authentication tag, so random or altered ciphertext can produce plausible-looking unauthenticated output.

If exporting hex, decode it directly with `bytes.fromhex` and require the measured length; base64-decode only when the actual captured format is base64. Keep plaintext as bytes until the observed encoding is known, and do not strip a newline merely to make it look like a password. A recovered binary predicate does not establish an account password or access; a selected authorized application check must establish acceptance and identity/effects separately.

See [cryptography Cipher/AES/CTR](https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/), [rust-crypto counter implementation](https://github.com/DaGenix/rust-crypto/blob/master/src/blockmodes.rs) and [Python byte conversion](https://docs.python.org/3/library/stdtypes.html#bytes.fromhex).
