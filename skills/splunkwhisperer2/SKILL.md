---
name: splunkwhisperer2
description: Test authenticated Splunk app installation and scripted-input execution with PySplunkWhisperer2 remote mode. Use for an authorized reachable management API where app permissions, service identity, bundle callback routing or misleading success messages affect the result.
---

# SplunkWhisperer2 remote app execution

Read this entire SKILL.md before acting; reuse complete current context. For remote testing, read [app installation, execution and cleanup](references/remote-app.md) fully before its procedure. Establish the scoped management endpoint, selected credential, tool revision and permitted app/process changes. Finish with separate authentication, install, execution/identity and cleanup evidence; a tool success message alone is insufficient.

Use the existing reviewed `PySplunkWhisperer2_remote.py` and compatible Python environment with `requests`. Define `python_bin` and `tool` as their actual invocations/paths; do not guess image locations or replace a missing tool silently. Inspect the selected trusted source/revision before loading its help:

~~~bash
"$python_bin" "$tool" --help
~~~

The supported branch installs an app through Splunk's management REST API, serves its bundle from the worker and creates a scripted input executed by the Splunk service. It is a mutating execution test, not a passive scanner. Service UID zero can make it privileged; another service identity produces that account's authority instead. Port 8089 or a Splunk banner alone does not establish a universal forwarder, permitted app installation or root execution.

The upstream Python remote mode also supports Linux targets when filename/content suit the target. Its Windows local and Sharp variants are separate procedures; this package does not claim their execution coverage. Current UF management exposure differs by version/configuration, so a historical externally reachable endpoint is a condition to test, not today's universal default.

Reference: [upstream tool and mode selection](https://github.com/cnotin/SplunkWhisperer2).
