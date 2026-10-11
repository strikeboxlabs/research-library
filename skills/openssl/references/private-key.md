# Diagnose a rejected PEM private key

For an existing private working-copy `key`, check the key without printing its private components:

~~~bash
openssl pkey -in "$key" -noout -check
openssl pkey -in "$key" -noout -text_pub
~~~

Retain the first command's status and diagnostic. An encrypted input can prompt for its passphrase; an unreadable/encrypted/unsupported object is not necessarily an invalid key pair. `-text_pub` exposes only public components; plain `-text` would expose private ones. Successful consistency checking does not establish the key owner's identity or application compatibility.

Distinguish the algorithm from its serialization. `BEGIN RSA PRIVATE KEY` normally labels traditional PKCS#1 RSA, `BEGIN PRIVATE KEY` unencrypted PKCS#8, and `BEGIN OPENSSH PRIVATE KEY` the OpenSSH container. The generating program's name does not settle compatibility. OpenSSL 3 `genrsa` defaults to PKCS#8; `-traditional` requests PKCS#1. Check the receiving application's exact accepted format before converting or replacing a key. Never infer that an old command produces the same header under a newer version.

A PEM parser may accept unrelated text outside the key boundaries. A successful key check therefore does not validate every input byte or establish that storing the whole uploaded file is safe. For an application that reserializes keys, compare the public components and separately inspect the saved representation; preservation of key identity does not imply byte-for-byte preservation. A failed upload alone does not prove a particular patch is installed.

Resolve format and option questions with the [pkey manual](https://docs.openssl.org/3.5/man1/openssl-pkey/), [genrsa manual](https://docs.openssl.org/3.5/man1/openssl-genrsa/) and [PEM textual-encoding rules](https://www.rfc-editor.org/rfc/rfc7468.html#section-2).

## Convert an owned RSA PVK working copy

PVK is a private-key container, distinct from a DER certificate. Confirm the object and local `openssl rsa` support before conversion; its help/manpage format list can omit PVK input even when the build accepts it. An unsupported decoder/provider or an incorrect passphrase is a compatibility/input failure, not evidence that the corresponding certificate is invalid. Do not regenerate or acquire another person's key to resolve it.

Define `pvk` as the owned RSA PVK copy and `pem_key` as a fresh output in a private directory:

~~~bash
umask 077
openssl rsa -inform PVK -in "$pvk" -outform PEM -aes256 -out "$pem_key"
~~~

Enter any required input passphrase and the new PEM passphrase at their prompts. Keep the output encrypted and check the conversion status before running `openssl pkey -in "$pem_key" -noout -check`. Compare public components with the original key or intended issued certificate when a matching identity matters. Conversion preserves key material; it does not grant access to encrypted files, install a certificate, or establish trust. PVK output flags such as `-pvk-none` do not request encrypted PEM output.

Use the [RSA manual](https://docs.openssl.org/3.5/man1/openssl-rsa/) and the matching build's help/format loader for differences; do not assume PVK support from the filename or from a successful conversion on another image.
