---
name: ip
description: Diagnose Linux address and route selection with iproute2 without changing network state. Use when local delivery, a more-specific prefix, policy routing or a namespace makes the observed path differ from a routing-daemon table.
---

# Explain the kernel's route choice

Confirm `ip -Version` and `ip route help`; BusyBox and older iproute2 builds may lack `fibmatch`, JSON or other selectors. Run queries in the network namespace of the affected process. The host, a container and a router namespace can have different addresses and rules. For an already identified named namespace, `ip -n "$namespace" ...` selects it when permitted; a named-namespace listing is not a list of every container namespace.

Define `destination` as the affected IPv4 address:

~~~bash
ip -brief -4 address show
ip -4 rule show
ip -4 route show table all match "$destination/32"
ip -4 route get "$destination"
ip -4 route get fibmatch "$destination"
~~~

Address output establishes local assignments. The matching route listing shows covering prefixes across tables, including `local`; it does not by itself select a route. Rules are evaluated in ascending priority number and can select different tables or terminal actions. The ordinary lookup resolves an output path and chosen source; `fibmatch` reports the underlying matched forwarding-table route. If unsupported, use the resolved output plus the relevant rule/table listing instead of treating a syntax error as no route.

`get` sends no packet to the destination. A result naming a gateway/interface establishes a lookup decision, not neighbor reachability, firewall permission, a listening service or the return path. `local ... dev lo` means local delivery in this namespace, even when the address was assigned to another interface. Compare the address inventory and local table before assuming traffic will leave through a gateway.

## Reproduce the relevant lookup inputs

For a locally originated flow, define `source_ip` as its actual source address:

~~~bash
ip -4 route get "$destination" from "$source_ip"
~~~

For a forwarded packet, use the observed remote source and receiving interface as `source_ip`/`incoming_interface`:

~~~bash
ip -4 route get "$destination" from "$source_ip" iif "$incoming_interface"
~~~

The second command models ingress forwarding rather than local output. If the rules depend on a mark, VRF, protocol or ports, include those observed selectors using the installed help. An unqualified lookup can otherwise answer a different question. These queries do not simulate the full firewall/NAT or application processing path.

**Illustrative:** installed `192.0.2.0/24` and `192.0.2.0/25` routes cover `192.0.2.10`. Within the selected table, the /25 is more specific; its larger metric does not make the /24 win. First resolve policy/table selection, then prefix length and applicable preferences. An unreachable/prohibit/blackhole route or rule needs interpretation as a deliberate action, not a missing default route.

Assigning an address normally also creates local and connected-prefix routing state, subject to flags such as `noprefixroute`. That alone does not prove BGP advertisement. Compare kernel state with the routing daemon's origination, redistribution and export evidence before attributing a route leak. Keep address changes, route replacement and flushing out of evidence collection.

References: [ip options and namespaces](https://man7.org/linux/man-pages/man8/ip.8.html), [route lookup](https://man7.org/linux/man-pages/man8/ip-route.8.html), [policy rules](https://man7.org/linux/man-pages/man8/ip-rule.8.html), [address flags](https://man7.org/linux/man-pages/man8/ip-address.8.html).
