---
name: service
description: Query or restart one selected Linux service through the service wrapper, preserving backend, script-specific status and application-health evidence.
---

# Operate one selected service

Read this entire SKILL.md before acting. Require the intended host, trusted service wrapper and exact service name/backend. Status invokes service code; restart additionally requires the selected service's supported action, valid reviewed configuration, appropriate privileges and authorization for the interruption. Finish with before/after state, action result and the requested application-health check or its unresolved gap. No conditional resources are required.

Define `service_bin` as the selected wrapper and `service_name` as the exact init-script/unit name. Inspect the wrapper's version/help and that service's supported actions before using it:

~~~bash
"$service_bin" --version
"$service_bin" --help
"$service_bin" "$service_name" status
~~~

The wrapper can select a SysV init script or a systemd unit; a same-named unit takes precedence in the documented Debian implementation. It resets the working directory to `/` and removes most environment variables. Do not expect the caller's current directory or shell variables to configure the daemon. Status text and exit codes come from the selected backend/script; a nonzero result needs interpretation, and a script without status support leaves state unresolved. `--status-all` covers SysV scripts, not a complete systemd inventory.

After the service-specific configuration validator passes and the restart is authorized, use its supported restart action in the approved privileged context:

~~~bash
"$service_bin" "$service_name" restart
"$service_bin" "$service_name" status
~~~

Restart can disconnect clients or leave the daemon stopped after a configuration failure. Retain both action diagnostics and resulting state, then perform the selected application's normal health check. Wrapper success or a running PID does not prove that a requested listener, share or application function is healthy. Do not treat an unsupported reload as permission to substitute a disruptive restart. This wrapper does not establish startup enablement or validate application configuration.

See the [documented wrapper/backend behavior](https://manpages.debian.org/bookworm/init-system-helpers/service.8.en.html); verify the installed implementation and service actions when they differ.
