---
name: netstat
description: Inspect Linux net-tools TCP/UDP listeners, bound addresses and available process ownership. Use when an internal service port or wildcard address needs interpretation in the current network namespace.
---

# Linux listeners with netstat

Read this entire SKILL.md before acting; reuse complete current context. Select protocol, address family and namespace before interpreting rows. Finish with the observed local endpoint, state and any supported process identity; a socket listing alone does not prove remote reachability or application authorization.

Use Linux **net-tools** `netstat --version` and `netstat --help`; Windows netstat has different switches and output. For numeric TCP listeners in the current network namespace:

~~~bash
netstat -tln
~~~

`-t` selects TCP, `-l` listening sockets and `-n` numeric addresses/ports. Add `-4` or `-6` to select an address family deliberately. `-a` instead includes non-listening sockets; those rows answer a different question. For UDP bound sockets use `netstat -uln`; UDP has no TCP LISTEN state, so do not require that word in its output.

Read the **Local Address** column, not the foreign endpoint. **Illustrative:** a TCP row with local `127.0.0.1:8443`, foreign `0.0.0.0:*` and state `LISTEN` is bound to IPv4 loopback; the foreign wildcard does not make it a public listener. Local `0.0.0.0:8443` means all IPv4 interfaces in that namespace; local `:::8443` is an IPv6 wildcard whose IPv4 acceptance depends on socket/system policy. A specific interface address is distinct from either wildcard.

For available PID/program associations:

~~~bash
netstat -tlnp
~~~

`-p` can omit processes the current user cannot inspect. A dash or warning is missing attribution, not proof that no process owns the socket. Use an already permitted process view if ownership matters. Keep the full row and current process identity; PIDs can be recycled and sockets can close between observations.

To isolate a selected decimal port in Linux TCP output, define `port` first:

~~~bash
netstat -tln | awk -v p="$port" '$1 ~ /^tcp/ && $4 ~ (":" p "$") && $6 == "LISTEN"'
~~~

Matching any occurrence of a port with grep can select a foreign address, another port or unrelated output. An empty filtered result remains bounded by family/protocol, namespace, observation time and command completion. A loopback listener must be reached from that host/namespace or an authorized mapped forward; the workstation's localhost is a different endpoint. Wildcard binding still leaves routing, firewall and application policy to establish separately.

See the [net-tools manual](https://manpages.debian.org/bookworm/net-tools/netstat.8.en.html) for protocol/family and process-visibility details.
