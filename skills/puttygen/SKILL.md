---
name: puttygen
description: Convert an existing authorized PuTTY private key to an OpenSSH file and compare its public fingerprint. Use when a PPK file is incompatible with the selected SSH client.
---

# Convert the existing key

Read this entire SKILL.md before acting. Establish the authorized input key, its known passphrase if encrypted, the required output format and a fresh destination in a private directory. Finish with the conversion status, readable output and matching public fingerprint; report missing format support separately.

Define `key` as the existing absolute PPK path and `output` as a different, unused absolute path in a directory controlled by the worker:

~~~bash
puttygen --version
puttygen --help
puttygen "$key" -l -E sha256
umask 077
if [ ! -e "$output" ] && [ ! -L "$output" ]; then
    puttygen "$key" -O private-openssh -o "$output"
fi
~~~

Supply the known passphrase interactively. The destination check assumes a private directory without competing writers; if it already exists, choose a fresh path. Check the conversion status immediately and reject empty or partial output after failure. The explicit `-o` avoids PuTTYgen's possible in-place rewrite when retaining the input format. Do not print private material to verify it.

`private-openssh` selects the oldest supported OpenSSH encoding; `private-openssh-new` forces the newer encoding. Choose for the receiving client's support, rather than a filename. Confirm PPK version support in the installed tool. A public-only input cannot yield a private key. This task changes representation, not key identity; omit key generation and passphrase-change options.

Read the resulting public fingerprint with `puttygen "$output" -l -E sha256` and compare the same algorithm with the input. Record output permissions and encryption status without exposing the key. A matching fingerprint does not establish server authorization.

See the [PuTTYgen manual](https://manpages.debian.org/testing/putty-tools/puttygen.1.en.html) for format and output behavior.
