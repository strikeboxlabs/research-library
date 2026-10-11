---
name: uptime
description: Read procps uptime and distinguish Linux load averages from CPU utilization or application health. Use when a status script extracts three load numbers without retaining their time windows and context.
---

# Read uptime and load in context

Read this entire SKILL.md before acting. Confirm procps with `uptime --version` and establish the host/container context. No conditional resources are required. Finish with the full successful observation, its time and interpretation limits; missing output is not a zero load.

~~~bash
LC_ALL=C uptime
status=$?
~~~

Retain stderr and check `status`. The ordinary line reports current time, uptime, logged-on users and load averages over **1, 5 and 15 minutes**, in that order. Keep the full line instead of assuming the localized phrase preceding the numbers is a stable parser contract.

Linux load counts runnable and uninterruptible tasks, including tasks waiting on I/O. It is neither CPU percent nor a direct latency measurement, and the values are not normalized by CPU count. A higher recent value suggests a trend to correlate with process, CPU and I/O observations; it does not identify a cause. A low value does not establish that a database or web service works. Establish what the visible kernel/procfs data represents before treating a container observation as the application's isolated load. Uptime alone does not establish patch level or explain a restart.

See the packaged [procps uptime manual](https://manpages.debian.org/bookworm/procps/uptime.1.en.html).
