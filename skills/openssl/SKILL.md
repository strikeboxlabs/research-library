---
name: openssl
description: Inspect and convert X.509 certificates and certificate requests with OpenSSL. Use to distinguish CSR signatures, issued identities, file encodings and trust-chain validation.
---

# OpenSSL certificate evidence

Record `openssl version` and inspect subcommand help. Identify whether the input is a CSR, certificate, private key or bundle; a `.cer` extension alone does not distinguish DER from PEM. Work on copies and choose fresh output paths.

Define `csr` as an existing PEM request and `cert` as an issued PEM certificate:

~~~bash
openssl req -in "$csr" -noout -text -verify
openssl x509 -in "$cert" -noout -text -fingerprint -sha256
~~~

CSR verification checks the request's signature against its included public key. It does not establish CA issuance, trust, identity authorization or that the requested extensions were granted. Inspect the **issued certificate's** subject, SAN, EKU, key usage, validity and issuer separately. Preserve extension context instead of grepping one matching name and assuming its meaning.

For an observed DER certificate, define `der_cert` and a new `pem_cert`:

~~~bash
openssl x509 -inform DER -in "$der_cert" -outform PEM -out "$pem_cert"
~~~

Use a separate `-noout -text` inspection when needed; do not mix a textual dump into the file intended as a clean PEM trust input. A parser error calls for checking object type, encoding and transfer completeness before regenerating keys or requests.

Define `ca_bundle` as independently trusted CA certificates and `intermediates` as the supplied intermediate chain:

~~~bash
openssl verify -CAfile "$ca_bundle" -untrusted "$intermediates" "$cert"
~~~

Omit `-untrusted` if no intermediate file is needed. Choose the intended verification purpose/hostname options when applicable; a generic chain check does not establish that Kerberos, TLS client authentication or a specific service will accept the certificate. An `OK` result is relative to the configured trust inputs and verification options, not proof that a CA is trustworthy. Revocation checking also needs explicit applicable data/options.

For certificate-based login, confirm the matching private key exists and is readable by the intended process without printing it. Record certificate fingerprints and verification diagnostics, not private-key contents.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Anubis pp. 7, 16–17. Sources: [req](https://docs.openssl.org/3.5/man1/openssl-req/), [x509](https://docs.openssl.org/3.5/man1/openssl-x509/), [verify](https://docs.openssl.org/3.5/man1/openssl-verify/).
