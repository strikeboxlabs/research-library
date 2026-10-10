---
name: ifconfig
description: Inspect Linux net-tools interface addresses, netmasks and link counters with ifconfig. Use when an internal execution vantage differs from an external address and subnet or route assumptions need correction.
---


# Inspect the current interface vantage

Read this entire SKILL.md before acting. Verify the installed implementation with `ifconfig --help`; these are net-tools read-only forms. Finish with the observed interface/address/netmask in this namespace and separately supported routing or reachability conclusions.

~~~bash
ifconfig -a
~~~

Without configuration arguments, ifconfig displays interfaces; `-a` includes down interfaces. Bare ifconfig normally shows active ones. Supply a known interface name alone to inspect it; adding addresses, `up`, `down` or `netmask` changes configuration and is a separate task.

An **illustrative** `inet 172.16.20.3 netmask 255.255.255.0` identifies that interface's `/24`, not permission to scan it or proof every address is reachable. The server can sit behind NAT, a proxy or a different network namespace, so this address need not equal the previously reached external IP. `UP` is administrative state; counters are accumulated observations, not a successful connection to the desired peer. Correlate with routes and an actual application response before assigning a network boundary.

This display does not enumerate policy routing, every namespace or the public address. If the installed tool is absent, do not recreate or install it merely to obtain this display; another supported interface reader can answer the same question. See the [net-tools manual source](https://github.com/ecki/net-tools/blob/master/man/en_US/ifconfig.8).
