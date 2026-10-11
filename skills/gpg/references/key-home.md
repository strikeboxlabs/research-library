# Select the backup's key home deliberately

Use a private working copy of an owned GnuPG-home backup. Retain its original bytes; review copied configuration and agent/pinentry settings before using it. Never replace the operator's ordinary keyring. Define `key_home` as the complete working-copy directory and `ciphertext`, `plaintext`, `status_file`, `error_file` as the selected ciphertext and fresh private output paths.

~~~bash
umask 077
gpg --homedir "$key_home" --no-options --with-colons --list-secret-keys
gpg --homedir "$key_home" --no-options --no-auto-key-retrieve \
  --status-fd 4 --output "$plaintext" --decrypt "$ciphertext" \
  4>"$status_file" 2>"$error_file"
~~~

`--homedir` overrides `GNUPGHOME`; `--no-options` skips gpg's default options file, not every agent configuration. Compare recipient requirements with the key listing. A `private-keys-v1.d` filename alone does not establish a usable decryption key; public metadata, matching secret subkey and its unlocking mechanism matter together.

An agent or pinentry failure, missing key or incompatible backup format needs its own diagnosis. Moving the same key files locally does not explain why an earlier decryption failed. Keep that cause unresolved without the actual diagnostics. Require successful decryption/integrity status and validate plaintext privately; do not infer current account access from recovered text.

See [GnuPG options](https://www.gnupg.org/documentation/manuals/gnupg26/gpg.1.html) and [agent options](https://www.gnupg.org/documentation/manuals/gnupg/Agent-Options.html).
