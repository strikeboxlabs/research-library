---
name: jenkins-offline-decrypt
description: Recover supported Jenkins Secret values from an authorized offline backup using pwn_jenkins' jenkins_offline_decrypt.py. Use to match ciphertext with its controller keys and distinguish partial extraction, parser limits and invalid backup material.
---

# Match the three offline inputs

Read this entire file before acting. Work from an authorized backup copy and protect plaintext output. Finish with which fields were recovered, which were unsupported/failed and the matching backup context; do not expose recovered values in a general report.

Set `script` to the installed `pwn_jenkins/offline_decryption/jenkins_offline_decrypt.py` and `backup` to the backup root. This is a specific implementation, not every script named `decrypt.py`. It requires Python 3 and the AES module used by that installation.

The selected XML, `secrets/master.key` and `secrets/hudson.util.Secret` must belong to the same controller/key context. Preserve their original bytes and Linux filename case. For a selected job configuration, define `xml_file`, `private_output` and `private_errors` as appropriate paths:

~~~bash
umask 077
python3 "$script" "$backup/secrets/master.key" \
  "$backup/secrets/hudson.util.Secret" "$xml_file" \
  > "$private_output" 2> "$private_errors"
~~~

The utility also accepts a controller base directory, where it expects root `credentials.xml`, and an interactive mode. Supplying the three files avoids silently assuming a job's credentials live in that root file. The process writes recovered values and some diagnostics to stdout; the output is not a clean machine-readable credential table.

The confidentiality key must first decrypt with the matching master key. Failure at that stage suggests mismatched, altered or incomplete key material. At the field stage, the implementation recognizes particular XML tag patterns and Jenkins Secret encodings; plugin-specific formats, multiline values, non-UTF-8 data or a different key store may not be covered. A file with no output is not evidence that no credentials exist. A zero process exit is not proof every field decrypted: inspect each relevant result/error and preserve its source-field mapping separately.

Do not replace a malformed value with a guessed decoding or strip bytes from the original backup to make it pass. An older `tweksteen/jenkins-decrypt` script uses different code, including removed Python APIs in some revisions; identify it before diagnosing an interpreter error as corrupt ciphertext. Plaintext recovery does not establish the credential remains valid or authorize an online login.

See the [supported implementation](https://github.com/gquere/pwn_jenkins/blob/master/offline_decryption/jenkins_offline_decrypt.py) and [Jenkins secret storage](https://www.jenkins.io/doc/developer/security/secrets/).
