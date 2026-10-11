---
name: net
description: Query a selected SMB server's time with Samba net and perform an explicitly authorized one-shot local clock correction. Use when server time, timezone display and Kerberos clock disagreement need to be separated.
---

# Compare time with the selected server

Read this entire SKILL.md before acting. Require the installed Samba net implementation, independently established server and reachable SMB service. The query is below; the clock-setting branch additionally requires local authority and an approved time source. Finish with query/status evidence or measured local time after the change, including failures and active time-service effects. No conditional resources are required.

Define `net_bin` as the actual installed Samba executable and `server` as the selected server hostname. Windows net.exe is a different implementation. Inspect the installed command before applying Samba options:

~~~bash
"$net_bin" --version
"$net_bin" time -S "$server"
"$net_bin" time zone -S "$server"
~~~

The first time command displays the remote server time; `time zone` separately reports its timezone offset from GMT. This is an SMB operation, not an NTP query or proof of the server's own synchronization. Check status and authentication/transport diagnostics. A displayed timestamp with another timezone is not automatically clock skew; compare equivalent instants and retain the local observation time. `time system` formats remote time for date, but does not set the local clock.

## Set the local clock only for the approved correction

Use this branch only when the selected server is the approved time source and the task authorizes changing the local system clock. Coordinate with the host's existing time service; a manual step is neither persistent synchronization nor a replacement for that service. Run under the already authorized local identity capable of changing system time:

~~~bash
"$net_bin" time set -S "$server"
~~~

Samba attempts to set the **local** date/time using its date utility; it does not change the remote server. A container or restricted process may lack the required capability even when its user name is root. Check the command's final status, compare the resulting local/server instants and record whether the active time service subsequently changes the clock. A failed set leaves clock agreement unresolved. Do not infer a successful change solely from silence or a later successful login.

Reference: [Samba net TIME commands and server selection](https://www.samba.org/samba/docs/current/man-html/net.8.html).
