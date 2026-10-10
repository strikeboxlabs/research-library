---
name: ssh
description: Use OpenSSH for selected-key logins and remote loopback forwarding. Diagnose key passphrases, server authentication, client hooks and configuration effects without confusing local and remote identities.
---

# SSH connections and local forwarding

Read this entire SKILL.md before acting; reuse complete current context. Map the client, SSH server and destination before connecting. If options/configuration can execute local helpers or a privileged launcher is involved, read [client commands](references/client-commands.md) fully first. For a selected private key or confusing password prompt, read [key authentication](references/key-authentication.md) fully first. Finish with observed authentication/tunnel behavior or the supported configuration finding; authenticated transport alone is not destination success.

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

Use `ssh -v` for this connection when necessary. For unexpected configuration, follow the client-command reference before using `-G`: evaluating a config can itself execute `Match exec`. A copied config is not passive connection data.

A quiet foreground tunnel is normal. Stop it with Ctrl-C and confirm the local listener closes before claiming cleanup. If deliberately using multiplexing/background forwarding, track that separate connection's lifetime.

References: [ssh manual](https://man.openbsd.org/ssh.1), [forwarding configuration](https://man.openbsd.org/ssh_config.5).
