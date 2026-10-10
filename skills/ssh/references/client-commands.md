# Distinguish local SSH helpers from the remote login

Read unfamiliar configuration as text before invoking SSH with it. Includes and `Match exec` can select or execute local material even while `ssh -G` evaluates settings. Once `config` is an absolute path to a fully reviewed configuration (including its includes and match conditions), and `destination` is the intended host alias, inspect effective options without connecting:

~~~bash
ssh -G -F "$config" "$destination"
~~~

Check the actual `user`, `hostname`, `port`, `proxycommand`, `localcommand` and `permitlocalcommand` settings that are present. `-F` selects that configuration instead of the normal user configuration and causes the system configuration to be ignored. This output establishes evaluated options, not authentication, execution of a connection-time helper or a working forward.

| Mechanism | Where and when it acts |
|---|---|
| `Match exec` | Local command while deciding configuration matches, including during `-G`. |
| `ProxyCommand` | Local helper supplying the SSH connection transport. Its presence is not remote shell execution. |
| `LocalCommand` with `PermitLocalCommand=yes` | Local command after a successful connection, through the user's shell. Default permission is no. It runs synchronously and has no access to the SSH session; it is not designed for interactive commands. |
| A command after the SSH destination | Remote command request, subject to server/account policy. |

For privileged launchers, distinguish the SSH client's local execution identity from the account named by `user@host`. An ordinary remote login does not lower the local client's privilege. A broadly permitted privileged SSH client may therefore expose local helper capabilities; evaluate the exact policy/options/configuration and installed behavior rather than concluding that permission is limited to remote access. Do not run a privileged helper just to substantiate a configuration finding.

If an unexpected local action occurs only after authentication, inspect `LocalCommand` and its permission before blaming the remote shell. Conversely, a failed connection does not demonstrate what a post-connection hook would do. `PermitLocalCommand=no` controls that feature, not every other local command mechanism. Keep a policy finding, evaluated configuration and observed runtime effect distinct.

References: [SSH invocation and -F/-G](https://man.openbsd.org/ssh.1), [client configuration mechanisms](https://man.openbsd.org/ssh_config.5).
