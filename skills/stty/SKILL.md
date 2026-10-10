---
name: stty
description: Inspect, save and restore GNU stty terminal settings and deliberately adjust a local relay terminal or remote PTY. Use for doubled echo, raw input, Ctrl-C behavior and incorrect terminal dimensions.
---

# Select the terminal before changing it

Read this entire SKILL.md before acting. Establish which owned terminal is local and which is the remote child. Save existing settings before changing them and restore that same terminal afterward. Read [relay and recovery](references/relay-and-recovery.md) fully before using raw mode/job control. Finish with the intended input/echo behavior and restored local state; a PTY allocated remotely does not configure the local relay.

In an interactive session with a controlling terminal:

~~~bash
tty_state=$(stty -g </dev/tty) || exit
stty -a </dev/tty
stty size </dev/tty
~~~

`-g` produces a restorable settings token; quote it as one argument. GNU stty does not include the terminal window size in this token. Record dimensions separately if changing them. By default stty operates on stdin, so redirected/piped input may select no terminal; `/dev/tty` explicitly selects this process's controlling terminal. A worker without one must request/use the harness's PTY facility or inspect a deliberately selected owned device with GNU `-F`, rather than changing a guessed terminal.

~~~bash
stty "$tty_state" </dev/tty
~~~

`stty sane` is a fallback to conventional settings, not restoration of the saved state. `raw` disables canonical processing and signal handling among other transformations; `-echo` disables terminal echo separately. Setting `TERM` changes application interpretation, not these settings or the actual terminal emulator. See [GNU stty modes and restoration](https://www.gnu.org/software/coreutils/manual/html_node/stty-invocation.html).
