---
name: nc
description: Open a selected TCP connection or listener using OpenBSD-style nc on Linux. Use for bidirectional callbacks, stdin EOF, listener binding and netcat-variant option differences.
---

# Selected netcat transport

Read this entire SKILL.md before acting; reuse complete current context. Confirm that the installed `nc` implements the OpenBSD-style options below, identify which side connects/listens and use the worker's session budget. Finish with peer/received-byte evidence and the protocol or effective-identity result actually observed; a socket alone proves neither.

Read `nc -h` and the installed manual. Traditional netcat, OpenBSD nc, BusyBox nc and Nmap Ncat have different CLI contracts. A copied `nc -lvp PORT` is not universal: upstream OpenBSD nc does not combine `-l` with source-port `-p`. This package uses a positional listening port. Do not assume `-e` starts a shell; implementations assign different meanings or omit it.

For one intended incoming TCP connection, define `bind_ip` as a selected local address reachable from the connecting side and `port` as an available unprivileged port. Keep the listener foreground:

~~~bash
nc -l -n -v "$bind_ip" "$port"
~~~

stdin sends bytes to the peer; received bytes go to stdout and diagnostics to stderr. An explicit loopback bind is reachable only locally. A listener cannot repair callback routing/firewall policy, and an accepted peer can be a relay. `-w` does not bound this implementation's listening wait: use the worker's overall deadline and stop this owned process. `-k` deliberately accepts further connections; shared output then loses per-connection boundaries.

For a selected outgoing connection, define `host` as its numeric address:

~~~bash
nc -n -v -w 5 "$host" "$port"
~~~

`-w` limits connection/idle waits rather than a busy session's total duration. With `-n`, use actual numeric addresses. A silent connection can be waiting for the protocol's request. Do not confuse displayed line editing with the remote process having a terminal.

For a finite reviewed protocol request, define `request_file` as its exact framed bytes and `response_file` as a new private output. On a verified implementation supporting `-N`:

~~~bash
umask 077
(set -C; nc -n -N -w 5 "$host" "$port" < "$request_file" > "$response_file")
~~~

`-N` shuts down the socket's sending side after stdin EOF, allowing servers that wait for EOF to finish; it still receives their reply. Other nc variants use different EOF options. Preserve final status and framing/completeness; timeout bytes can be partial. A raw listener does not generate an HTTP response automatically.

An already authorized command channel is two-way transport, not a terminal or privilege transition. Correlate the actual remote `id`/result with the selected channel; a root-looking prompt or callback after a file write is insufficient alone. Shell/FIFO plumbing can block or retain children independently of nc; do not copy a compound cleanup/launch string merely to test transport. Stop the owned session and its tracked components when the selected question ends.

Reference: [OpenBSD nc manual](https://man.openbsd.org/nc). Match its option subset against the Linux image's installed port before use.
