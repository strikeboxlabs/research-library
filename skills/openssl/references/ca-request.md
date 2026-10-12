# Prepare a CA request for an owned identity

Require the intended CA's approved identity, algorithm/key-size policy and request configuration. This creates a key and CSR locally; submitting it and selecting a CA template are separate operations. Define `key` and `csr` as fresh paths in a private owned directory, `rsa_bits` as the CA-approved RSA size, and `request_config` as the reviewed configuration for that identity. Do not substitute another person's UPN or assume blank subject prompts select the right identity.

~~~bash
umask 077
openssl genpkey -algorithm RSA -pkeyopt "rsa_keygen_bits:$rsa_bits" -aes-256-cbc -out "$key"
openssl pkey -in "$key" -noout -check
openssl req -new -sha256 -key "$key" -config "$request_config" -out "$csr"
openssl req -in "$csr" -noout -text -verify
~~~

Check each result before continuing. Enter the private-key passphrase at the prompts; it is distinct from an account password or a CSR challengePassword. Keep the generated key encrypted. The reviewed request configuration must supply the intended subject and requested extensions; inspect the resulting SAN and EKU instead of assuming the configuration included them. Request-signature verification is not CA issuance. On OpenSSL before 3.3, read its diagnostic rather than relying solely on a zero `req -verify` status.

After issuance, inspect the certificate's actual subject, issuer, SAN, EKU and validity. Compare the complete public-key encodings when checking its association with this key. Define `cert` as the issued PEM certificate and `key_public`/`cert_public` as fresh public-only files:

~~~bash
openssl pkey -in "$key" -pubout -outform DER -out "$key_public"
openssl x509 -in "$cert" -pubkey -noout | openssl pkey -pubin -outform DER -out "$cert_public"
openssl dgst -sha256 "$key_public" "$cert_public"
~~~

Use Bash `pipefail` and preserve the pipeline's diagnostic/status. Matching complete digests establish the same public key, relative to the acquired files. Separately verify the certificate chain using independently trusted CA inputs and the intended application purpose. A CA-issued client certificate does not configure a WinRM listener, its certificate-to-account mapping or endpoint authorization. Finish with the CSR and key location, verified key association and remaining issuance/trust/service facts; do not include private key bytes or passphrases.

Resolve generation and encoding differences with [genpkey](https://docs.openssl.org/3.5/man1/openssl-genpkey/), [req](https://docs.openssl.org/3.5/man1/openssl-req/), [pkey](https://docs.openssl.org/3.5/man1/openssl-pkey/) and [x509](https://docs.openssl.org/3.5/man1/openssl-x509/).
