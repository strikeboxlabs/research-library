---
name: pyload
description: Query an installed pyLoad launcher's reported version without starting the download service. Use when a short version string is being confused with a running service's exact build or advisory applicability.
---

# Identify the selected installed pyLoad launcher

Read this entire SKILL.md before acting. Require the trusted installed launcher and its interpreter/environment; retain actual version output, status and identity limits. No conditional resources are required. This task neither starts pyLoad nor tests an exploit.

Define `pyload_bin` as the verified absolute path of the selected launcher:

~~~bash
"$pyload_bin" --version
status=$?
~~~

Check status and diagnostics. The documented option prints the program version and exits. Invoking the launcher still loads its Python entrypoint; use the trusted installed program rather than running an acquired script. A missing dependency or wrong environment leaves the version query incomplete.

Retain the complete returned version, package/build identity when independently available, and the queried path. A short `0.5.0` label does not resolve development release, patch provenance or the code loaded by a separately running process. Correlate that process's executable/interpreter, start context and package metadata before applying a version-specific advisory. A root-owned process row describes that observed process, not the caller or every HTTP endpoint.

Do not invoke the launcher without options as a diagnostic fallback: ordinary startup can create storage/configuration directories and start the service. Reset, dry-run and daemon modes have separate effects and are outside this narrow version task. Finish with the verified launcher result and unresolved runtime-build association.

Reference: [pyLoad documented CLI options](https://github.com/pyload/pyload#usage).
