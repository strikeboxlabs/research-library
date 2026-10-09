---
name: ssh-keygen
description: Inspect OpenSSH key identity and derive public keys without modifying private-key artifacts. Use when fingerprints, public/private encodings, certificates or parser failures are being confused.
---

# Establish key identity before changing format

Identify the artifact: an OpenSSH public-key line, OpenSSH private-key envelope, PEM/PKCS key or SSH certificate requires different handling. The filename, comment and base64 appearance do not establish the type. Keep an original private-key artifact unchanged and restrict working-copy access.

Define `private_key` as an existing absolute private-key path and `public_copy` as a fresh output path in a private directory:

~~~bash
umask 077
(set -C; ssh-keygen -y -f "$private_key" > "$public_copy") && ssh-keygen -l -E sha256 -f "$public_copy"
~~~

`-y` reads the private key, prompting for its passphrase when needed, and writes its public counterpart. It does not change the source. If derivation fails, the redirected file may exist but be empty or partial; do not accept it as a usable result. The no-clobber subshell prevents replacing an existing output.

Compare the resulting SHA-256 fingerprint with the independently obtained public key using the same `-l -E sha256` options. Comments can differ without changing key identity. A fingerprint identifies key material; it does not prove who owns the key or that any server currently authorizes it. `ssh-keygen -L -f` inspects an SSH certificate's principals, validity and restrictions; those are distinct from the underlying key fingerprint and server trust policy.

On `invalid format`, check object type, complete delimiters, wrapping and transfer integrity before regenerating anything. An OpenSSH `openssh-key-v1` private-key envelope contains length-prefixed metadata and key data; it is not simply the public-key base64 field or an interchangeable ASN.1 object. Hardcoded byte offsets from a particular key are not a portable parser. Prefer supported parsing/conversion over hand-editing lengths or key integers.

Keep `-p` passphrase changes and key regeneration separate from inspection: they can modify or replace artifacts. Do not copy a writeup's unusually large RSA key size as an operational requirement. An SSH server's `AuthorizedKeysCommand` `%k` token supplies the offered **public** key/certificate blob, not the user's private key; a copied configuration still needs independent confirmation on the actual server.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Attended pp. 18–21, 26–31. Sources: [ssh-keygen](https://man.openbsd.org/ssh-keygen.1), [OpenSSH private-key format](https://github.com/openssh/openssh-portable/blob/master/PROTOCOL.key), [sshd tokens](https://man.openbsd.org/sshd_config.5#TOKENS).
