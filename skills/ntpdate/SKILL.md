---
name: ntpdate
description: Query a Linux clock's offset from a selected NTP server and perform an intended one-time correction with ntpdate. Use when real clock skew must be separated from displayed time zones or authentication failures.
---

# Separate a clock query from clock changes

Read this entire SKILL.md before acting. Identify the installed ntpdate implementation, the intended trusted time server and whether the task requests a query or host-clock correction. Finish with offset/status evidence and the result of any intended correction; authentication success is a separate check.

Define `server` as that NTP hostname/IP. Query without setting the clock:

~~~bash
ntpdate -q -v "$server"
~~~

`-q` queries only; `-v` adds version identification. In legacy ntpdate, `-s` sends logging to syslog; it does not select query mode or prove a silent correction succeeded. Preserve server selection, offset units, status and diagnostics. A displayed time-zone difference is not necessarily epoch skew. A network timeout or unsuitable server is not a measured zero offset.

For a requested one-time correction, establish the host's existing time-service arrangement and required clock-changing privilege first:

~~~bash
sudo ntpdate "$server"
ntpdate -q "$server"
~~~

The first operation changes the host clock and can step a large offset; it is not a per-command virtual clock. An active time service can conflict with it or subsequently correct it. Do not disable that service simply to hide a failure. `-u` selects an unprivileged outgoing network port; it does not remove the privilege required to set time. `-b` forces a step and is unnecessary for a routine query.

Legacy NTP and NTPsec packages can provide different implementations. A one-time result does not establish ongoing synchronization. Treat Kerberos clock tolerance as the deployed policy rather than a universal five-minute guarantee.

Use the [upstream ntpdate manual](https://www.ntp.org/documentation/4.2.8-series/ntpdate/) and [NTPsec package manual](https://manpages.debian.org/bookworm/ntpsec-ntpdate/ntpdate.8.en.html) to resolve installed behavior; this skill does not install or configure a time service.
