---
name: pkcheck
description: Check polkit authorization for a selected owned process and known action on Linux. Use when denial, unavailable authentication and incomplete action context need distinguishing.
---

# Check one authorization decision

Read this entire SKILL.md before acting. Require the known `action` and an independently verified `subject` formatted as `pid,pid-start-time,uid` for the owned process. All instructions are inline. Finish with status, diagnostics and context; this check does not execute the action.

~~~bash
pkcheck --action-id "$action" --process "$subject"
status=$?
~~~

Avoid PID-only subjects because identity lookup can race. Obtain start time and UID from trusted operating-system evidence; do not guess them. Without interactive authentication, status 0 indicates authorization, 1 denial, and 2 unavailable/required authentication. Status 3 is dismissal, 126 malformed options, and 127 a checking error.

Preserve stdout details as data, not shell code. A decision lacking the application's required action details does not establish that application's effective permission. Use the actual documented request context; do not invent detail values to obtain authorization. Missing subject/context evidence leaves the result incomplete.

Reference: [pkcheck contract](https://manpages.debian.org/trixie/polkitd/pkcheck.1.en.html).
