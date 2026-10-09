---
name: ssh
description: Reach a remote loopback service using OpenSSH local port forwarding. Use when diagnosing bind errors, remote destination failures, virtual-host mismatches or tunnel cleanup from Linux.
---

# SSH local forwarding

Map both ends before connecting: the listener is on the Linux client; the destination is reached from the SSH server. In `-L`, destination `127.0.0.1` means the SSH server's own loopback, not the workstation's.

Define `ssh_host` and `user` for the known SSH account, `local_port` as a free client port, and `remote_port` as the observed service port on the SSH server. Confirm the server's host key through the established trust process. Keep the first tunnel in the foreground:

~~~bash
ssh -N -T -o ExitOnForwardFailure=yes -L "127.0.0.1:$local_port:127.0.0.1:$remote_port" "$user@$ssh_host"
~~~

`-N` requests no remote command; `-T` avoids allocating a terminal. Explicit local loopback binding avoids exposing the forwarded service on every client interface. For a destination on a different authorized host, replace the destination loopback with the name/address reachable **from the SSH server**.

An IPv6 literal in the `-L` destination needs brackets: `-L "127.0.0.1:$local_port:[$destination_ipv6]:$remote_port"`, where `destination_ipv6` is the verified unbracketed address. This can expose an IPv6-only destination through a local IPv4 listener. Use a high local port and configure the consuming tool to use it explicitly; an SMB client silently using port 445 will not reach a forward on 1445. This remains a TCP forward.

In a second terminal, use the intended application against the local listener. For HTTP, preserve the application's expected hostname; reaching a forwarded IP/port with the wrong Host header can select a different virtual host. HTTPS also depends on SNI and certificate identity.

| Observation | Next check |
|---|---|
| Local bind fails | Inspect the occupied port or choose another; do not kill an unidentified process. |
| SSH authenticates, application fails | Check remote service/listener and SSH forwarding policy. `ExitOnForwardFailure` does not test future destination connections. |
| `administratively prohibited` | Inspect allowed forwarding destinations/policy; password retries are irrelevant. |
| Wrong page or TLS identity error | Check destination, application hostname and TLS naming. |

Use `ssh -v` for this connection when necessary; inspect effective options with `ssh -G "$user@$ssh_host"` if configuration is unexpected. A quiet foreground tunnel is normal. Stop it with Ctrl-C and confirm the local listener closes before claiming cleanup. If deliberately using multiplexing/background forwarding, track that separate connection's lifetime.

Documentation reviewed 2026-10-09; Linux execution untested. Cases: AdmirerToo p. 17; Agile p. 18; APT p. 8. Sources: [ssh manual](https://man.openbsd.org/ssh.1), [forwarding configuration](https://man.openbsd.org/ssh_config.5).
