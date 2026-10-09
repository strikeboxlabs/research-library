---
name: aureport
description: Inspect existing Linux audit logs for TTY input with aureport and correlate entries using ausearch. Use for interpreting recorded keystrokes and avoiding incorrect user attribution in copied logs.
---

# Aureport TTY evidence

TTY input exists only if auditing captured it. Reading logs does not enable auditing or reconstruct earlier input. Define `audit_log` as an existing raw audit file or a directory of relevant logs, and `report` as a fresh file:

~~~bash
aureport --version
aureport --input "$audit_log" --tty > "$report"
~~~

On the original host, omitting `--input` reads the configured logs. Permission errors and unreadable rotations are coverage gaps, not evidence that no input was recorded.

Use the report's timestamp, event number, audit user, session and command together. To inspect one event, set `event_id` to its reported audit serial:

~~~bash
ausearch --input "$audit_log" -a "$event_id"
~~~

Event numbers can recur across boots or hosts; narrow by the observed time/node when necessary. Preserve the raw identifiers. `aureport -i` can resolve numeric users using the analysis machine's current accounts, producing misleading names for copied logs.

TTY records contain keystrokes, including control keys and corrections. They do not prove that the final command executed or authentication succeeded; correlate neighbouring authentication/process events. An audit login UID can remain associated with the original session after an identity change.

Password capture is configuration- and terminal-dependent: `pam_tty_audit` normally excludes input entered with echo disabled, while `log_passwd` and some session behaviours can expose it. Do not assume every password was logged. Preserve any sensitive evidence locally and report only what the investigation requires.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Academy PDF pp. 13–14. Maintenance sources: [aureport](https://github.com/linux-audit/audit-userspace/blob/master/docs/aureport.8), [ausearch](https://github.com/linux-audit/audit-userspace/blob/master/docs/ausearch.8), [pam_tty_audit](https://github.com/linux-pam/linux-pam/blob/master/modules/pam_tty_audit/pam_tty_audit.8.xml).
