---
name: composer
description: Inspect PHP Composer projects, install their locked dependencies and run reviewed project scripts. Use to distinguish lockfile state, platform requirements, plugin execution and the privilege context of Composer scripts.
---

# Choose inspection, dependency installation or script execution

Read this entire file before acting. For installation or script execution read [execution and project state](references/execution-and-state.md) fully. Finish with the selected project, command/result and dependency or script evidence; a valid manifest does not establish a working application.

Define `project` as the intended project directory. Inspect manifest/lock consistency and locked package information while suppressing project plugins and scripts:

~~~bash
composer --working-dir="$project" --no-plugins --no-scripts validate
composer --working-dir="$project" --no-plugins --no-scripts show --locked
~~~

These are project inspections; `show --locked` describes the lockfile, not necessarily the installed `vendor/` contents. A missing or stale lockfile is a deployment decision to resolve, not a reason to run `update` reflexively.

Use the existing Composer installation rather than writing dependency-resolution glue. Composer runs on the PHP interpreter selected by its installation/launcher. A successful shell `php -v` under another environment does not prove the same interpreter, extensions or configuration were used by a scheduled/elevated invocation. See [Composer CLI commands](https://getcomposer.org/doc/03-cli.md) for the installed option set.
