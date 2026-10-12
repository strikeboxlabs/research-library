# Sign and verify one owned ordinary file

Require a reviewed ordinary file, an existing usable signing key in the selected trusted GnuPG home, and the independently established full primary-key fingerprint. A name or email can match several keys. Define `artifact` as the existing file, `fingerprint` as that expected full fingerprint, and `signature` and `public_key` as fresh distinct output paths. Inspect `gpg --version` and the selected key before signing:

~~~bash
gpg --list-secret-keys --with-colons --fingerprint --fingerprint "$fingerprint"
gpg --local-user "$fingerprint" --output "$signature" --detach-sign "$artifact"
gpg --verify "$signature" "$artifact"
~~~

An offline, missing or unusable secret key/subkey is a prerequisite failure, even if its public key is listed. Use the configured pinentry or token unlocking flow; do not place a passphrase in argv. Omit overwrite suppression such as `--yes`. Preserve command status and verification diagnostics. A detached signature contains no copy of the signed data: explicitly supply the original file when verifying. Renaming an archive does not change its bytes, but rebuilding or modifying it requires a new signature.

Require successful verification and the expected full signer fingerprint, resolving any signing subkey to the expected primary key. A `Good signature` message establishes a mathematical match to the selected public key, not that its displayed name is trustworthy or that the contents are harmless. Signing neither encrypts the file nor authorizes its subsequent upload or execution.

For a recipient who needs this selected public key:

~~~bash
gpg --armor --output "$public_key" --export "$fingerprint"
gpg --show-keys --with-colons --fingerprint "$public_key"
~~~

Require a successful export, nonempty output and the expected fingerprint in the inspected export. Export the selected public key, rather than the whole keyring or a secret key. Importing changes the receiving keyring; publication and account key replacement are separate operations. Finish with the original file, detached signature, verified signer and, when requested, inspected public-key artifact. Key generation is a separate provisioning task.

See [GnuPG signing, verification and export commands](https://gnupg.org/documentation/manuals/gnupg/Operational-GPG-Commands.html) for installed-version differences.
