---
name: netpgp
description: Recover a selected owned OpenPGP backup with netpgp and its matching existing secret key. Use when the installed client is netpgp rather than GnuPG and an output-permission failure must be separated from key or decryption failure.
---

# Decrypt the selected owned backup

Read this entire SKILL.md before acting. Require the acquired ciphertext, trusted installed netpgp implementation, matching existing secret key and its unlocking mechanism. All steps are inline. Finish with the client/key selection, command status and validated plaintext; a created output file alone is incomplete.

Define `ciphertext` as an absolute acquired-file path. Confirm the installed implementation and inspect packet metadata when the format or recipient is unknown:

~~~bash
netpgp --version
netpgp --list-packets "$ciphertext"
~~~

An `.enc` suffix does not establish OpenPGP format. Public-key encryption requires the matching secret key; a directory containing public and secret keyring filenames does not prove that match. Packet inspection is not successful decryption and can fail on unsupported input. This procedure assumes the current trusted key home is already configured; netpgp's `--homedir` contract is not interchangeable with GnuPG's. Modern GnuPG key storage is not automatically compatible with a legacy netpgp keyring.

Define `output_dir` as a fresh absolute path inside an owned private working area and `plaintext` as a child path inside it. Create the directory before writing sensitive plaintext:

~~~bash
umask 077
mkdir -m 700 "$output_dir" && netpgp --decrypt --output="$plaintext" "$ciphertext"
~~~

Supply any required passphrase through the client's interactive prompt. Capture the final exit status and diagnostics separately from plaintext. A directory-creation failure means decryption did not run. Output `Permission denied` concerns the selected output pathname; changing the current directory can change a relative output location without changing which home/keyring the client uses. Inspect the parent directory itself rather than inferring its permissions from a listing of its children.

If decryption fails, retain any output as partial and resolve the specific key, passphrase, format or write error before accepting it. A printed RSA key identity is not proof of a completed decrypt. Unsupported packets or key storage require a compatible recovery client; do not import or rewrite the original key material as a speculative repair.

Validate the recovered file according to its intended format. For an archive, list it and check the listing's final status before selecting members for extraction into a separate fresh directory. A successful decrypt does not prove a complete archive, an authenticated signer or the trustworthiness of recovered scripts. Preserve the original ciphertext and identify the resulting artifact without copying secrets into the report.

References: [netpgp command and key-home contract](https://man.netbsd.org/netpgp.1), [portable package](https://ftp.netbsd.org/pub/pkgsrc/current/pkgsrc/security/netpgp/index.html).
