# Dependency and script execution

Set `project` to the intended absolute project directory. Inspect `composer.json`, `composer.lock`, script definitions, plugin declarations and the intended execution identity before selecting a write. A project-controlled Composer script runs with the Composer process's privileges. A sudo rule allowing Composer in a writable project can therefore permit execution of project-controlled commands; the command name alone is not a confinement boundary.

## Install a known locked dependency set

For a deployment that intentionally excludes developer packages and project hooks:

~~~bash
composer --working-dir="$project" --no-plugins --no-scripts --no-interaction install --no-dev
composer --working-dir="$project" --no-plugins --no-scripts check-platform-reqs --no-dev
~~~

`install` uses locked versions when a lockfile exists and writes dependencies/autoload files. It may need network access even when versions are locked. `update` resolves dependencies and rewrites the lockfile; that is a different task. `--no-dev` is appropriate for a selected deployment, not a default for developing or testing every project.

Suppressing scripts/plugins may omit application initialization the project requires. Treat that as a known incomplete stage and select the reviewed next step. Do not claim the application is ready merely because dependency installation succeeded. `check-platform-reqs` checks actual PHP/extension requirements; a configured emulated platform used during dependency resolution does not install those extensions.

## Run one reviewed project script

List script names without running them, inspect their definitions and referenced files, then set `script_name` to the requested one:

~~~bash
composer --working-dir="$project" --no-plugins run-script --list
composer --working-dir="$project" --no-plugins run-script "$script_name"
~~~

This second command executes the script. Do not add `--no-scripts` and then assume a desired script ran. Scripts can call other scripts or external programs; the effect is defined by the project, not the friendly script name. Additional arguments after `--` are passed to the script and can change its behavior.

If plugin functionality is required, review that plugin and the project's allow-plugins configuration before enabling it; a blanket enable-all switch is not evidence of compatibility. Preserve the actual failing stage and its output. A timeout or failed hook can leave an installed dependency tree alongside incomplete application state, so inspect the result before repeating stateful hooks.

See [script semantics](https://getcomposer.org/doc/articles/scripts.md) and [CLI command distinctions](https://getcomposer.org/doc/03-cli.md).
