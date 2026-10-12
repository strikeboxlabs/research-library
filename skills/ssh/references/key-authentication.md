# Separate key unlocking from server authentication

Define `key` as the authorized private key's local working-copy path, and `ssh_host`, `ssh_port` and `user` as the verified destination/account. Protect the working key from other users; on Linux an overly accessible private key can be refused. Preserve the source artifact separately. Review effective client settings and helper behavior before connecting, as described in [client commands](client-commands.md) when that configuration is unfamiliar.

For an intended interactive login with that key:

~~~bash
ssh -p "$ssh_port" -i "$key" -o IdentitiesOnly=yes "$user@$ssh_host"
~~~

`-p` selects the SSH service, not a forwarded application port. Two SSH listeners on the same IP can be different services with different accounts and host keys. Keep host-key verification; a Git-hosting SSH endpoint need not provide an ordinary OS shell.

`-i` selects an identity file; `IdentitiesOnly=yes` limits offers to configured identities instead of every agent-held key. Other configured IdentityFile entries can still apply. A known configuration and verbose authentication trace help establish which identity was offered and accepted; the flag alone does not prove exclusivity or success.

| Observation (illustrative) | Meaning and next decision |
|---|---|
| `Enter passphrase for key ...` | Local key decryption. It is not the remote account's password prompt; successful unlocking does not prove server acceptance. |
| `user@host's password:` | Server authentication: either fallback after a key failure or a required additional factor. Check the preceding trace; the local key passphrase is not this credential. |
| `Authenticated ... with partial success` | One method succeeded, but policy still requires another. Preserve the accepted identity and inspect the remaining methods; do not replace the key merely because another prompt follows. |
| `Permission denied (publickey)` | Server authentication failed. Check actual endpoint, account, offered key and server policy rather than repeatedly changing the key's passphrase. |
| `Authenticated ... using "publickey"` in verbose output | Key authentication succeeded; shell/command access remains subject to server restrictions. |

For a bounded diagnostic retry use `-v` with the same intended connection. `BatchMode=yes` suppresses interactive password/passphrase questions, so an encrypted key needing a prompt can fail in a worker although it works interactively. Use the deployment's approved unlocked-agent/key mechanism rather than embedding a passphrase in arguments. A web application's login success establishes that service/account only.

A server policy such as `AuthenticationMethods publickey,password` requires both methods in order. Space-separated lists are alternative acceptable sequences; check applicable Match blocks and the authentication backend. A password-shaped prompt can request an OTP; keyboard-interactive can also carry challenge/response. Establish the actual configured factor before selecting a tool: Yubico OTP is not OATH TOTP, and a generic TOTP generator cannot substitute for it. Report completed authentication separately from partial success.

A private key stored in an account's home directory does not establish that its corresponding public key is authorized for incoming login. That key may instead be an outbound identity. Check the account's actual key authorization source, key restrictions, ownership/modes and applicable server policy. `PubkeyAuthentication yes` allows the method, not every key. `PermitRootLogin prohibit-password` disables root password and keyboard-interactive authentication; it does not itself authorize a particular root key or promise an unrestricted shell.

For a server using `AuthorizedKeysCommand`, follow the selected helper, arguments and `AuthorizedKeysCommandUser` as well as file-based keys. A helper can retrieve keys from a directory backend; a visible LDAP key attribute does not prove the installed helper's mapping, return value or server acceptance. The helper's execution account is separate from the authenticated user's eventual shell identity. Review acquired configuration and existing authentication traces without executing an unreviewed helper or editing directory attributes to test acceptance. Current OpenSSH tries the helper after ordinary key files when no matching key has succeeded; verify the deployed release rather than applying a historical source excerpt's lookup order universally.

An authorized_keys comment such as `name@machine` is an editable label; OpenSSH does not use it to authenticate that named person or host. Its appearance in one account's file does not establish the same private key is shared or accepted for a second account. Keep actual key material, the destination account's authorization and the observed accepted identity separate. See the [authorized-key format](https://man.openbsd.org/sshd.8#AUTHORIZED_KEYS_FILE_FORMAT).

## An already issued user certificate

Require the intended certificate, its corresponding authorized private key and verified endpoint/account. Inspect the certificate's type, underlying key, CA, principals, validity and restrictions before the connection. Define `certificate` as the selected absolute path:

~~~bash
ssh -p "$ssh_port" -i "$key" -o "CertificateFile=$certificate" -o IdentitiesOnly=yes "$user@$ssh_host"
~~~

`CertificateFile` selects the certificate separately from the private identity. Without an explicit certificate setting, OpenSSH normally tries the identity path with `-cert.pub` appended. That convention does not require all artifacts to share a directory. A downloaded response named `.pub` may instead be an API error; parsing and key association remain prerequisites.

For a CA trusted through `TrustedUserCAKeys`, inspect the applicable `AuthorizedPrincipalsFile`, `AuthorizedPrincipalsCommand` and account policy. With neither principal source configured, the requested username must appear in the certificate's principals; absence of a principals file does not disable identity checking. With an explicit principal source, an accepted principal can differ from the OS username; `%u` expands to the requested account. A principal-list file is neither a list of all OS accounts nor a complete effective daemon configuration. Validity, revocation, critical options and other account/authentication restrictions still apply. An exposed CA private key compromises the issuing authority; it is a different failure from accepting an unsigned identity claim. Preserve public fingerprints and permission evidence for incident response without issuing a test certificate.

`PasswordAuthentication no` disables that method; it alone does not establish certificate-only authentication. Preserve whether the certificate was offered, accepted and followed by an authorized session; keep host-key verification and close the selected session afterward.

References: [certificate selection](https://man.openbsd.org/ssh_config.5#CertificateFile), [certificate principals and server policy](https://man.openbsd.org/sshd_config.5#AuthorizedPrincipalsFile).

A grep of two keywords in one configuration file can select commented lines and miss `Include`, applicable `Match` blocks, other authentication/account restrictions or a daemon started with a different configuration. Preserve the selected file as evidence, but establish the running service's configuration and relevant connection context before reporting effective policy. Use readable deployed configuration and administrator-provided effective settings when available; do not restart or alter the daemon merely to diagnose a client failure.

References: [required methods](https://man.openbsd.org/sshd_config#AuthenticationMethods), [server key authorization and policy](https://man.openbsd.org/sshd_config), [identity selection and prompts](https://man.openbsd.org/ssh.1), [IdentitiesOnly, IdentityFile and BatchMode](https://man.openbsd.org/ssh_config.5).
