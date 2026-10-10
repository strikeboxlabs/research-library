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
| `user@host's password:` | Server password authentication, possibly after key authentication failed. Do not assume the local key passphrase is the account password. |
| `Permission denied (publickey)` | Server authentication failed. Check actual endpoint, account, offered key and server policy rather than repeatedly changing the key's passphrase. |
| `Authenticated ... using "publickey"` in verbose output | Key authentication succeeded; shell/command access remains subject to server restrictions. |

For a bounded diagnostic retry use `-v` with the same intended connection. `BatchMode=yes` suppresses interactive password/passphrase questions, so an encrypted key needing a prompt can fail in a worker although it works interactively. Use the deployment's approved unlocked-agent/key mechanism rather than embedding a passphrase in arguments. A web application's login success establishes that service/account only.

References: [identity selection and prompts](https://man.openbsd.org/ssh.1), [IdentitiesOnly, IdentityFile and BatchMode](https://man.openbsd.org/ssh_config.5).
