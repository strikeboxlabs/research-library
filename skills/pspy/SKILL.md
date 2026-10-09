---
name: pspy
description: Observe short-lived Linux commands and scheduled jobs without root using pspy. Use to interpret process timestamps and UID evidence while accounting for missed processes and procfs visibility.
---

# pspy process observation

Choose a build matching the machine's architecture. Upstream `pspy64`/`pspy32` are the larger static builds; the `s` suffix marks smaller libc-dependent builds, not the static ones. An executable-format or loader error calls for checking architecture/build, not adding privileges. Define `pspy_bin` as the verified local executable and check its `--help`.

Define `log` as a fresh private transcript and `seconds` as an observation window covering the suspected schedule:

~~~bash
umask 077
timeout --signal=INT "$seconds" "$pspy_bin" -p -i 1000 >"$log" 2>&1
~~~

`-i` is the procfs scan interval in **milliseconds**. `timeout` ending the observation normally returns a timeout status; inspect the transcript before calling that a pspy failure. Command lines may contain credentials.

pspy scans `/proc` and uses filesystem inotify events to trigger extra scans. It first reports currently visible processes, then newly observed ones. It is not a complete kernel execution audit. Short lifetimes, unreadable procfs entries, namespaces and watcher limits can leave gaps; `???` fields mean missing information, not a special account. Use `--debug` to diagnose hidden watcher/read errors.

For a focused investigation, `-r directory` watches recursively and `-d directory` watches only that directory; inspect the startup summary to confirm the resulting watch set. These controls change filesystem triggers, not a guaranteed filter on which process commands are printed. `-f` also prints file events, which can be noisy and do not establish which process caused each event.

Correlate timestamps, UID, PID and command with the suspected job. Seeing UID 0 execute a script does not establish that you can modify the script or its dependencies. Check the actual file/configuration separately. No observed event during one window does not establish that no scheduled job exists. Finish with the observation interval and visibility limitations.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Alert p. 13. Source: [upstream operation, flags and builds](https://github.com/DominicBreuker/pspy).
