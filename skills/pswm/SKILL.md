---
name: pswm
description: Retrieve a selected pswm password-vault alias or recover an authorized copied cryptocode vault offline. Use for XDG store selection, forgotten master passwords, tab-separated records and retrieval commands that unexpectedly rewrite the encrypted file.
---

# Select the existing vault before invoking pswm

Read this entire SKILL.md before acting. Require the identified Julynx pswm implementation and an authorized vault. The native procedure below requires the known master password and an isolated working copy; for an unknown master password, read [offline vault recovery](references/offline-vault.md) fully first. Finish with the selected record or bounded recovery result and original-file integrity; decryption is separate from any OS/application login.

The reviewed 1.5 implementation derives its store from an **existing** XDG_DATA_HOME directory, then appends pswm/pswm; otherwise it falls back to the current user's ~/.local/share/pswm/pswm. It creates directories during startup. Even alias retrieval, -a or a help-shaped invocation can authenticate and rewrite the vault with fresh encryption. Do not run it against the original just to identify its format.

Define `pswm_bin` as the trusted installed executable, `data_home` as an existing private task directory containing an already populated working copy at `pswm/pswm`, and `alias` as the exact selected stored alias. Preserve the original's bytes/hash independently. Verify this installed version's path behavior from its trusted source/documentation before relying on the override:

~~~bash
(
  export XDG_DATA_HOME="$data_home"
  "$pswm_bin" "$alias"
)
~~~

Supply the known master password at its hidden prompt. The selected Alias/Username/Password table is sensitive output, not routine telemetry. A missing alias is different from failed decryption. `pswm -a` requests all records only when that is the task. Quoting preserves spaces in an alias, but a leading dash is parsed as a flag by this implementation; do not assume a conventional -- separator exists.

Three failed master attempts offer a reset that **deletes** the selected vault; decline it when recovering existing data. An absent/empty store instead starts registration, which is evidence of the wrong context or missing data, not successful retrieval. Cancellation/unsupported arguments can still return zero; retain actual diagnostics and selected record rather than status alone. A successful read can change ciphertext without changing the logical records, so compare original integrity separately from working-copy effects.

The native storage/deletion/password-generation branches modify the selected vault and are outside this retrieval/recovery task. A record's alias/username/password is a candidate for its named service; an alias resembling a hostname does not prove an OS account or authentication. See [pswm usage](https://github.com/Julynx/pswm) and [store/parser implementation](https://github.com/Julynx/pswm/blob/main/pswm) for installed-version differences.
