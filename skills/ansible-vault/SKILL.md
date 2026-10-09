---
name: ansible-vault
description: Inspect and decrypt existing Ansible Vault files or extracted inline vault values. Use when YAML wrappers, vault IDs, credential helpers or confusing encrypted values with password hashes blocks inspection.
---

# Inspect the vault object without running the playbook

Use the `ansible-vault` CLI supplied by Ansible/ansible-core; the executable's name does not establish which similarly named Python package provides it. Check `ansible-vault --version`, including its reported configuration path. Work from a clean task directory: do not inherit an unreviewed role's `ansible.cfg`, executable vault-password helper or Jinja lookups merely to inspect data.

Distinguish a fully encrypted file from YAML containing individual `!vault |` values. For an inline value, copy just one complete `$ANSIBLE_VAULT;...` header and its ciphertext lines to a new working file, removing YAML indentation and preserving the header/version/optional vault ID. Keep the variable-name mapping separately. Do not concatenate several values or remove arbitrary internal characters.

Define `vault_file` as that complete vault object and `plaintext` as a fresh private output path. With the known vault password:

~~~bash
umask 077
ansible-vault decrypt --ask-vault-pass --output "$plaintext" "$vault_file"
~~~

`decrypt` without `--output` normally replaces an input file with plaintext. For temporary viewing, `ansible-vault view --ask-vault-pass "$vault_file"` leaves the encrypted input intact but displays its secret content through a pager. `edit` opens an editor and re-encrypts changes; it is not a read-only inspection command. A named vault can use the corresponding `--vault-id label@prompt`; the label identifies which secret to try, not the secret itself.

A vault password unlocks the encrypted value, which may be a username, application password or arbitrary data. Recovering that password does not establish a valid application login. Multiple encrypted values can share a vault password while holding different plaintext.

For an authorized offline password audit, the Jumbo `ansible2john.py` converter accepts the extracted vault object. Its output includes a filename label before `$ansible$`; retain that mapping and remove only the label when a consumer requires an unlabeled record. Confirm complete output and diagnostics: malformed input can yield no record without a useful exit failure. Verify a candidate by decrypting the original-format working copy, without executing its contents.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Authority pp. 5–8. Sources: [CLI](https://docs.ansible.com/ansible/latest/cli/ansible-vault.html), [file and variable encryption](https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html), [converter](https://github.com/openwall/john/blob/bleeding-jumbo/run/ansible2john.py).
