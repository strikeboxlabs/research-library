---
name: pip
description: Inspect, retrieve or install Python distributions in a selected Linux interpreter environment. Use when manifest versus installed versions, wheel compatibility, source builds or the wrong pip cause reproduction failures.
---

# Match the interpreter before installing

Read this entire SKILL.md before acting. Identify the intended interpreter and select environment inspection, distribution retrieval or installation. For retrieval without installation, read [reviewed wheel retrieval](references/wheel-retrieval.md) completely before its procedure. Installation below requires an authorized change in the selected reproduction environment, with reviewed package inputs. Finish with the selected metadata/artifact/dependency result and the relevant application check separately; retrieval or installation success is not application compatibility.

Call pip through the intended Python interpreter. A bare `pip` may belong to another environment; installing successfully there does not resolve imports in the program's actual interpreter.

## Inspect the existing environment before recreating it

A downloaded `requirements.txt` describes installation inputs, not necessarily the running service's packages. Use the service's actual trusted interpreter path as `python` and the distribution's metadata name as `distribution`:

~~~bash
"$python" -m pip --version
"$python" -m pip show "$distribution"
~~~

Record Version and Location alongside that interpreter. A missing-distribution warning only establishes absence of matching metadata in this environment; check the selected virtual environment, distribution name and vendored source before declaring the application unaffected. Distribution and import names need not match. Reading package metadata avoids importing the suspect application merely to ask its version.

An **illustrative** manifest pin `library==1.2` plus installed metadata `Version: 1.3` is a mismatch to investigate, not a reason to downgrade the live service. Even matching metadata needs package-origin/patch and reachable-code checks for a vulnerability conclusion. Installing the downloaded requirements first changes the evidence and can execute build code.

## Legacy dependencies and a separate reproduction environment

For an old Python 2.7 application, use its reviewed existing environment and a compatible pip release. Pip 21.0 removed Python 2 support; the current pip is not a drop-in replacement. An unversioned `pip install django` neither selects Django 1.6.11 nor proves which interpreter receives it. Determine the deployed version and API/serializer contract before choosing a pinned reproduction input. Preserve an existing service environment rather than downgrading it to match a copied command.

The standard-library `venv` command below is for a compatible Python 3 interpreter. Python 2.7 has no `-m venv`; select an existing prepared legacy environment or separately authorized matching environment tooling rather than claiming this command will create one. New pip options such as `--dry-run` are also not universal in legacy releases: inspect the installed command's help. A resolution/dry-run of source distributions may run build/metadata code, so it is not passive inspection of an unknown package.

Define `python` as the intended interpreter's absolute path and `environment` as a new virtual-environment directory:

~~~bash
"$python" --version
"$python" -m venv "$environment"
"$environment/bin/python" -m pip --version
~~~

Stop if environment creation fails. If the matching interpreter is unavailable, choose an explicit prepared runtime/container; do not change the host's system Python to reproduce a historical walkthrough.

A wheel's tags encode compatibility: `cp38-cp38` requires the corresponding CPython/ABI, while platform tags constrain architecture and platform compatibility. A Python 3.8 x86_64 TensorFlow wheel is not generally interchangeable with another Python or architecture. Renaming the wheel does not change those constraints. Match the documented producer environment and separately investigate consumer compatibility.

For a reviewed local wheel set, define `wheelhouse` as its absolute directory, `wheel` as the selected absolute wheel path and `distribution` as its package metadata name:

~~~bash
"$environment/bin/python" -m pip install --no-index --find-links "$wheelhouse" --only-binary=:all: "$wheel"
"$environment/bin/python" -m pip show "$distribution"
"$environment/bin/python" -m pip check
~~~

This confines normal dependency lookup to the provided wheel location and rejects source-distribution fallback. The full compatible dependency set still has to be present; inspect direct-URL requirements separately. `--no-deps` merely skips dependency installation and does not establish that dependencies are satisfied. Package installation changes the chosen environment.

For online resolution, select the approved index and versions explicitly. Do not use certificate-validation bypasses as a routine fix. Building an sdist can execute its build backend; a successful wheel install still does not make its code safe to import. `pip show` reports metadata/location, and `pip check` checks declared dependency consistency, not native-library loading or application behavior. Run the smallest relevant fixture separately; loading a supplied model or constructing a callback-bearing model can execute code locally.

See [pip interpreter selection](https://pip.pypa.io/en/stable/user_guide/#running-pip) and [Python 2 support removal](https://pip.pypa.io/en/stable/news/#v21-0) for legacy environment differences. Use the [requirements format](https://pip.pypa.io/en/stable/reference/requirements-file-format/), [pip show](https://pip.pypa.io/en/stable/cli/pip_show/) and [distribution/import distinction](https://packaging.python.org/en/latest/discussions/distribution-package-vs-import-package/) when reconciling source and environment evidence.
