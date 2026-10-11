---
name: timedatectl
description: Inspect Linux clock, timezone and time-service state with timedatectl. Use when a synchronization indicator or displayed timezone is mistaken for a measured remote clock offset.
---

# Inspect the host's time arrangement

Read this entire SKILL.md before acting. Require the intended systemd host and reachable timedated service. No conditional resources are required. Finish with observed clock/timezone/service fields, status and unresolved offset evidence.

Confirm `timedatectl --version` and help, then query without changing the clock:

~~~bash
timedatectl --no-pager status
status=$?
~~~

Check status and errors; a container without the service is unavailable, not unsynchronized. Separate local/UTC display, RTC mode, active NTP service and synchronization status. An enabled service is not proof of agreement with a selected server; measure that offset through the established time client when needed.

`set-ntp` changes service enablement rather than merely querying it. Do not disable synchronization to diagnose an authentication failure. An intended clock/service change requires its original state and subsequent verification; one correction does not establish ongoing synchronization. `timesync-status` concerns systemd-timesyncd and does not describe every alternative daemon.

Reference: [timedatectl status and service scope](https://manpages.debian.org/bookworm/systemd/timedatectl.1.en.html).
