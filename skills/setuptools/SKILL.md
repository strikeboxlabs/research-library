---
name: setuptools
description: Build a reviewed Python project using its Setuptools backend and publish selected release artifacts to an approved private repository. Use when legacy setup.py commands, package metadata or repository labels cause build and upload confusion.
---

# Build the selected project

Read this entire SKILL.md before acting. Require the reviewed project, intended trusted Python and approved build inputs. For an authorized private release, read [private publishing](references/private-publishing.md) fully after the build. Finish with selected artifact paths, metadata and build/check results; an upload receipt and consumer installation are separate evidence.

Inspect the project's pyproject.toml, setup.cfg and setup.py as text first. Confirm the backend, distribution name, explicit version, package discovery and included files. A setup.py is executable Python: top-level operations can occur before setup() or any build failure. A marker appearing during a build does not establish that a separate consumer installed the package. An exception-only setup() call can skip the actual build entirely when the preceding operation succeeds.

Use the existing prepared interpreter and build frontend; tool provisioning is a separate action. Define `python` as its absolute path, `project` as the reviewed absolute project directory and `dist_dir` as a new absolute output directory:

~~~bash
"$python" --version
"$python" -m build --version
mkdir -- "$dist_dir" || exit
"$python" -m build --outdir "$dist_dir" "$project"
~~~

Stop on failure and retain the diagnostics and any partial outputs separately. The default build produces an sdist, then builds a wheel from that sdist; this helps expose missing source files. Build isolation supplies build dependencies, potentially downloading them: approve their sources and constraints before running. Isolation is dependency separation, not a security sandbox. A selected prepared offline build needs its complete build dependency set; do not remove isolation merely to hide a missing requirement.

Review the resulting exact artifacts, their distribution metadata and archive member lists. Require the intended name/version, package files and supported wheel tags; no unexpected private files. Native extensions need the intended compiler, headers and platform. A build completion line does not establish importability on another interpreter/image. Use a separate prepared environment for an authorized installation and relevant application check.

Direct `python setup.py sdist`, `bdist_wheel` and `upload` are historical command interfaces. Keep an acquired transcript's actual interpreter, configuration and command separate from a modern reproduction. Setuptools still supports setup.py as build configuration, but recommends the build frontend and a separate uploader rather than direct command execution. Do not run an unknown setup.py merely to ask its version.

See [Setuptools command migration](https://setuptools.pypa.io/en/latest/deprecated/commands.html), [build frontend](https://build.pypa.io/en/latest/) and [build CLI](https://build.pypa.io/en/latest/reference/cli.html) for backend/version and output differences.
