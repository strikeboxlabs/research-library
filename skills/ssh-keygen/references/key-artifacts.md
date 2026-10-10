# Selected key creation or transferred-key recovery

Use the applicable branch only. A new login key and an acquired private key are different artifacts; creating a replacement does not recover missing bytes or establish authorization for the original account.

## Generate a selected pair without replacing another key

Choose the key type from actual client/server policy and supported algorithms. For an explicitly selected RSA 3072-bit pair, define `new_key` as a fresh absolute basename in a private directory; ensure neither it nor its `.pub` counterpart exists:

~~~bash
umask 077
ssh-keygen -t rsa -b 3072 -f "$new_key" -C 'selected-task-key'
~~~

Choose the passphrase deliberately at the prompt. Do not accept an overwrite prompt or the default home key path just to follow a screenshot. `-f` chooses the private-key path; the public counterpart is normally written to `$new_key.pub`. RSA bit size is a choice, not proof of server compatibility; Ed25519 may be the appropriate alternative where supported. Do not assume the installed default type from a historical invocation without `-t`.

Derive the new public key using SKILL.md's `-y` procedure and compare SHA-256 fingerprints with the generated `.pub` file. Successful generation does not authorize the key remotely. If public-key enrollment is also authorized, map the actual account/filesystem, preserve existing authorized entries and add only the selected public line using the established enrollment process; never copy the private key into authorized_keys. Confirm the separate login result and track the task's intended key lifetime.

## Recover an exact key envelope from a text transport

Retain the original capture unchanged. Select only the complete begin/end envelope and its encoded lines, excluding chat prompts and unrelated output. Establish the exact prefix added by the transport, any ANSI decoration and whether the service altered line endings or truncated the read. Do not repair SNIP markers, omitted lines or an unverified prefix by guessing.

For selected lines each beginning with the literal `[SYSTEM] ` prefix, define `selected_lines` as that private capture and `candidate` as a fresh private working-copy path:

~~~bash
umask 077
(set -C; sed 's/^\[SYSTEM\] //' "$selected_lines" > "$candidate") && chmod 600 -- "$candidate"
~~~

This removes only that established leading prefix; it is not a generic transcript parser. Confirm complete delimiters, line order and final newline, then run `ssh-keygen -y -f "$candidate"` with a fresh public output file as in SKILL.md. A passphrase prompt is distinct from `invalid format`. If parsing fails, check transfer completeness and supported format before converting or generating anything. Do not use a redirected empty/partial public file as success.

Compare the derived public fingerprint with independently obtained public material when available. Parsing proves that this working copy is a supported private-key artifact; it does not prove original-byte equality after a line-based transport, owner identity, current server authorization or a later login's privilege. Keep the capture, candidate and fingerprint conclusions distinct.

See [ssh-keygen options](https://man.openbsd.org/ssh-keygen.1) and [the OpenSSH private-key format](https://github.com/openssh/openssh-portable/blob/master/PROTOCOL.key).
