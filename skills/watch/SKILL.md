---
name: watch
description: Observe repeated read-only directory or systemd timer output with procps-ng watch. Use when command re-parsing or sampled screen updates are mistaken for a complete event log or completed service execution.
---

# Observe the selected read-only command

Read this entire SKILL.md before acting. Select the known directory or timer, read-only command and observation window. Require installed procps-ng watch and an interactive terminal; timer observation also requires the intended running systemd manager. There are no conditional resources. Finish with observed samples and timing/visibility limits; an unavailable terminal or failed command leaves an evidence gap.

Check `watch --help` for this implementation. Define `directory` as an absolute directory you are authorized to observe:

~~~bash
watch -n 2 -d -x ls -la -- "$directory"
~~~

`-x` passes arguments directly to the command, avoiding another shell parse. The invoking shell expands the quoted variable once; watch does not expand wildcards, pipelines or redirections in this mode. Without `-x`, the command is interpreted through a shell on every run, so choose that behavior explicitly before adding shell syntax.

`-d` highlights changed displayed output. This polls snapshots; short-lived changes between runs and output outside the visible screen can be missed. A newly visible filename alone proves neither its contents nor which process created it. Treat command errors separately from an unchanged listing.

End the observation with Ctrl-C. Record the interval, selected path and actual observation window; capture selected evidence separately if it must persist. Watch's screen is not a durable or complete event history.

For a selected scheduled task, define `timer` as the exact `.timer` unit and use the intended system manager:

~~~bash
watch -n 2 -d -x systemctl --no-pager --full list-timers --all "$timer"
~~~

For a user manager, add `--user` to the systemctl arguments in the selected user's session. Preserve UNIT and ACTIVATES separately: the timer is not the service it triggers. NEXT/LAST describe trigger timing, not completed backup/application work. The displayed gap between samples does not establish the configured recurrence. Follow the selected unit's configuration, service result and output separately; do not start it to improve a read-only observation. See [systemctl timer fields](https://github.com/systemd/systemd/blob/main/man/systemctl.xml).

See the distribution's [procps-ng watch manual](https://manpages.debian.org/bookworm/procps/watch.1.en.html) for implementation differences.
