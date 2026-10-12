---
name: gpg
description: Decrypt a selected OpenPGP backup or create and verify a detached signature for an owned ordinary file with GnuPG. Use to resolve key requirements, pinentry failures, partial plaintext and signer identity.
---


# Select the OpenPGP operation

Read this entire SKILL.md before acting. For decryption, establish the ciphertext, encryption type and required key/passphrase, then finish with status evidence and validated plaintext. For an owned ordinary file's detached signature and selected public-key export, read [detached signatures](references/detached-signatures.md) fully first; finish with verification of the exact bytes and expected signer. Missing usable key material or failed validation remains unresolved.

For recovery from an owned backup containing a GnuPG home, read [backup key-home recovery](references/key-home.md) fully first. Keep that branch unloaded when using the current trusted keyring or a symmetric passphrase.

Define `ciphertext` as the existing acquired encrypted-file copy before using the commands below.

Use GnuPG's installed `gpg --version`. A `.gpg` extension or `.gnupg` directory does not identify the object's encryption type or prove a usable private key exists. For a selected working copy, inspect packet metadata when this distinction is unknown:

~~~bash
gpg --list-packets "$ciphertext"
~~~

A symmetric-key encrypted session-key packet indicates a passphrase route; a public-key encrypted session-key packet identifies recipient-key requirements. Metadata inspection can still prompt or emit errors. Public-key decryption needs the matching secret key or configured token, plus its unlocking mechanism. A symmetric message does not require a private key. No exposed private key therefore does not rule out testing a known passphrase on a symmetric backup.

For a public-key message, a recipient can identify an encryption subkey rather than the primary key. `gpg --list-keys` lists public material and does not establish a usable secret key. Inspect the intended current keyring with `gpg --list-secret-keys --with-subkey-fingerprint`; compare the encryption subkey and its primary-key fingerprint with trusted recipient evidence. A short key ID or display name alone is insufficient to establish identity. A `secret key not available` diagnostic applies to this invocation's keyring/token context; supplying an unlocking passphrase cannot replace a missing secret key. Inspect on the intended recovery account instead of assuming every host's GnuPG installation shares keys.

For an interactive known-passphrase decryption, define `plaintext` as a fresh private output path:

~~~bash
umask 077
gpg --output "$plaintext" --decrypt "$ciphertext"
~~~

For an approved unattended run, define `passphrase_file` as a protected existing file containing the intended passphrase on its first line, with `status_file` and `error_file` fresh paths:

~~~bash
umask 077
gpg --batch --pinentry-mode loopback --passphrase-fd 3 \
  --status-fd 4 --output "$plaintext" --decrypt "$ciphertext" \
  3<"$passphrase_file" 4>"$status_file" 2>"$error_file"
~~~

This separates status, diagnostics and plaintext, and avoids a literal secret argument. GnuPG 2.1+ needs loopback with these passphrase controls; the agent's policy can still disallow loopback. Do not alter global agent settings to hide that failure. Omit `--yes` so an existing output is not silently overwritten; in batch mode this fails rather than asking. An agent cache may supply an already unlocked key/passphrase, so record that context when assessing a specific candidate.

Require a successful exit and relevant decryption/integrity status before using plaintext; a failed run can leave partial bytes. A decrypted SQL dump is text evidence: inspect schema, COPY column order and account-to-verifier rows without executing/restoring it. A database credential reused as an encryption passphrase establishes this object's decryption only; a later application or directory login is a separate selected-account check. Keep ciphertext, diagnostics and recovered material private.

See the [GnuPG command/status and passphrase options](https://www.gnupg.org/documentation/manuals/gnupg26/gpg.1.html) and [agent loopback policy](https://gnupg.org/documentation/manuals/gnupg-devel/Agent-OPTION.html).
