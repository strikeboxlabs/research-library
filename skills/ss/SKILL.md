---
name: ss
description: Inspect Linux listeners and connections with iproute2 ss. Use to distinguish loopback binding, remote reachability, hidden process ownership and the wrong network namespace.
---

# Find the actual listener

Read this entire SKILL.md before acting. Select the namespace, protocol and endpoint; finish with observed binding/state/visible ownership and its limits, not a reachability claim from a wildcard address.

Use `ss -V` to identify iproute2. With no options, `ss` does not show the listener inventory wanted here. Start with numeric TCP/UDP listeners:

~~~bash
ss -lntup
~~~

Read **Local Address:Port**, not the peer wildcard. A local `127.0.0.1:8080` listener is bound to IPv4 loopback. `0.0.0.0:8080` means all local IPv4 addresses, but does not establish firewall or remote reachability. `[::]:8080` is an IPv6 wildcard; IPv4 acceptance also depends on socket/kernel configuration. Test the required family rather than inferring it from this row.

A local `[::ffff:127.0.0.1]:8080` row represents an IPv4-mapped loopback address through the IPv6 API. It does not mean an IPv6 wildcard or a remotely bound service. Preserve the complete local address when explaining why a workstation scan differs from this namespace's listener inventory; an external port scan cannot inventory loopback-only bindings. See [Linux IPv4-mapped address semantics](https://manpages.debian.org/bookworm/manpages/ipv6.7.en.html).

For a specific observed TCP port, define `port` as its decimal number:

~~~bash
ss -lntp "sport = :$port"
ss -ntp state established "( sport = :$port or dport = :$port )"
~~~

The first command checks local listeners. The second checks established connections involving that port; it is not a substitute for the first. A UDP `UNCONN` row is not evidence of a failed TCP-style handshake.

`-p` requests process information, which may be incomplete for the current user or procfs visibility. A socket row without PID/program still establishes a socket; it does not prove that no process owns it. A config file's `User` directive is also not proof of the current owning process.

Results describe the network namespace where the command runs. A container, host and named namespace can have different inventories; inspect the intended namespace through the existing administration mechanism if necessary. Preserve the endpoint, family, state, time and any visible owner. Correlate with an application request or packet observation before declaring a service reachable or healthy.

Sources: [iproute2 ss manual](https://github.com/iproute2/iproute2/blob/main/man/man8/ss.8).
