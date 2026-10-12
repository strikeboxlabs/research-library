---
name: netstat
description: Inspect Linux net-tools listeners and routes or Windows netstat.exe through an established Windows session. Use when address roles, namespace, protocol state or missing process ownership changes the interpretation.
---

# Linux listeners with netstat

Read this entire SKILL.md before acting; reuse complete current context. Select implementation, protocol, address family and namespace before interpreting rows. For Windows native output through an established Windows session, read [Windows listeners](references/windows-listeners.md) fully before its commands; the inline commands are Linux net-tools. For routes, use the routing section below. Finish with the selected socket or route evidence and its observation scope. A listing alone does not prove remote reachability or application authorization.

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

## Read the current namespace's routes

For numeric IPv4 routing entries with the same verified net-tools implementation:

~~~bash
netstat -4 -rn
~~~

Keep destination, gateway, mask, flags and interface together. A destination and mask both shown as `0.0.0.0` identify a default route; the gateway column names its next hop, not this process's local address. More specific routes can select another path. A connected subnet entry does not enumerate every peer or establish a Docker host relationship. Correlate an interface-address observation when the local address matters.

This view belongs to the current network namespace. It is not an inventory of every namespace or policy-routing rule, and a configured route does not establish that the gateway or application responds. Preserve command failures and observation time; do not infer an empty network from missing route output. Use the image's policy-aware routing query when the task needs an actual destination/source lookup.

See the [net-tools manual](https://manpages.debian.org/bookworm/net-tools/netstat.8.en.html) for protocol/family, route and process-visibility details.
