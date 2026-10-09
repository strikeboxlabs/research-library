---
name: script
description: Use util-linux script to allocate a pseudoterminal or capture terminal-dependent program output. Use when pipes change behavior, exit status is lost or terminal transcripts need careful interpretation.
---

# util-linux script and PTYs

Check `script --version` and `script --help`: BSD and util-linux syntax differ. `script` runs a child through a pseudoterminal. It can help an application requiring a TTY, but does not repair the surrounding network transport, forward signals reliably across every relay or choose correct terminal dimensions automatically.

For an interactive Bash under a local PTY without a transcript:

~~~bash
script -q -e -c /bin/bash /dev/null
~~~

This starts a child shell; leave it with `exit` before closing the outer session. Confirm that `/bin/bash` is the intended installed shell. Do not infer that an existing basic network shell now has every property of an SSH terminal.

For a terminal-dependent program, define `transcript` as a fresh private output file and use a deliberately constructed fixed command after `-c`. For example, to record a shell session:

~~~bash
umask 077
script -q -e -c /bin/bash "$transcript"
~~~

`-e` propagates the child's exit status; without it, script's status is not a reliable substitute for the program's result. `-q` suppresses start/end announcements. A `-c` command is interpreted as shell command text, so do not splice untrusted arguments into it.

The transcript contains terminal output and echoed input, including escape sequences, carriage returns and potentially secrets. It is not a clean line-oriented log. `--log-in`/`--log-io` additionally capture input even when echo is disabled, including password entry; avoid these modes unless that capture is specifically intended. Output logging can still contain sensitive application output.

Piped stdin can leave a child waiting after EOF; prefer direct noninteractive execution when a PTY is unnecessary. Record whether the child exited normally, timed out or was interrupted, and retain the raw transcript separately from any cleaned presentation.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Altered p. 18. Source: [util-linux script manual](https://github.com/util-linux/util-linux/blob/master/term-utils/script.1.adoc).
