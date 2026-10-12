---
name: logger
description: Send one benign message to an owned local syslog path and verify its destination. Use when client success, facility selection or missing downstream records obscures log delivery.
---

# Verify one local log message

Read this entire SKILL.md before acting. Require an owned logging path, a reviewed facility/level and permission to add a clearly identified diagnostic message. All instructions are inline. Finish with the submitted marker, time, client status and matching destination record; missing downstream evidence leaves delivery unconfirmed.

Identify util-linux logger with `logger --version` and its installed help. Review the local receiver's routing first, including forwarding and automated actions. Choose a harmless message without secrets or control characters. Define `priority` as the intended facility.level, `tag` as a short diagnostic label and `marker` as a unique short text identifying this check. For example, user.notice is suitable only when that route is the intended one.

~~~bash
logger --socket-errors=on --priority "$priority" --tag "$tag" -- "$marker"
status=$?
~~~

This submits to the local system-log socket. `--` terminates option parsing. Supplying the message explicitly avoids waiting for standard input. Retain stderr and status immediately; socket errors are surfaced explicitly here, while defaults can hide a missing local socket in some environments. A stderr copy with `-s` is not a receipt from the receiver.

Use the configured destination's existing reader to locate that exact marker in a bounded time window. Record its facility/level, tag, time and any transformation. A client return of zero does not prove forwarding, database insertion or durable retention. If absent, inspect receiver availability, filters, queue state and read permissions before sending another message. A container's local socket may belong to a different logging path than the host's.

For rsyslog selector lines, a facility with `.info` matches info and more severe messages; `.debug` is lower severity. An exact-level selector uses `.=info`. Read the complete rule ordering and selected ruleset before attributing a destination; a familiar facility name does not mean every receiver stores it. Keep routing success separate from whether a later consumer safely interprets the message.

See the [util-linux logger manual](https://manpages.debian.org/bookworm/bsdutils/logger.1.en.html) and [rsyslog selector rules](https://docs.rsyslog.com/doc/configuration/filters.html).
