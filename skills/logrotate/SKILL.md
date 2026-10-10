---
name: logrotate
description: Diagnose logrotate decisions without rotating logs. Use for custom scheduled configurations, unexpected skips, state-file mismatches and permission or hook-identity questions.
---

# Diagnose a rotation job

Check `logrotate --version` and local help. Establish the actual executable, invocation UID, configuration arguments in order, state-file option and scheduler command. A process using a private configuration does not establish that `/etc/logrotate.conf` or its includes apply. If those inputs are unreadable, record the missing evidence; another configuration cannot explain that job.

Define `config` as the observed readable configuration and `report` as a fresh local report path:

~~~bash
logrotate --version
umask 077
logrotate --debug "$config" >"$report" 2>&1
rotation_status=$?
~~~

Inspect both the status and report. `--debug` previews decisions without changing logs or the state file; hook text may be printed but is not executed. `--verbose` alone still performs rotation. Preserve the job's known `--state` argument and configuration order when adapting this command. Keep `--debug` present if reproducing an observed `--force` decision; force without debug is a real operation.

| Observation | Interpretation and next check |
|---|---|
| No rotation needed | Compare reported last-rotation time, current size and effective criteria. A `daily` rule needs a scheduler to invoke the program; it does not schedule itself. |
| Different result from the job | Compare state path, force flag, includes, UID and environment. An empty state file or `/dev/null` changes the evidence for time-based decisions. |
| Permission error or skipped path | Distinguish inaccessible inputs, insecure parent-directory rejection, symlinks and multiple hard links. Inspect the stated condition before proposing a configuration change. |
| Rotation predicted | A preview does not establish that the scheduled job ran, the application reopened its log or the hooks succeeded. Check the actual job evidence separately. |

## Interpret ownership and replacement

A writable log alone does not establish control over its pathname or privileged code execution. Inspect directory ownership, traversal/replacement permissions, the effective configuration and the installed package's protections. A preview under your UID cannot prove what a privileged invocation can access; scheduler confinement may also differ.

`su user group` selects rotation identity; hook scripts run with the invoking identity. Review these separately. `copytruncate` keeps the original file but has a copy/truncate loss window; `create` does not create a replacement in that mode. With rename/create, confirm how the writer reopens its log and what the configured hooks do before changing rotation behavior.

Use the installed manual first; the upstream [manual](https://github.com/logrotate/logrotate/blob/main/logrotate.8.in) and [implementation](https://github.com/logrotate/logrotate/blob/main/logrotate.c) explain option interactions and skip conditions. Distribution versions and backports can differ.
