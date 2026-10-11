---
name: sshuttle
description: Route a selected administration service through an existing SSH account with sshuttle. Use when a service is reachable from the SSH host but client routing, Python requirements or firewall setup prevent access.
---

# Reach a selected service through SSH

Read this entire SKILL.md before acting. Require permission for the selected service, remote Python execution and temporary local firewall changes, plus an existing SSH identity. No conditional resources are required. Finish with the actual forwarded range, service response and shutdown/cleanup evidence; SSH connection alone is incomplete.

Inspect `sshuttle --version` and `sshuttle --help`. Check that release's Python requirements on both ends and supported local firewall method. Remote sshuttle installation is unnecessary: its Python code is sent and executed through SSH. Local firewall management needs root/sudo; this does not grant remote root.

Define `ssh_host` as an existing reviewed SSH-config alias and `service_route` as the requested numeric single-host destination, preferably its `/32:port` when installed help supports port restriction. With no extra inherited SSHUTTLE_ARGS, run in the foreground:

~~~bash
sshuttle -v -r "$ssh_host" "$service_route"
~~~

Keep authentication in the SSH configuration; do not reconstruct a shell command from untrusted key paths. Inspect the chosen method, forwarded/excluded ranges and connection/firewall setup. Establish overlapping local routes before changing routing. A normal SSH endpoint is excluded automatically; ProxyCommand configurations require verifying the necessary explicit exclusion.

Use the intended service client for one known read-only operation. Diagnose SSH/Python failure, firewall setup, remote reachability and application authentication separately. Defaults do not proxy DNS, and ordinary NAT mode does not establish arbitrary UDP forwarding. Avoid automatic network/hostname discovery or a default route for this selected-service task.

Stop with Ctrl+C and retain shutdown/firewall diagnostics. Check that this session's temporary rules were removed; a killed process or disconnection alone does not establish cleanup. Investigate only its identified rules rather than flushing unrelated firewall state. A failed service check remains unresolved even if setup printed a connection message.

Consult upstream [usage](https://sshuttle.readthedocs.io/en/stable/usage.html), [options](https://sshuttle.readthedocs.io/en/stable/manpage.html) and [requirements](https://sshuttle.readthedocs.io/en/stable/requirements.html) for the installed release.
