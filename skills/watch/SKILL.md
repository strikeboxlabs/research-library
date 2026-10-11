---
name: watch
description: Observe repeated read-only command output in a terminal with procps-ng watch. Use for selected directory changes, command re-parsing and distinguishing sampled screen output from an event log.
---

# Watch a selected directory

Read this entire SKILL.md before acting. Select the known directory, read-only command and observation window. This task requires installed procps-ng watch and an interactive terminal; there are no conditional resources. Complete it with the observed samples and timing/visibility limits. An unavailable terminal or failed command leaves an evidence gap.

Check `watch --help` for this implementation. Define `directory` as an absolute directory you are authorized to observe:

~~~bash
watch -n 2 -d -x ls -la -- "$directory"
~~~

`-x` passes arguments directly to the command, avoiding another shell parse. The invoking shell expands the quoted variable once; watch does not expand wildcards, pipelines or redirections in this mode. Without `-x`, the command is interpreted through a shell on every run, so choose that behavior explicitly before adding shell syntax.

`-d` highlights changed displayed output. This polls snapshots; short-lived changes between runs and output outside the visible screen can be missed. A newly visible filename alone proves neither its contents nor which process created it. Treat command errors separately from an unchanged listing.

End the observation with Ctrl-C. Record the interval, selected path and actual observation window; capture selected evidence separately if it must persist. Watch's screen is not a durable or complete event history.

See the distribution's [procps-ng watch manual](https://manpages.debian.org/bookworm/procps/watch.1.en.html) for implementation differences.
