---
name: crontab
description: Read the current user's installed cron table and distinguish a listed schedule, no table, access errors and system-wide scheduling coverage gaps.
---

# Read the current user's cron table

Read this entire SKILL.md before acting; reuse complete current context. Require the installed crontab implementation and the intended current account. Use the read-only listing below, preserving status and diagnostics. Finish with that account's reported entries and scope gaps; a listed entry is configuration evidence, not observed execution.

Define `report` and `errors` as fresh private file paths:

~~~bash
umask 077
(set -o noclobber; crontab -l >"$report" 2>"$errors")
status=$?
~~~

Distinguish a readable table from a 'no crontab' diagnostic or permission/service errors; a nonzero status alone does not distinguish these. With no user selector, this lists the invoking user's table. A service-account session does not expose every user's schedules. Installed access policy can restrict use.

Preserve each entry's actual fields, environment assignments and command. Comments, filenames and a walkthrough's interval description do not establish cadence. Cron implementations, extensions and timezone handling differ; use the installed crontab format manual when the selected entry depends on them. A configured path is a lead to inspect the actual file and service context, not proof the scheduler ran it successfully.

An empty or missing user table does not exclude /etc/crontab, cron.d, periodic directories, systemd timers or another scheduler. Those are separate selected sources; user and system crontab formats differ, including the system table's user field. Do not install the captured output, invoke crontab with a filename, or select editing/removal options to inspect it.

See the [Cronie crontab manual](https://manpages.debian.org/testing/cronie/crontab.1.en.html) for implementation and access-policy differences.
