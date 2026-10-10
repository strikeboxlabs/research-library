---
name: rsh
description: Use a GNU Inetutils rsh client for a selected legacy remote command and distinguish rsh execution from rlogin fallback. Use when diagnosing host-based trust, unexpected interactive login or remote input/output behavior.
---

# Select command execution or remote login deliberately

Read this entire file before acting. Confirm the installed implementation with `rsh --version` and `rsh --help`; this recipe describes GNU Inetutils. Finish with the actual client/protocol, selected host/user and observed command result.

For an authorized command on an existing legacy service, define `server` and `remote_user`:

~~~bash
rsh -n -l "$remote_user" "$server" 'id'
~~~

`-n` supplies no standard input, avoiding an unintended wait for input from the local terminal or pipeline. Omit it only when the remote command should consume stdin. Quote the remote command as one local-shell argument. For example, redirection inside the quoted command occurs remotely; redirection outside it writes on the local machine.

GNU rsh with no remote command invokes rlogin. A resulting interactive banner or connection to the login service therefore is not evidence that the command-execution service worked. Do not copy another implementation's `-v user@host` syntax without checking its help.

Classic r-command access depends on the daemon's trust policy, remote username and host identity, including applicable `.rhosts`/`hosts.equiv` rules and file permissions. A DNS answer or a mounted file seen inside a container is not proof of the host daemon's effective trust decision. Check the daemon-side context through the authorized administration path when a login is rejected; do not change DNS/trust entries as an automatic client repair.

This is a legacy protocol; ordinary deployments lack SSH-style confidentiality and server authentication. Use it only where that service and trust context are part of the task. A denied request can concern trust/policy rather than a bad password. Preserve command output and any remote error separately from transport errors; a remote banner alone does not establish the requested execution identity.

See [GNU rsh invocation](https://www.gnu.org/software/inetutils/manual/html_node/rsh-invocation.html).
