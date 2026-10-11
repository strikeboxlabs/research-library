---
name: npm
description: Inspect npm package versions or install selected exact dependencies and run a reviewed build in an owned project. Use when package attribution, lockfiles or generator/build differences affect reproducibility.
---

# Attribute the installed package

Read this entire SKILL.md before acting. Select inventory below or, for an approved dependency change/build, read [project installation and build](references/project-build.md) fully first. Establish the selected project/package and required artifact. Finish with observed versions and diagnostics, plus actual build status/artifacts when requested; inventory alone is not an executed behavior.

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
