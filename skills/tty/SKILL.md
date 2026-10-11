---
name: tty
description: Identify the terminal connected to stdin with tty and compare selected Unix session endpoints. Use when a su shell may share its caller's terminal, redirected stdin behaves differently or a terminal-dependent operation lacks its prerequisite.
---

# Identify stdin's terminal

Read this entire SKILL.md before acting. Run tty in the actual selected process/session context and retain its path or status. The result describes file descriptor 0; it does not by itself identify a controlling terminal, foreground process group or the identity of another reader.

~~~bash
tty
~~~

An **illustrative** /dev/pts/4 names this context's stdin terminal. Run it separately before and inside a selected account/session change when comparing endpoints. Equal names in the same device namespace support a shared endpoint; they do not prove parentage, ioctl permission or which shell will consume future input. A different namespace can give equal text names to different devices.

For a silent GNU test, inspect the status immediately:

~~~bash
tty -s
status=$?
printf 'tty_status=%s\n' "$status"
~~~

Zero means terminal stdin; 1 means non-terminal stdin. Incorrect arguments or output errors have other statuses, and newer GNU versions separately report failure to determine a terminal name. Preserve the implementation's diagnostic rather than treating every nonzero status as a missing PTY. `tty </dev/null` tests /dev/null, even if stdout remains on a terminal; piping into tty likewise changes its input. Use the real launch context for a terminal prerequisite.

For shared-terminal analysis, correlate the endpoint with actual process/session/foreground-group evidence and the launch command. A login shell does not necessarily allocate a new terminal. util-linux su --pty creates a separate pseudo-terminal on supporting versions, while ordinary su can inherit the caller's terminal. A tty path is a prerequisite observation, not evidence that injected input executed or elevated an identity.

See [GNU tty](https://manpages.debian.org/bookworm/coreutils/tty.1.en.html), [current GNU status definitions](https://github.com/coreutils/coreutils/blob/master/doc/coreutils.texi) and [su terminal behavior](https://github.com/util-linux/util-linux/blob/master/login-utils/su.1.adoc).
