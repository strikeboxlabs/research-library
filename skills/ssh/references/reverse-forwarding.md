# Forward an owned client service to server loopback

Require an administrative forwarding task, approved SSH account/server, trusted host key, allowed server forwarding policy and a selected ordinary service reachable from the SSH client. Map roles before connecting: the listener is on the SSH server; destination loopback is on the client.

Define `ssh_target` as the known SSH alias or user@host, `server_port` as a free unprivileged server-side port and `client_service_port` as the observed client service port. Review effective configuration for additional forwards/local helpers and persistent multiplexing first. Keep the initial connection in the foreground:

~~~bash
ssh -N -T -o ExitOnForwardFailure=yes -R "127.0.0.1:$server_port:127.0.0.1:$client_service_port" "$ssh_target"
~~~

`-N` requests no command and `-T` no terminal. Explicit server loopback is the intended scope; verify the actual listener because server GatewayPorts policy can affect binding. A shell set to /bin/false alone is insufficient to infer forwarding rejection; authentication/PAM and forwarding policy still apply. Do not change those policies to force a failed task.

Setup failure, authenticated transport and successful application use are separate observations. ExitOnForwardFailure detects forward setup failure, not future destination-connection errors. Test the intended application from server loopback and retain its result. Stop the tracked foreground connection with Ctrl-C, then verify the server listener closes; account separately for any multiplexed/persistent connection.

See [OpenSSH remote forwarding](https://man.openbsd.org/ssh.1) and [server listener policy](https://man.openbsd.org/sshd_config.5).
