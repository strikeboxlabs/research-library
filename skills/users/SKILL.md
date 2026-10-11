---
name: users
description: Read GNU users login-session records for the selected host or acquired utmp-format file. Use to distinguish recorded logins from account existence, home directories and current process identity.
---

# Read the selected login records

Read this entire SKILL.md before acting. Confirm GNU coreutils and choose the current host's records or an acquired compatible file. No conditional resources are required. Finish with the selected record source, time, output/status and coverage limits; an empty result is not a complete account inventory.

For the current selected host:

~~~bash
users --version
users
status=$?
~~~

The tool reports names from its configured login-record file, normally `/var/run/utmp` on the documented Linux build. It does not query every account or enumerate all processes. Containers, record maintenance and sessions that do not update utmp can limit the result. Confirm diagnostics and record availability before reporting no recorded logins.

For a preserved compatible acquired record file, define `records` as its absolute working-copy path:

~~~bash
users -- "$records"
status=$?
~~~

The input is a platform-dependent binary login-record format, not a text list or passwd file. Identify its originating host/format and capture time. A copied historical file cannot establish who is logged in now, and a generic log file with a plausible name need not be parseable.

Keep session names separate from account existence and process identity. A home directory named after an account does not prove that account currently resolves. Conversely, absence from users output does not prove the account is missing or unused. A name can appear for multiple sessions; do not equate printed tokens with unique accounts. Use the intended account database to establish account existence and process identity evidence for a shell's authority.

Reference: [GNU users manual](https://manpages.debian.org/bookworm/coreutils/users.1.en.html).
