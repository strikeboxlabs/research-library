---
name: virtualenv
description: Create a selected Python interpreter environment with the installed virtualenv tool and use its executables explicitly. Use when a CLI dependency belongs in a separate environment or activation obscures which Python/pip runs.
---

# Select the interpreter and environment

Read this entire SKILL.md before acting. Require the installed virtualenv tool, the selected available interpreter and a fresh authorized environment directory. Create only that environment, verify its executable/metadata context and keep dependency installation a separately authorized change. Finish with the selected interpreter/environment and requested tool result; an activation prompt is not evidence of dependency availability or isolation.

Define `python_bin` as the verified existing interpreter and `environment` as a new absolute directory. Inspect installed version/help before using version-dependent options:

~~~bash
virtualenv --version
virtualenv --help
virtualenv --python "$python_bin" "$environment"
"$environment/bin/python" -c 'import sys; print(sys.executable); print(sys.version); print(sys.prefix); print(sys.base_prefix)'
"$environment/bin/python" -m pip --version
~~~

`--python` selects the environment's base interpreter; omitting it normally uses the Python associated with virtualenv. A generic python name can resolve differently under a version manager. Check creation status and actual executable before continuing. The chosen interpreter must already exist; creating an environment is not installing a new Python version.

Creation writes the environment and can seed packaging tools/use cache or download behavior according to that virtualenv version/options. Review those when the task must be offline or avoid automatic updates. A reused directory can retain stale packages; do not clear an existing environment as an incidental retry. A virtual environment separates Python package lookup, not OS privileges/network/filesystem access or arbitrary-code execution.

For an existing CLI installed there, invoke its verified path such as `"$environment/bin/git-dumper" --help`; package presence alone does not guarantee that entrypoint exists or the operation succeeds. For package metadata, use `"$environment/bin/python" -m pip show "$distribution"` with the actual distribution name. Installation, if separately requested, should use this same interpreter and reviewed inputs instead of an unrelated bare pip.

Optional activation in the current Bash shell is `source "$environment/bin/activate"`; `deactivate` restores its shell changes. It changes PATH and related shell context, not the process identity, and sourcing executes that local script. Explicit environment executables work without activation and avoid assuming it persists across task-graph shell calls. An environment tied to a moved/removed base interpreter may need recreation; copying its directory is not a portable tool distribution.

See [virtualenv interpreter and activation guidance](https://virtualenv.pypa.io/en/latest/how-to/usage.html) and [installed-option reference](https://virtualenv.pypa.io/en/stable/reference/cli.html) for the applicable creation/seeding behavior.
