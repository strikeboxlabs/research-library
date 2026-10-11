---
name: ps
description: Inspect Linux process identity, state and arguments with procps ps and targeted procfs reads. Use when truncated command lines, NUL separators, namespaces or mutable process metadata obscure the evidence.
---

# Tie process evidence to a PID and time

Read this entire SKILL.md before acting. Select the intended process set or PID in its namespace, then preserve identity/start time and complete relevant arguments. Finish with the scoped snapshot and visibility limits; a PID or displayed account name is not proof of another process's authority.

Confirm the procps implementation with `ps --version`. For this user's processes, including ones without a controlling terminal, use BSD-style selectors:

~~~bash
ps ux
~~~

`u` selects a user-oriented display; `x` includes this effective user's processes without a terminal. This is not every process on the machine. `ps -e` deliberately selects all visible processes instead; option personalities can differ, so don't mix dashed and BSD forms casually. A `systemd --user` row is a user's manager, not necessarily PID 1. Choose its current PID and retain start time before using it with another process-specific tool.

For a known decimal `pid`, take an explicit snapshot:

~~~bash
ps -ww -p "$pid" -o pid=,ppid=,euid=,ruid=,stat=,lstart=,args=
~~~

`-ww` avoids ordinary display-width truncation. Effective and real UID are distinct; a command containing `su user` or a session named `root` does not establish the child's current credentials. A parent shell loop can recreate a child under a new PID. Keep PID, start time and process relationship together when comparing observations; PIDs can be reused.

For normal argument boundaries, inspect the targeted procfs file without storing its NUL-containing bytes in a shell variable:

~~~bash
tr '\000' '\n' < "/proc/$pid/cmdline"
~~~

Arguments are normally NUL-separated, not missing spaces. The newline display is for reading; arguments can themselves contain newlines, so preserve raw bytes for exact reconstruction. Processes can alter this memory. An empty result can reflect a zombie or another process type without ordinary arguments; a vanished PID, denied read and empty file are different findings.

| Procfs path | Meaning |
|---|---|
| `/proc/cmdline` | Kernel boot command line. |
| `/proc/PID/cmdline` | That process's exposed argument memory. |
| `/proc/self/...` | The process performing the read, in its procfs/PID namespace. |
| `/proc/PID/environ` | Initial environment area, normally NUL-separated; not necessarily later environment changes. |

For an acquired API file-read capture, `self` refers to the server-side reader, not the curl process on the workstation. Treat environment fields such as `PWD`, `USER`, `LOGNAME`, `APP_MODULE` or a virtualenv path as leads; they do not independently prove effective UID, current working directory or exact imported module. Correlate current process credentials and the selected cwd/exe links when accessible. A process's root link describes its filesystem view and remains subject to namespace/access limits; procfs is not an unrestricted copy of every host file. Environment captures may contain credentials; retain only relevant evidence privately.

`ps` is a snapshot, not complete process history or listener ownership proof. `STAT` value `T` denotes a stopped process: Ctrl-Z normally suspends a foreground job rather than resuming it in the background. Permission and namespace limits can hide relevant processes; do not report absence solely from a restricted listing.

If ps aux displays only one user's processes, keep that restricted observation rather than changing aux's ordinary all-process selection semantics. Procfs hidepid/namespace restrictions or an incomplete capture can limit visibility. Establish the actual mount/namespace and completion before attributing it to a specific restriction; do not change procfs policy merely to diagnose the listing. See [kernel procfs visibility](https://www.kernel.org/doc/html/latest/filesystems/proc.html).

Sources: [procps ps](https://man7.org/linux/man-pages/man1/ps.1.html), [cmdline](https://man7.org/linux/man-pages/man5/proc_pid_cmdline.5.html), [environment](https://man7.org/linux/man-pages/man5/proc_pid_environ.5.html), [self](https://man7.org/linux/man-pages/man5/proc_self.5.html), [boot command line](https://man7.org/linux/man-pages/man5/proc_cmdline.5.html).
