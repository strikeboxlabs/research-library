---
name: gdbserver
description: Debug a controlled remote Linux program through gdbserver and GDB. Use when transport exposure, remote versus extended-remote mode, symbol matching or inferior lifetime needs explicit handling.
---

# Treat the debug connection as process control

Confirm local GDB and remote gdbserver versions/architecture support. Match the local executable and debug symbols to the remote build; a filename match is insufficient. Running or attaching gdbserver starts or stops a real process and needs that specific debugging task to be in scope.

Gdbserver has no built-in authentication. Its documented TCP `host:port` form currently ignores the host component: spelling `127.0.0.1:port` is not a reliable loopback bind restriction. An exposed debugger is process-control access with the server account's privileges, not merely a version-specific exploit hypothesis. Prefer a verified SSH transport for an owned fixture.

Define `local_binary` as the matching local executable:

~~~bash
gdb -q -nx -iex 'set auto-load off' "$local_binary"
~~~

At the GDB prompt, replace the account, host and absolute program path below with the intended fixture values. These are GDB commands containing an SSH command, not shell-variable placeholders:

~~~text
target remote | ssh -T user@debughost gdbserver - /absolute/remote/program
info files
info registers
bt
~~~

Use trusted, correctly quoted command arguments and the established SSH host-key identity. `-T` avoids a remote PTY interfering with the debugger protocol. Keep shell startup chatter off protocol stdout. In this stdio mode the inferior's stdin is `/dev/null`, and its stdout/stderr are combined for display through GDB; an interactive-input fixture needs a different deliberate arrangement.

The remote process has already been started and stopped for debugging. Set an observed breakpoint and use `continue` or stepping as needed. `run` is not supported by ordinary `target remote`; starting/restarting inferiors through the protocol requires the appropriate `target extended-remote` setup, commonly with `gdbserver --multi`. Do not start another instance to conceal a mode error.

Record the stop, actual build and relevant state. Decide whether to terminate the owned inferior or deliberately detach and let it run, then verify remote process/server lifetime. `--once` limits reconnections, not authentication, and a supervisor loop may launch a replacement server after exit.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Backdoor pp. 9–11. Sources: [gdbserver](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Server.html), [connection modes](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Connecting.html).
