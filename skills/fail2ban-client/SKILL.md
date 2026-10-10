---
name: fail2ban-client
description: Diagnose Fail2ban jails and perform selected ban, unban or reload operations. Use when login failures do not trigger a ban, a client remains blocked or configured actions differ from the running jail.
---

# Follow a failure through the jail

Read this entire file before acting. Read [filters and changes](references/filters-and-changes.md) for log matching, action inspection, unbanning or reloads. Finish with the selected jail's observed input, counters, ban state and action result; server liveness alone is insufficient.

Check `fail2ban-client --help` for the installed version. It controls a running local Fail2ban server through its socket; `-c` selects configuration and `-s` selects the socket when the deployment uses nondefault locations. Permission denied on that socket is different from an absent server.

~~~bash
fail2ban-client ping
fail2ban-client status
~~~

Select `jail` from the returned jail list, then inspect the running settings:

~~~bash
fail2ban-client status "$jail"
fail2ban-client get "$jail" findtime
fail2ban-client get "$jail" maxretry
fail2ban-client get "$jail" bantime
fail2ban-client get "$jail" ignoreip
fail2ban-client get "$jail" actions
~~~

Failures must match the jail's input/filter and occur within its window; a lifetime failed count alone does not predict the next ban. Check ignore rules, parsed source IP and actual timestamps. A proxy/NAT can make the observed source differ from the client you intended to diagnose. An increasing ban counter is also not proof that the firewall/mail/custom action succeeded.

Use `get "$jail" logpath` for file-backed jails and `get "$jail" journalmatch` for journal-backed ones. Check the configured backend rather than demanding a log file for every jail. Correlate Fail2ban's own error log with the service's input. Configuration files on disk may not match runtime state until the relevant reload.

The [client manual](https://github.com/fail2ban/fail2ban/blob/master/man/fail2ban-client.1) lists version-specific queries and changes.
