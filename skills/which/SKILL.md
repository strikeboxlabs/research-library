---
name: which
description: Locate a selected executable on the current PATH with the installed Linux which utility. Use when a walkthrough's interpreter name or a missing command must be resolved without claiming its version or task compatibility.
---

# Resolve the selected executable name

Read this entire SKILL.md before acting. Require the intended shell/environment and a known simple executable name. Check the installed which implementation's help; this task uses Debianutils-compatible PATH search. No conditional resources are required. Finish with status, returned path and the unresolved version/behavior questions.

Define `program` as the intended name, for example an interpreter name selected by the task:

~~~bash
which -- "$program"
status=$?
~~~

Check diagnostics and status. A returned executable path establishes a PATH candidate in this environment; it does not execute the program or establish its version, ABI, modules or provenance. In particular, finding `python` does not establish Python3 or availability of Unix pty. Verify the selected program through its normal version/help contract before its actual procedure.

No result can mean no executable was found on this PATH, not absence everywhere on the machine. A failed which invocation is a separate lookup failure. `which -a -- "$program"` on supporting implementations retains multiple PATH candidates instead of silently choosing the first. Shell functions, aliases, builtins and hashed command lookup can make the shell choose differently from an external PATH-search utility; use the shell's `type` when diagnosing that discrepancy. Do not install a tool or alter PATH solely to turn a missing lookup into success.

Reference: [Debianutils which manual](https://manpages.debian.org/bookworm/debianutils/which.debianutils.1.en.html); other implementations can inspect aliases or use different statuses/options.
