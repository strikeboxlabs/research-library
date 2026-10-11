---
name: pgrep
description: Find visible Linux processes by a selected name pattern with procps pgrep. Use when a script confuses no name match, process lookup failure and application health.
---

# Interpret a process-name lookup

Read this entire SKILL.md before acting. Confirm procps with `pgrep --version`, select the current PID namespace and establish the intended process-name pattern. No conditional resources are required. Finish with matched PIDs, status, observation time and visibility limits; a name match does not establish application health.

Define `name_pattern` as the selected extended regular expression, deliberately escaping regex characters when matching a literal name. Inspect names together with PIDs:

~~~bash
pgrep -l -x -- "$name_pattern"
status=$?
~~~

`-x` requires a whole-name regex match; it does not turn the pattern into literal text. For example, a literal dot requires `\.` in the pattern. Without `-f`, matching uses the process name, limited to 15 characters on Linux; a script filename may instead appear only in its interpreter's command line. Use `-f` only when that different full-command-line question is intended.

Status **0** means at least one match, **1** no match, **2** a syntax error and **3** a fatal error. Do not collapse every nonzero status into “service stopped.” Matches can include defunct processes. Namespace/procfs permissions limit the inventory, and a process can exit or its PID be reused before the next observation. Correlate a relevant match with the established service status or expected application response; do not start a program solely because a name lookup returned nothing.

See the packaged [procps pgrep manual](https://manpages.debian.org/bookworm/procps/pgrep.1.en.html).
