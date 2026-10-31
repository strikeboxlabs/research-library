---
name: "pacu"
description: "Exploit misconfigurations in an AWS account you are authorized to test using Pacu's session-based module framework, chaining enumeration output into exploitation modules. Use after obtaining account credentials; not for accounts outside the engagement scope."
---

# Pacu AWS exploitation framework

Installed invocation: `/usr/bin/pacu`, version `1.7.0` (Kali package pacu; interactive console).

Read this entire SKILL.md before acting. Require credentials explicitly in scope for exploitation testing and a named Pacu session before starting. Finish with module results tied to their session; exploitation output is account state at test time, not a durable finding set.

Pacu is session-based: each session holds the AWS keys and the structured data every module writes, and later modules consume earlier modules' collected data. The normal shape is enumeration first, exploitation second:

~~~bash
/usr/bin/pacu --session "$engagement"
# inside the console: set_keys, then run enum modules (e.g. enum_users, enum_s3)
# then exploitation modules that consume the collected data (e.g. s3__download)
~~~

Keys and findings live in a per-user SQLite database (~/.local/share/pacu); a session is the audit boundary — do not mix engagement credentials into one session. Modules mutate account state (creating users, reading buckets, escalating roles); every module run is an authorized action, and `data` inside the console shows what has been collected before an exploit module acts on it.

A module that errors on permissions has still produced evidence: the IAM policy denial itself describes the boundary. Report what each module changed, not only what it found.

References: [project documentation](https://github.com/RhinoSecurityLabs/pacu).
