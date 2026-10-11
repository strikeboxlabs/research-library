---
name: openssl
description: Inspect and package owned keys, certificates, PKCS#12 and ASN.1 artifacts, diagnose TLS mail/FTP sessions, or recover known-format AES-CBC and legacy crypt-record artifacts. Use for trust, serialization and incomplete-output decisions.
---

# OpenSSL inspection

Read this entire SKILL.md before acting; reuse complete current context. Identify the object/protocol and required trust inputs, then read the selected conditional reference fully. Finish with parsing/verification status and the requested identity or recovered-artifact evidence; missing trust or incomplete output remains unresolved. Keep unrelated references unloaded.

Record `openssl version` and inspect subcommand help. Identify whether the input is a CSR, certificate, private key or bundle; a `.cer` extension alone does not distinguish DER from PEM. Work on copies and choose fresh output paths.

For a requested transfer-integrity comparison, define `artifact` as the saved file and run `openssl dgst -sha256 "$artifact"` at both available endpoints. Compare the same algorithm and complete digest, retaining each file's size and transfer status. A matching digest corroborates identical bytes relative to those inputs; it does not establish publisher identity or safe contents. The source's legacy SHA-1 comparison is not a preferred authenticity check. See the [digest manual](https://docs.openssl.org/3.5/man1/openssl-dgst/).

For a legacy `openssl passwd` stage or archive-key pipeline, read [crypt-record bytes](references/crypt-record.md).

For an AES-CBC artifact with independently established raw-key settings, a legacy OpenSSL password container or a CryptoJS password envelope, use [known-format CBC decryption](references/aes-cbc.md). Base64 text or a field named `aes_key` alone does not establish that format.

For a TLS mail endpoint, use [IMAP transport and mailbox diagnosis](references/imap-tls.md) to distinguish implicit TLS, STARTTLS, protocol and authenticated mailbox state.

For PFX/P12 inspection, selected extraction or packaging an already issued owned certificate/key, use [PKCS#12 operations](references/pkcs12.md). It separates bundle passwords, encrypted key output and legacy-provider failures.

For an acquired ASN.1 section/object, read [ASN.1 structural inspection](references/asn1-structure.md) fully before interpreting tags as trust evidence.

For FTP control-channel TLS, read [FTPS handshake diagnosis](references/ftp-tls.md). For a renewal horizon, read [certificate expiry](references/certificate-expiry.md); for key serialization, owned RSA PVK conversion or rejected uploads, read [private-key inspection](references/private-key.md).

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

For a trust-directory layout explicitly requiring the old subject hash, use `openssl x509 -in "$pem_cert" -noout -subject_hash_old`. This is a subject-name lookup key, not the certificate fingerprint or a trust decision. Hash collisions use numbered suffixes such as `.0`, `.1`; inspect existing entries rather than overwriting `.0`. The platform's store format, permissions and actual application trust policy remain separate. Format conversion and a matching filename do not install trust.

Define `ca_bundle` as independently trusted CA certificates and `intermediates` as the supplied intermediate chain:

~~~bash
openssl verify -CAfile "$ca_bundle" -untrusted "$intermediates" "$cert"
~~~

Omit `-untrusted` if no intermediate file is needed. Choose the intended verification purpose/hostname options when applicable; a generic chain check does not establish that Kerberos, TLS client authentication or a specific service will accept the certificate. An `OK` result is relative to the configured trust inputs and verification options, not proof that a CA is trustworthy. Revocation checking also needs explicit applicable data/options.


Resolve certificate-option differences with the [request](https://docs.openssl.org/3.5/man1/openssl-req/), [certificate](https://docs.openssl.org/3.5/man1/openssl-x509/) and [verification](https://docs.openssl.org/3.5/man1/openssl-verify/) manuals.
