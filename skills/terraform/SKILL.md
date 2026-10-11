---
name: terraform
description: Apply a reviewed Terraform configuration in an existing initialized controlled workspace and interpret provider overrides, no-change results and partial failures. Use when selecting the directory alone does not establish the effective provider or apply effects.
---

# Apply the selected configuration

Read this entire SKILL.md before acting. Require the initialized workspace, reviewed configuration/providers, selected backend/workspace and permission for the proposed effects. All task instructions are inline. Finish with status, diagnostics, resource changes and the requested resulting artifact/state; an output pathname alone does not prove its contents.

Define `directory` as the selected existing absolute root-module directory. Confirm `terraform version`. Review the complete configuration, effective inputs, backend and executable provider context before applying. `main.tf` is only a conventional filename; other module files also contribute. Missing initialization or unknown infrastructure ownership is a prerequisite gap.

~~~bash
terraform -chdir="$directory" apply
status=$?
~~~

The global `-chdir` precedes the subcommand. It selects ordinary module-relative reads/writes, but CLI configuration is processed before that change and `path.cwd` remains the original directory. Do not infer effective CLI settings from the selected module directory alone.

A provider development-override warning means apply can use a local build instead of the dependency lockfile selection/checksums. Establish that build's provenance and intended behavior before continuing; do not remove the warning or run init merely to conceal it.

Without a saved plan, apply plans and requests approval for changes. Read that concrete proposal before entering yes; replacement includes destruction and creation. A no-change result can still involve provider refresh. Inspect the requested artifact separately. Lock/access/provider errors are failures to resolve, not reasons to disable locking or elevate the process blindly. Failed apply can leave partial changes; inspect state and effects before retrying because rollback is not automatic.

References: [apply](https://developer.hashicorp.com/terraform/cli/commands/apply), [directory selection](https://developer.hashicorp.com/terraform/cli/commands), [provider override semantics](https://developer.hashicorp.com/terraform/cli/config/config-file#development-overrides-for-provider-developers).
