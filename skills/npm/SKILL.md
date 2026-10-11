---
name: npm
description: Inspect an installed npm package and its dependency context without installing or running it. Use when a reported package version needs attribution to a global prefix or selected project.
---

# Attribute the installed package

Read this entire SKILL.md before acting. Select global versus project scope and the exact package name. Finish with the observed version/tree and diagnostics; a version entry is not an executed behavior or complete vulnerability finding.

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
