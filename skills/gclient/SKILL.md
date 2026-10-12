---
name: gclient
description: Synchronize the dependency layout of a selected trusted Chromium or V8 checkout with depot_tools gclient. Use after an intended source revision changes and a plain Git checkout leaves dependencies inconsistent.
---

# Synchronize a modular checkout

Read this entire SKILL.md before acting. Require the reviewed .gclient, selected solution revision and its DEPS configuration, a compatible depot_tools environment and authorization for dependency acquisition/setup. No conditional resources are required. Finish with actual solution/dependency revisions, sync status and remaining errors; synchronization does not compile or test the source.

Define `gclient_bin` as the verified depot_tools invocation, `workspace` as the absolute root containing .gclient and `sync_log` as a fresh private output:

~~~bash
"$gclient_bin" help
"$gclient_bin" help sync
(
  cd -- "$workspace" || exit
  "$gclient_bin" sync
) >"$sync_log" 2>&1
status=$?
~~~

Establish the intended source revision and preserve local edits before syncing. .gclient and DEPS are executable/configuration inputs, not harmless URL lists. They define solutions, pinned dependencies and possible overrides; depot_tools wrappers can also update/bootstrap tools. Review the selected setup before invoking even its helper workflow.

Check final status and every consequential checkout or setup error. A solution at the requested commit does not prove its dependencies match. Custom dependency overrides and unpinned URLs can change the resulting tree; retain them with the actual revisions. Network, unsupported runtime and local-change conflicts need distinct resolution rather than destructive reset options.

A failed sync may leave several repositories changed. Inspect that partial state before retrying; do not call the entire workspace synchronized because one dependency succeeded. Running installation scripts or the resulting build requires its own selected task.

See [gclient configuration](https://chromium.googlesource.com/chromium/tools/depot_tools/+/main/README.gclient.md), [wrapper/bootstrap behavior](https://chromium.googlesource.com/chromium/tools/depot_tools/+/main/README.md) and [V8 synchronization](https://v8.dev/docs/source-code).
