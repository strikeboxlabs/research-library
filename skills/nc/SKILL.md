---
name: nc
description: Use the installed nc/netcat implementation for a selected TCP exchange, owned file transfer or incoming callback. Choose traditional versus OpenBSD options and diagnose EOF/listener differences; load process-stream attachment only when that task is authorized.
---

# Netcat TCP exchanges

Read this entire SKILL.md before acting; reuse complete current context. Identify the installed implementation with `nc -h` and its manual before selecting a command below. For a selected owned binary-file transfer, read [finite file transfer](references/file-transfer.md) fully first. For an authorized executable attached to a TCP stream, read [executable or FIFO process streams](references/process-streams.md) fully first. Finish with the received bytes and protocol/identity evidence; connecting alone is not application success.

Define `host`/`port` as the selected TCP endpoint and `request`/`response`/`log` as exact input and fresh private output files. For ordinary traditional or OpenBSD-style TCP interaction:

~~~bash
umask 077
nc -n -v -w 5 "$host" "$port" <"$request" >"$response" 2>"$log"
~~~

Use numeric `host` with `-n`. Choose framing from the actual protocol; nc does not turn arbitrary bytes into an HTTP request or guarantee a CRLF/body terminator. Check status, stderr and the complete protocol reply. EOF/timeout semantics vary: OpenBSD `-N` half-closes the sending side on stdin EOF, while traditional Debian `-q` controls delay before quitting after EOF. Do not add a short quit delay when the required reply may arrive later. BusyBox nc and Linux ports can differ too; match the installed contract.

For a finite request on a verified OpenBSD-style implementation supporting `-N`, retain the reply after sending EOF and avoid replacing an existing response file:

~~~bash
(set -C; nc -n -N -w 5 "$host" "$port" <"$request" >"$response" 2>"$log")
~~~

Check final status and the received protocol's framing/completeness; timeout output can be partial. A silent interactive connection can be waiting for a request, not proving the service absent.

## Check one selected TCP port without sending application data

On a verified traditional/OpenBSD-style implementation supporting these flags:

~~~bash
nc -n -v -z -w 5 "$host" "$port"
~~~

Use a numeric host and one selected positive TCP port. A successful TCP connection tests that endpoint at this vantage/time, not the service's authentication or future reachability. Retain status/stderr; a timeout differs from an explicit refusal. -z selects zero-I/O scanning, not a security boundary for additional options. Do not combine it with an executable-attachment option merely to reproduce a reachability check.

## Listen on an explicit interface

Define `bind_ip` as the authorized reachable address and `port` as an available permitted port. Select **one** command matching the installed implementation, in a tracked foreground session:

~~~bash
# Traditional netcat:
nc -n -v -l -s "$bind_ip" -p "$port" >"$response" 2>"$log"
# OpenBSD-style nc:
nc -n -v -l "$bind_ip" "$port" >"$response" 2>"$log"
~~~

The options are alternatives, not two listeners to start together. On upstream OpenBSD, `-p`/`-s` cannot accompany `-l`, and `-w` is ignored in listen mode. Linux ports can differ; local help/manual wins. OpenBSD `-k` deliberately accepts further connections; shared output loses per-connection boundaries. Stop the owned listener under the worker's overall budget; a connect timeout is not a guaranteed bound waiting for the first callback. A bind failure leaves no listener. Loopback is reachable only from that host.

Capture peer/time diagnostics separately from bytes. An HTTP request received on this stream does not imply a valid HTTP response, imported JavaScript execution or authenticated identity. A remote process stream is also different from a pseudo-terminal; missing prompt/echo is not evidence of changed privilege. Shell/FIFO plumbing can block or retain children independently of nc; track those components separately instead of copying an unexplained cleanup/launch string. Keep the observed protocol/identity result and stop the owned session when finished.

References: [Debian traditional netcat](https://manpages.debian.org/bookworm/netcat-traditional/nc.1.en.html) and [upstream OpenBSD nc](https://man.openbsd.org/nc). These are different implementations; the OpenBSD `-e` TLS-name option is not traditional netcat's execute option.
