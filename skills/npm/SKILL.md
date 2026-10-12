---
name: npm
description: Inspect npm package versions or registry metadata, diagnose private-registry login, install an approved global CLI, or install/build/start a reviewed owned project. Use when package attribution, prefixes, lockfiles or registry configuration affect the result.
---

# Attribute the installed package

Read this entire SKILL.md before acting; reuse complete current context. Require the trusted installed Node/npm runtime and selected project/package or approved registry task. Use inventory below; for registry metadata or an owned existing-account login, read [registry queries and authentication](references/registry-queries.md) fully first. For an approved global CLI, read [global CLI installation](references/global-cli.md) fully first. For approved project installation, build or server startup, read [project installation, build and start](references/project-build.md) fully first. These resources are conditional. Finish with observed versions and diagnostics, plus the requested registry result, installed CLI, build artifact or service readiness; missing identity/configuration/results remain unresolved.

Check `npm --version`. Define `package_name` as the selected package name. For global packages:

~~~bash
npm ls --global --depth=0 -- "$package_name"
~~~

For a selected local project, define `project` as its existing absolute directory:

~~~bash
npm --prefix "$project" ls --depth=0 -- "$package_name"
~~~

`list` aliases `ls`. Inspect status and missing/invalid/extraneous diagnostics, even when a version row appears. The tree is logical dependency context, not the physical module layout. Depth zero selects top-level inventory; a transitive package needs a deliberate deeper query. Use `--json` for structured results when supported by the installed version.

A different global prefix can describe another installation than the executable in use. Correlate the executable/wrapper with that package before attributing its behavior. Do not substitute install/update/exec for inventory. See the [npm ls manual](https://docs.npmjs.com/cli/v11/commands/npm-ls/).
