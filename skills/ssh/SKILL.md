---
name: ssh
description: Use OpenSSH for selected-account/key logins, SSH application/chat services, authorized public-key enrollment, loopback forwarding and dynamic SOCKS connections. Diagnose key passphrases, authentication, DNS location, client hooks and configuration effects.
---

# SSH connections and local forwarding

Read this entire SKILL.md before acting; reuse complete current context. Map the client, SSH server and destination before connecting. If options/configuration can execute local helpers or a privileged launcher is involved, read [client commands](references/client-commands.md) fully first. For an authorized public-key installation through an established filesystem write, read [selected authorized-key change](references/authorized-key-change.md) fully first. For a selected private key or confusing password prompt, read [key authentication](references/key-authentication.md) fully first. For a selected Kerberos/GSSAPI login or name-mapping discrepancy, read [GSSAPI identity and delegation](references/gssapi-identity.md) fully first. Finish with observed authentication/tunnel behavior or the supported configuration finding; authenticated transport alone is not destination success.

For an SSH endpoint exposing an application/chat interface, a legacy host-key negotiation failure or a fork-specific file command, read [SSH application services](references/application-services.md) fully before that procedure.

For a selected administrative connection through a dynamic SOCKS listener, read [dynamic forwarding and DNS](references/dynamic-forwarding.md) fully before that procedure.

For an approved client-side service exposed through an SSH server's loopback listener, read [reverse forwarding](references/reverse-forwarding.md) fully before starting it.

For an acquired forwarding command whose client/server direction or destination port disagrees with the prose, read [forwarding evidence](references/forwarding-evidence.md) fully before interpreting it. This is a static evidence task.

For an authorized interactive login, define `ssh_host`, `ssh_port` and `user` as the verified SSH endpoint and selected OS account. Confirm its host key through the established trust process, then use the intended credential mechanism:

~~~bash
ssh -p "$ssh_port" "$user@$ssh_host"
~~~

A password obtained from a database setup file is a candidate for that database account, not automatically this Linux account. An authentication failure is specific to the endpoint, account, method and attempt; it does not disprove a separately evidenced reuse with another selected account. Check the server authentication trace before attributing the failure to the secret. Do not put a password in the command line; use the approved prompt/credential mechanism. An authenticated session and observed remote identity establish the login result; a changed prompt alone does not.

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
