---
name: minio-mc
description: Inspect selected MinIO/S3 bucket objects and retrieve an explicit owned object version with the MinIO mc client. Use when alias credentials, version history or same-name downloads obscure which bytes were acquired.
---

# Select the object and its version

Read this entire SKILL.md before acting. Require trusted installed MinIO mc, the intended owned endpoint/bucket and provisioned credentials. Establish the alias/configuration below; for version history or retrieval, read [selected object versions](references/object-versions.md) fully. Finish with the observed object/version and requested local artifact evidence, or the explicit access/transfer gap.

Define `mc_bin` as the selected MinIO client executable. The name `mc` can also identify Midnight Commander; confirm this implementation with `"$mc_bin" --version` and its local help. A downloaded filename or executable bit is insufficient provenance.

For an existing provisioned alias, define `config_dir` as its private configuration directory and `alias` as its known name. Verify the intended endpoint and credential context without printing `alias list` or exporting configuration that may contain keys. Keep server TLS verification enabled and use the deployment's trusted CA configuration; do not accept an unexpected certificate as an endpoint repair.

If configuring a new alias is part of the task, define `endpoint` as the approved HTTPS service and choose a fresh `alias` in a new private owned `config_dir`. On a client supporting interactive keys:

~~~bash
umask 077
"$mc_bin" --config-dir="$config_dir" alias set "$alias" "$endpoint" --api S3v4
~~~

Enter the provisioned access/secret keys at the prompts. This stores credentials in local configuration and may contact the server; preserve status. It is not a credential issuance or a bucket authorization result. Do not replace an existing alias or disable certificate verification to make setup succeed. A headless task needs an approved credential-input mechanism rather than putting secrets in command arguments.

For selected nonrecursive bucket inspection, define `bucket` as the exact approved bucket:

~~~bash
"$mc_bin" --config-dir="$config_dir" ls "$alias/$bucket/"
~~~

An error, empty listing and successful visible entries are different outcomes; retain the complete command result. This is scoped to that prefix and principal, not a global storage inventory or permission to read every object. A successful alias setup does not establish versioning or access to a particular key.

References: [alias implementation and prompts](https://github.com/minio/mc/blob/master/cmd/alias-set.go), [client configuration](https://docs.min.io/aistor/reference/cli/mc-global-settings/), and [object listing](https://docs.min.io/aistor/reference/cli/mc-ls/).
