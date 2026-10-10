---
name: pspy
description: Observe short-lived Linux commands and scheduled jobs without root using pspy. Use to interpret process timestamps and UID evidence while accounting for missed processes and procfs visibility.
---

# pspy process observation

Read this entire SKILL.md before acting; reuse complete current context. Select the process or filesystem observation below, establish the time window and visibility, then retain the transcript and supported identities/events. Missing process details remain unknown; a file event alone cannot complete an execution/UID claim.

Choose a build matching the machine's architecture. Upstream `pspy64`/`pspy32` are the larger static builds; the `s` suffix marks smaller libc-dependent builds, not the static ones. An executable-format or loader error calls for checking architecture/build, not adding privileges. Define `pspy_bin` as the verified local executable and check its `--help`.

Define `log` as a fresh private transcript and `seconds` as an observation window covering the suspected schedule:

~~~bash
umask 077
timeout --signal=INT "$seconds" "$pspy_bin" -p -i 1000 >"$log" 2>&1
~~~

`-i` is the procfs scan interval in **milliseconds**. `timeout` ending the observation normally returns a timeout status; inspect the transcript before calling that a pspy failure. Command lines may contain credentials.

pspy scans `/proc` and uses filesystem inotify events to trigger extra scans. It first reports currently visible processes, then newly observed ones. It is not a complete kernel execution audit. Short lifetimes, unreadable procfs entries, namespaces and watcher limits can leave gaps; `???` fields mean missing information, not a special account. Use `--debug` to diagnose hidden watcher/read errors.

For a focused investigation, `-r directory` watches recursively and `-d directory` watches only that directory; inspect the startup summary to confirm the resulting watch set. These controls change filesystem triggers, not a guaranteed filter on which process commands are printed. `-f` also prints file events, which can be noisy and do not establish which process caused each event.

When only your own processes appear, inspect the current procfs mount options (for example `findmnt -no OPTIONS /proc`). `hidepid=2` hides other users' process directories subject to exemptions; more frequent polling does not override it. If the relevant filesystem is accessible, define `watch_dir` as that observed directory and `fs_log` as a fresh private file:

~~~bash
timeout --signal=INT "$seconds" "$pspy_bin" -p -f -r "$watch_dir" -i 1000 >"$fs_log" 2>&1
~~~

Check the printed watcher set and errors. Repeated `OPEN`, `ACCESS` or `CLOSE_NOWRITE` events near a schedule support a file-access lead, not execution, reader UID or the complete command line. File inspection itself can create events. Acquire the relevant file/configuration for static inspection or obtain separately authorized process evidence; do not report a bypass of procfs visibility. See [kernel procfs visibility](https://docs.kernel.org/filesystems/proc.html#mount-options).

Correlate timestamps, UID, PID and command with the suspected job. Seeing UID 0 execute a script does not establish that you can modify the script or its dependencies. Check the actual file/configuration separately. No observed event during one window does not establish that no scheduled job exists. Finish with the observation interval and visibility limitations.

A command-line password can disappear before a scan because some MySQL clients overwrite it during initialization. A masked argument or missed event does not prove it was never exposed. Conversely, a captured value establishes argument exposure in that process, not successful database authentication or reuse as an operating-system password. Preserve a private original only when required; redact the value in the finding while retaining the executable, option, UID and timestamp. A shorter polling interval still cannot guarantee capture; see the client's [documented startup exposure window](https://dev.mysql.com/doc/refman/8.4/en/password-security-user.html).

For a task that already permits an application action, capture a baseline, perform one identifiable action and compare the subsequent process sequence. Background maintenance can appear at the same time; temporal proximity alone is not causation. Preserve the exact absolute path and interpreter. `/bin/sh /absolute/script` selects that file directly, so a writable entry in the observer's PATH does not explain its execution. Check both file-content permissions and directory replacement rights before describing a writable-script finding.


If observation appears stuck, inspect the existing process and log before restarting. In a terminal with job control, Ctrl-Z normally suspends the foreground job; it does not terminate a hung collector. Use `jobs -l` to identify a job suspended from the current shell and resume or stop that specific instance through normal job control. Do not accumulate suspended collectors. `--debug` exposes diagnostics; it is not a documented crash repair or guarantee of complete event coverage.

See [upstream flags and operation](https://github.com/DominicBreuker/pspy) and [Bash job control](https://man7.org/linux/man-pages/man1/bash.1.html).
