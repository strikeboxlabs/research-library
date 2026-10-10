# PKCS#12 inspection and selected extraction

Use an existing authorized PFX/P12 copy. Define `bundle` as its absolute path. Inspect its structure without outputting keys or certificates:

~~~bash
openssl pkcs12 -in "$bundle" -info -noout
~~~

Enter the actual import password at the prompt. A particular tool may have created a bundle with an empty password; do not assume every bundle has one. Keep MAC verification enabled. A wrong password, corrupt file and unavailable legacy cipher are different failures.

If an OpenSSL 3 diagnostic identifies an unsupported legacy algorithm such as RC2, inspect the installed providers and retry that specific operation with `-legacy` if appropriate. This is per-command compatibility, not a reason to weaken global TLS settings or disable integrity checks. Failure to load the legacy provider needs a local installation/provider-path fix.

Define `cert_out` and `key_out` as fresh files in a private directory, then extract separately:

~~~bash
umask 077
openssl pkcs12 -in "$bundle" -clcerts -nokeys -out "$cert_out"
openssl pkcs12 -in "$bundle" -nocerts -out "$key_out"
~~~

The first command selects certificates associated with the identity rather than CA certificates and omits keys. The second omits certificates and normally prompts for a **new output PEM passphrase** as well as the bundle's import password. Keep key output encrypted. `-noenc` (older `-nodes`) removes that output encryption and is not needed for ordinary inspection. Add a legacy compatibility flag only if the earlier diagnosis required it.

Inspect the resulting certificate's identity, usage and fingerprint, and verify that the intended key matches before configuring a consumer. Do not assume a multi-identity bundle yields exactly one object or that every consumer accepts bag attributes/multiple PEM objects. Successful extraction does not establish trust, certificate mapping or acceptance by PKINIT/Schannel. Retain private keys and passphrases locally; report fingerprints and diagnostics.

See [OpenSSL pkcs12](https://docs.openssl.org/3.5/man1/openssl-pkcs12/).
