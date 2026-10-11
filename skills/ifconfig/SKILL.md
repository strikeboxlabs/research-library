---
name: ifconfig
description: Inspect Linux interface addresses, flags and counters with net-tools ifconfig. Use when active-only output, container namespaces or address assumptions obscure the local network evidence.
---

# Inspect interface status

Read this entire SKILL.md before acting. Verify the installed implementation with `ifconfig --help`; these are net-tools read-only forms. Select the current network namespace and requested interface evidence; no conditional resources are needed. Complete it with observed interface/address/flag data and visibility limits. A missing command or interface leaves a prerequisite gap.

List available interfaces, including down ones:

~~~bash
ifconfig -a
~~~

Without `-a`, the no-argument command shows active interfaces only. Define `interface` from the actual listing and inspect that interface:

~~~bash
ifconfig "$interface"
~~~

One interface argument displays status; additional address/configuration operands can change it. Read `inet`, netmask and broadcast as local address information. A container's address does not identify its host gateway, and a familiar subnet does not prove Docker topology. Correlate routes and the relevant namespace before selecting a peer.

An **illustrative** `inet 172.16.20.3 netmask 255.255.255.0` identifies that interface's `/24`, not permission to scan it or proof every address is reachable. NAT, a proxy or another namespace can make this address differ from a previously reached external IP. This display does not enumerate policy routing, every namespace or the public address.

Retain flags, MTU, counters and observation time. UP is administrative state; UP/RUNNING and accumulated packet counters do not establish current application reachability. A single sample cannot measure traffic over a selected interval. Preserve command errors rather than treating them as an empty interface inventory. If the installed tool is absent, another supported interface reader can answer the question; installation is a separate action.

See the packaged [net-tools ifconfig manual](https://manpages.debian.org/bookworm/net-tools/ifconfig.8.en.html).
