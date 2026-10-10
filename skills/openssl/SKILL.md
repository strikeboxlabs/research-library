---
name: openssl
description: Inspect certificates, keys, TLS mail sessions and known-format AES-CBC artifacts with OpenSSL. Use for trust, protocol selection, serialization, padding and incomplete-output decisions.
---

# OpenSSL inspection

Record `openssl version` and inspect subcommand help. Identify whether the input is a CSR, certificate, private key or bundle; a `.cer` extension alone does not distinguish DER from PEM. Work on copies and choose fresh output paths.

For an AES-CBC artifact with independently established raw-key settings or a CryptoJS password envelope, use [known-format CBC decryption](references/aes-cbc.md). Base64 text or a field named `aes_key` alone does not establish that format.

For a TLS mail endpoint, use [IMAP transport and mailbox diagnosis](references/imap-tls.md) to distinguish implicit TLS, STARTTLS, protocol and authenticated mailbox state.

For a PFX/P12 containing certificates and private keys, use [PKCS#12 inspection and extraction](references/pkcs12.md). It separates bundle passwords, encrypted key output and legacy-provider failures.

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

## Distinguish approaching expiry from a failed check

For an existing PEM `cert` and a nonnegative integer `seconds` defining the renewal horizon, first require successful parsing and retain the dates:

~~~bash
if openssl x509 -in "$cert" -noout -dates -subject; then
    if openssl x509 -in "$cert" -noout -checkend "$seconds"; then
        printf 'Certificate expiry is beyond the selected horizon.\n'
    else
        printf 'Nonzero check: inspect expiry result and diagnostics.\n'
    fi
else
    printf 'Certificate could not be inspected; expiry is unresolved.\n' >&2
fi
~~~

`-checkend 86400` asks whether `notAfter` falls within the next 86,400 seconds, relative to the checking host's clock. For a valid parsed certificate, zero means it does not expire within that horizon; nonzero is also possible for malformed/unreadable input or invocation errors. Do not route every failure into renewal. Keep the exact diagnostic and parsed `notAfter` together. The illustrative messages above are workflow labels, not captured OpenSSL output.

This checks expiry, not `notBefore`, chain trust, hostname or the service's currently loaded certificate. A one-day self-signed fixture soon falls inside a one-day horizon; it does not establish trusted issuance. Treat subject/CN strings as untrusted data when passing them to a renewal script or constructing filenames. Certificate parsing does not itself execute shell syntax embedded in a name.

For certificate-based login, confirm the matching private key exists and is readable by the intended process without printing it. Record certificate fingerprints and verification diagnostics, not private-key contents.

Resolve certificate-option differences with the [request](https://docs.openssl.org/3.5/man1/openssl-req/), [certificate](https://docs.openssl.org/3.5/man1/openssl-x509/) and [verification](https://docs.openssl.org/3.5/man1/openssl-verify/) manuals.

## Diagnose a rejected PEM private key

For an existing private working-copy `key`, check the key without printing its private components:

~~~bash
openssl pkey -in "$key" -noout -check
openssl pkey -in "$key" -noout -text_pub
~~~

Retain the first command's status and diagnostic. An encrypted input can prompt for its passphrase; an unreadable/encrypted/unsupported object is not necessarily an invalid key pair. `-text_pub` exposes only public components; plain `-text` would expose private ones. Successful consistency checking does not establish the key owner's identity or application compatibility.

Distinguish the algorithm from its serialization. `BEGIN RSA PRIVATE KEY` normally labels traditional PKCS#1 RSA, `BEGIN PRIVATE KEY` unencrypted PKCS#8, and `BEGIN OPENSSH PRIVATE KEY` the OpenSSH container. The generating program's name does not settle compatibility. OpenSSL 3 `genrsa` defaults to PKCS#8; `-traditional` requests PKCS#1. Check the receiving application's exact accepted format before converting or replacing a key. Never infer that an old command produces the same header under a newer version.

A PEM parser may accept unrelated text outside the key boundaries. A successful key check therefore does not validate every input byte or establish that storing the whole uploaded file is safe. For an application that reserializes keys, compare the public components and separately inspect the saved representation; preservation of key identity does not imply byte-for-byte preservation. A failed upload alone does not prove a particular patch is installed.

Resolve format and option questions with the [pkey manual](https://docs.openssl.org/3.5/man1/openssl-pkey/), [genrsa manual](https://docs.openssl.org/3.5/man1/openssl-genrsa/) and [PEM textual-encoding rules](https://www.rfc-editor.org/rfc/rfc7468.html#section-2).
