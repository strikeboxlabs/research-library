# Decrypt a known-format AES-CBC artifact

Establish the producer's mode, key bytes, IV, padding and outer encoding before selecting a command. A textual key may mean literal encoded bytes, hexadecimal, or a password for a KDF; these are different inputs. Base64 describes an outer representation, not the encryption algorithm. Preserve the original and decode only that established layer into a fresh binary file, checking decoding status and length.

For **raw AES-128-CBC ciphertext with PKCS#7 padding**, define `ciphertext` as that binary file, `key_hex` as exactly 32 hex digits for the known 16-byte key, `iv_hex` as exactly 32 hex digits for the known IV, and `plaintext`/`diagnostics` as fresh private output paths. Use `openssl enc -help` and `openssl enc -list` to confirm local support. This command exposes raw key material through its process arguments; use public fixtures or a context where that exposure is acceptable.

~~~bash
umask 077
openssl enc -d -aes-128-cbc -K "$key_hex" -iv "$iv_hex" -in "$ciphertext" -out "$plaintext" 2>"$diagnostics"
status=$?
~~~

Inspect `status` and diagnostics before consuming any output. `-K` takes key bytes expressed as hex; `-k`/`-pass` derive a key from a password and are not substitutes. Reject short/long hex values yourself: OpenSSL can warn and pad or truncate them. AES-192/256 requires the corresponding cipher and key size; all three CBC variants use a 16-byte IV/block. Do not add password/salt/KDF options to imitate an unrelated encrypted-file format.

An omitted IV in a producer must be resolved from that implementation. For example, pyaes' low-level CBC constructor defaults to a zero IV, whereas OpenSSL's explicit-key command requires an IV. That compatibility observation is not a rule to guess zero for other inputs or a recommendation for new encryption.

| Result | Interpretation and next decision |
|---|---|
| Nonzero exit, `bad decrypt`, or non-block-aligned input | Check transfer/encoding, cipher, key, IV and padding agreement. The output file can already contain partial plaintext; do not treat its existence as success. |
| Successful exit and plausible text | Padding was accepted, not authenticity. Check independent structure/expected contents; a wrong IV can corrupt only the first block while later blocks and padding remain valid. |
| Producer explicitly uses no padding or returns raw padded blocks | Use `-nopad` only for that established format or deliberate raw-block diagnosis. Retain exact bytes; do not strip arbitrary trailing characters until a verified padding scheme justifies it. |

With PKCS#7, a final value `n` denotes `n` equal padding bytes, with `1 <= n <= 16`; validate the entire suffix. The default command validates/removes this padding. Do not turn a padding error into an apparent success merely by disabling the check. CBC supplies no authentication, and `openssl enc` does not provide GCM/CCM verification; authenticated formats need their actual reader.

