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
