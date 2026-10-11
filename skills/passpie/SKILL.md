---
name: passpie
description: Export an owned initialized Passpie vault with a known master passphrase while preserving database selection, private output and export-failure evidence.
---

# Export an owned password vault

Read this entire SKILL.md before acting. Require an authorized initialized local vault, its existing GnuPG key material, a known master passphrase and trusted Passpie/GnuPG dependencies. Read the selected vault and user configuration before invoking a database command. Finish with the selected vault, export status, format and verified record count; keep credential values out of the report. A missing key/passphrase is an unresolved prerequisite.

Use installed `passpie --version`, `passpie --help` and `passpie export --help` to confirm its interface. Select the vault with `-D` before the subcommand. Inspect effective path, recipient/keyring and `autopull` configuration: a local vault's configuration can override supplied settings, and automatic Git retrieval can occur during database setup. Require the intended local path and no automatic remote synchronization for this export task. A `.passpie` directory or public-key block alone does not establish usable decryption material.

Define `vault` as that existing absolute database directory and `outdir` as a new private absolute directory outside the vault and synchronized trees. Define `export_file="$outdir/passwords.db"`. Create the directory and export only if creation succeeds:

~~~bash
umask 077
if mkdir -m 700 -- "$outdir"; then
    passpie -D "$vault" export "$export_file"
fi
~~~

Enter the known master passphrase at the hidden prompt. Export decrypts **all** records into plaintext YAML; it is not an encrypted backup, and the filename suffix does not select a database format. Do not put the passphrase on the command line. Existing destinations can be truncated by the output writer, so retain the fresh directory rule even for retries. Preserve status immediately: `Wrong passphrase` or a dependency/recipient error leaves the export incomplete, and an empty or partial destination can still exist. Resolve the named prerequisite before retrying to a new destination.

Check the output privately for its Passpie handler/version, record structure and expected account names/count, without copying passwords into logs or chat. Legacy YAML can include Python-specific tags; inspect it as text or select a confirmed JSON-capable version rather than using an unsafe YAML object loader. When installed help lists `--json`, `passpie -D "$vault" export --json "$export_file"` produces JSON even with the same suffix; validate it with a standard JSON parser. Successful parsing alone does not prove expected vault coverage.

Record where the plaintext export is retained and follow the task's agreed transfer/retention requirements. A vault record named `root@ssh` describes a saved credential; it does not establish current OS authentication or privilege. GnuPG key import/setup effects are separate from export contents. Do not initialize, reset or purge an existing vault to fix an export error.

See [Passpie database selection/export/keyring documentation](https://passpie.readthedocs.io/en/latest/getting_started.html) and the [CLI export implementation](https://github.com/marcwebbie/passpie/blob/master/passpie/cli.py) for version differences.
