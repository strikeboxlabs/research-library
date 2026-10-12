---
name: w
description: Read Linux login-session and process snapshots with procps-ng w. Use when a tty, display hint, idle value or command line needs interpretation without assuming authenticated access.
---

# Read session records in their process context

Read this entire SKILL.md before acting. Require procps-ng w and the intended Linux namespace with readable login records and process metadata. No conditional resources are required. Finish with the timestamped snapshot, selected fields and missing-record or process-visibility limits.

~~~bash
w --version
w
~~~

For one selected account, define `account` as its exact login name and use `w "$account"`. This filters session records; it does not authenticate that account or change the caller's identity. Preserve the header and column labels because distribution defaults can change whether FROM is printed. `-f` toggles that field rather than unconditionally enabling it.

The header contains observation time, uptime, logged-in record count and 1/5/15-minute load averages. Rows associate login name, tty, origin, login time, idle time, JCPU, PCPU and WHAT. JCPU covers processes attached to that tty, including current background jobs; PCPU covers the process shown in WHAT. These are CPU times, not wall-clock session duration. `-s` omits login and CPU fields.

A FROM value such as the **illustrative** `:0` can suggest an X display associated with a session. It establishes neither permission to connect to that display nor its current window contents. WHAT is a selected current process command line, not proof that every process on the tty has the listed user's effective UID. For identity or process ownership, inspect the particular process separately. `-u` changes how the current process/CPU times are selected across account changes such as su.

W combines login records with /proc information. Containers, stale/missing records, restricted /proc access and concurrent logins/process exits can make this incomplete. An empty table does not prove there are no interactive processes; a count is not a count of unique people. Retain diagnostics and the actual namespace rather than treating display or username text as access evidence.

See the packaged upstream [procps-ng w manual](https://manpages.debian.org/bookworm/procps/w.1.en.html).
