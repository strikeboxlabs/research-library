# Add a controlled key through an authorized filesystem write

Use when the task explicitly includes installing a selected public key for an account, including through an already established writable host-filesystem view. File-write access and successful SSH authentication are separate results. First map the actual server/account home and effective `AuthorizedKeysFile`; a container `/root` or a mounted directory named `root` does not establish the host account. Keep the private key on its intended client.

Confirm public-key authentication, applicable Match rules, account restrictions and key type support. For root, `PermitRootLogin prohibit-password` can allow key login, `forced-commands-only` requires an appropriate forced-command key, and `no` rejects root login. Do not change that server policy merely to reproduce a walkthrough. `StrictModes` checks ownership/modes of the home, `.ssh` and key file; bytes written somewhere else are not server enrollment.

In the established account/file-write context, define `public_key` as a reviewed existing file containing **one complete public-key line**, `authorized_keys` as the mapped existing regular key file, and `backup` as a fresh private backup on the controlled working tree. Resolve symlinks and existing restrictions first. Retain original bytes and metadata. `ssh-keygen -lf "$public_key"` identifies the selected key's fingerprint; inspect the line/options too, rather than treating that command as proof of authorization. No private-key material belongs in `authorized_keys`.

For this existing-file case, after confirming the selected key is not already present:

~~~bash
test -f "$authorized_keys" && test ! -L "$authorized_keys"
test ! -e "$backup"
cp -p -- "$authorized_keys" "$backup"
printf '\n' >>"$authorized_keys"
cat -- "$public_key" >>"$authorized_keys"
~~~

Check each command before continuing. The blank line prevents joining onto a prior line lacking its final newline. The public-key file must itself contain a complete line ending. Appending preserves other key entries; `>` would replace them. Keep existing correct ownership/modes (and relevant ACL/security labels), then verify the exact added key/fingerprint and read-back in the mapped file. For a missing directory/file, use the target account's verified ownership/modes and configured path rather than this existing-file recipe. Preserve any key-specific restrictions required by the task.

Back on the intended client, define `key` as the corresponding private identity and `ssh_host`, `ssh_port`, `user` as the verified SSH endpoint/account. Keep host-key verification and inspect unfamiliar client helper/configuration behavior. For the separately authorized login/result check:

~~~bash
ssh -p "$ssh_port" -i "$key" -o IdentitiesOnly=yes "$user@$ssh_host" id
~~~

Observed authentication and returned remote identity establish this request's access; file write/read-back alone does not. A password fallback, partial authentication or failure requires checking the offered fingerprint, account/path permissions, effective server policy and endpoint, not overwriting the file again. A restricted/forced-command key may deliberately reject `id` despite key authentication.

If temporary, remove only the exact added key after the agreed task and verify the file again. Restore the backup only when no intervening legitimate changes would be lost; otherwise reconcile the added line with current content and preserve metadata. Record enrollment, login result and cleanup separately. A stopped local SSH client does not remove the server's authorized key.

See [authorized-key format and ownership](https://man.openbsd.org/sshd.8#AUTHORIZED_KEYS_FILE_FORMAT), [server authentication policy](https://man.openbsd.org/sshd_config.5) and [key inspection](https://man.openbsd.org/ssh-keygen.1).
