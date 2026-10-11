---
name: neo4j
description: Start and diagnose an owned Neo4j DBMS process from Linux. Use when backgrounding a launcher, the wrong installation or a service-manager mismatch hides startup failure.
---

# Establish the DBMS process before using a client

Read this entire SKILL.md before acting. Require the selected installed Neo4j/Java runtime, reviewed configuration/data directories and authority to start that instance as its service user. Determine its existing process manager first. Finish with startup/status and an actual client response separately; missing runtime, config or credentials remain prerequisite gaps.

Use the selected installation's executable, not whichever same-named binary happens to lead PATH. Inspect its version and help:

~~~bash
neo4j --version
neo4j --help
neo4j status
~~~

A status from another installation or user can describe a different instance. Establish the selected home/configuration, data store, account and configured listeners before starting; defaults are not proof of which endpoint a client uses. Starting writes runtime/log/data state and exposes the configured listeners.

For an owned standalone instance managed through this launcher:

~~~bash
neo4j start
start_status=$?
neo4j status
~~~

`start` launches a daemon; `console` runs the server in the foreground when startup diagnostics are needed. Adding shell `&` to `start` backgrounds the launcher and makes its output/status easier to miss; it is not needed to daemonize the server. Preserve the launch status and diagnostic log, then use the intended existing client to verify its requested operation. Process status does not establish authentication, database availability, successful data import or compatibility with that client.

If startup fails, resolve the reported Java/configuration, listener, store-lock or filesystem issue for the selected instance. Do not delete lock/data files or start a second instance over the same store as a retry. First-time credentials and client compatibility must already be prepared; a password-history entry is not a successful login.

For a package deployment already managed by systemd, use its configured service lifecycle rather than a second direct launcher. Choose one manager and inspect that service's status/logs. Stop only an instance started for this task, using its same manager (`neo4j stop` for this standalone daemon), and verify its state afterward.

Current [Neo4j CLI documentation](https://neo4j.com/docs/operations-manual/current/neo4j-admin-neo4j-tools/) describes `neo4j` as the corresponding server-command interface; select documentation for the installed version. See the [systemd deployment guidance](https://neo4j.com/docs/operations-manual/current/installation/linux/systemd/) when that manager owns the process.
