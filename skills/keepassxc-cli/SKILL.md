---
name: keepassxc-cli
description: Inspect an authorised KeePass database using a known key file or password. Use to select exact entries and fields, distinguish missing unlock factors from missing entries, and avoid unnecessary whole-database exports.
---

# Inspect a database with known unlock factors

Read this entire SKILL.md before acting. Require the trusted installed CLI, an authorized database working copy and its known required unlock factors. Select key-only, password-plus-key or password-only options before listing; retain the same factor selection for the requested exact entry/fields. No conditional resources are required. Finish with unlock/lookup status and selected stored-field evidence; missing factors or format support remain unresolved, and stored content does not establish current remote authentication.

Check `keepassxc-cli --version` and `keepassxc-cli help show`. Define `database` and `keyfile` as absolute paths to private working copies. A nearby `.key` file is a candidate unlock factor; its name does not establish that it belongs to this database or replaces a password.

For a database known to use **only a key file**:

~~~bash
keepassxc-cli ls --no-password -k "$keyfile" "$database"
~~~

`--no-password` omits the password component of the composite key; it does not bypass a required password. For password plus key file, omit that option and answer the prompt. For password only, also omit `-k`. Do not place a password in a command argument.

Use an observed group path with `ls` to narrow the listing. Set `entry` to the exact group-qualified path; duplicate leaf names can select an unintended entry. Retrieve only the fields needed:

~~~bash
keepassxc-cli show --no-password -k "$keyfile" -a UserName -a URL "$database" "$entry"
~~~

Explicit `-a` fields are printed in the specified order, without field labels. They can reveal protected values even without `--show-protected`: selecting Password or a sensitive custom field is a disclosure decision. A broad default summary can also expose Notes; prefer precise fields. Use the same unlock-factor options on each command.

If unlocking fails, check the exact database copy, key-file bytes, required factors and supported format/KDF before concluding corruption. If unlock succeeds but entry lookup fails, inspect the group/path spelling. A missing TOTP configuration differs from a wrong current code. Successful local retrieval establishes stored content, not current remote credentials or hostname resolution. Avoid whole-database `export` or clipboard output for a single-field task.

Resolve version differences with the [CLI manual](https://github.com/keepassxreboot/keepassxc/blob/develop/docs/man/keepassxc-cli.1.adoc) and [field-display implementation](https://github.com/keepassxreboot/keepassxc/blob/2.7.10/src/cli/Show.cpp).