Consult [enc options](https://docs.openssl.org/3.5/man1/openssl-enc/), [input/output and key parsing](https://github.com/openssl/openssl/blob/openssl-3.5/apps/enc.c), [pyaes CBC behavior](https://github.com/ricmoo/pyaes/blob/master/pyaes/aes.py) and [NIST CBC mode definitions](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38a.pdf) when matching a producer.

## Custom length header and space padding

For a producer explicitly writing **16 ASCII decimal length bytes, then 16 IV bytes, then AES-CBC ciphertext**, parse that envelope before using `enc`. It is not OpenSSL's salted-password container. Use binary reads; a text-mode reader can reject or transform IV/ciphertext bytes.

If producer source derives the key as `SHA256(password.encode('utf-8')).digest()`, that is 32 raw bytes and selects AES-256. Its hex representation for `-K` has 64 digits. It is not the 64 ASCII bytes of a hex digest, and `-pass` plus `-md sha256` does not reproduce that arbitrary derivation. A 64*1024 read chunk is 65,536 bytes; it is independent of AES's 16-byte block size.

Validate the decimal header and file length first. Let `n` be the original byte count and `c` the ciphertext byte count after the 32-byte header. For the producer that pads only a final short block with ASCII spaces, require `c == ((n + 15) // 16) * 16`. No extra block is added when `n` is already aligned. Reject a short header, malformed length or mismatched ciphertext before decrypting.

Define `ciphertext` as the extracted bytes after that header, `key_hex`/`iv_hex` as the verified key/IV representations and `padded_plaintext`/`diagnostics` as fresh private files:

~~~bash
umask 077
openssl enc -d -aes-256-cbc -nopad -K "$key_hex" -iv "$iv_hex" -in "$ciphertext" -out "$padded_plaintext" 2>"$diagnostics"
status=$?
~~~

Only after zero status, verify the output has `c` bytes and the `c-n` trailing bytes are exactly spaces; retain precisely the first `n` bytes in a new file. Do not use `strip()`/`rstrip()` or discard the length: original content can legitimately end in spaces. Apply any inner base64 decoding to those recovered bytes, then check that decoder's status. Visible text followed by `invalid input` does not establish a complete decode.

The header and CBC ciphertext are unauthenticated; plausible length, padding and output do not prove integrity or the correct key. An aligned plaintext has no padding to check. Keep independent expected structure/checksums where available. An unavailable IV prevents reliable recovery of the first CBC block, but does not universally prevent recovery of later blocks with a known key and preceding ciphertext.

See [CBC byte requirements](https://www.pycryptodome.org/src/cipher/classic), [digest versus hexadecimal output](https://docs.python.org/3/library/hashlib.html) and the enc/NIST references above. This is a compatibility procedure for an established historical format, not a new encryption design.


## Match a legacy OpenSSL password container

For a producer confirmed to use **OpenSSL enc AES-256-CBC with its legacy password derivation**, establish the producer version, digest, padding and outer encoding. The decoded legacy container starts with `Salted__`, an 8-byte salt and ciphertext. That marker does not encode the cipher or KDF; length divisible by 16 does not identify AES-256-CBC. PBKDF2 containers need the producer's actual parameters and a separate matching command.

OpenSSL changed the default digest from MD5 to SHA-256 in 1.1.0. Use the independently established digest explicitly rather than the installed version's default or CryptoJS's MD5 convention. Define `ciphertext` as the complete decoded binary container, `digest_name` as that known digest, `passfile` as a private file whose first line is the known exact passphrase, and `plaintext`/`diagnostics` as fresh private destinations:

~~~bash
umask 077
openssl enc -d -aes-256-cbc -md "$digest_name" -pass "file:$passfile" \
  -in "$ciphertext" -out "$plaintext" 2>"$diagnostics"
status=$?
~~~

The command reads the stored salt and derives both key and IV. Do not strip the header, supply a raw `-K`, override the salt with `-S`, or add `-pbkdf2`/`-iter` to this established legacy format. Those changes alter the derivation. The password-file interface does not represent arbitrary multiline or NUL-containing passphrases. A deprecated-KDF warning describes compatibility with the old producer; it does not by itself mean decryption failed. Apply the exit-status, partial-output and independent-content checks above. Missing producer parameters remain a prerequisite gap, not a reason to try password or cipher lists.

The [enc manual](https://docs.openssl.org/3.5/man1/openssl-enc/) documents digest history, password sources and PBKDF2 options. This is recovery of an owned historical format with a known passphrase, not a new encryption design.

## Match a CryptoJS password envelope

Only for a producer confirmed to use CryptoJS's default **string-passphrase AES** interface: its OpenSSL formatter writes base64 of `Salted__`, an 8-byte salt and AES-256-CBC ciphertext. The legacy EvpKDF uses MD5 with one iteration; this differs from PBKDF2 and OpenSSL's current default digest. A base64 prefix alone does not establish those settings. Check the producer version and overrides.

Define `base64_file` as one validated, unwrapped base64 field without JSON quotes, `passfile` as a private file whose first line contains the known exact passphrase, and `plaintext`/`diagnostics` as fresh private destinations:

~~~bash
umask 077
openssl enc -d -aes-256-cbc -a -A -md md5 -pass "file:$passfile" \
  -in "$base64_file" -out "$plaintext" 2>"$diagnostics"
status=$?
~~~

Do not add `-pbkdf2`, `-iter`, a raw `-K`, or `-S` for an envelope that already carries its salt. A legacy-KDF warning describes the established old format; changing the derivation makes it incompatible. This command handles a single-line password file, not an arbitrary multiline or NUL-containing passphrase. Apply the status, partial-output and independent-structure checks above.

For nested formats, preserve the intermediate representation exactly. `CryptoJS.AES.decrypt(...).toString()` returns a WordArray's default **hex text**; `.toString(CryptoJS.enc.Utf8)` decodes text instead. If that hex text is passed as the next AES argument as a JavaScript string, it is another passphrase, not raw key bytes. Hex-decoding it before the next KDF changes the input. A nearby Argon2 verifier does not establish that AES uses Argon2. Plausible plaintext or a successful TOTP import still does not establish remote authentication.

See [CryptoJS formats and encodings](https://cryptojs.gitbook.io/docs), [password dispatch and salt handling](https://github.com/brix/crypto-js/blob/develop/src/cipher-core.js), [EvpKDF defaults](https://github.com/brix/crypto-js/blob/develop/src/evpkdf.js) and the enc manual above. This is recovery of a known historical format, not a recommendation for new encryption.
