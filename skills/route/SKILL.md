---
name: route
description: Inspect the legacy Linux net-tools IPv4 route table or add and remove one approved static network route. Use for gateway, netmask, interface and VPN route discrepancies.
---

# Legacy IPv4 route inspection

Read this entire SKILL.md before acting. Require the selected network namespace and net-tools implementation. For a change, also require authority over the route, a configured interface, a reachable gateway and the exact approved prefix/metric. Finish with the observed table and selected-path evidence; remove only the unchanged route created for a temporary task.

~~~bash
route --version
route -n
~~~

Numeric output avoids name-resolution ambiguity. Read Destination, Gateway, Genmask, Flags, Metric and Iface together: `U` means up, `G` means gateway, `H` means a host route. A connected entry with no gateway and a gatewayed network are different paths. This legacy FIB view is not a complete policy-routing inventory; when available, `ip route get "$service_ip"` corroborates the selected path for that destination in the same namespace. Missing iproute2 leaves that selected-path check unresolved. Neither table proves an application responds.

For a separately approved addition, define `network` as a specific IPv4 CIDR network, `gateway` as its already reachable next hop, `metric` explicitly, and `interface` as the configured device. Capture the baseline and confirm the exact route is absent; do not replace an existing route or default route to resolve a failed add.

~~~bash
sudo route add -net "$network" gw "$gateway" metric "$metric" dev "$interface"
route -n
~~~

Retain diagnostics and inspect the resulting prefix/mask, gateway, metric and interface. A failed add or unchanged table is incomplete; check the intended namespace and gateway reachability before retrying. A VPN's completed handshake does not establish every desired route. For a temporary addition, after confirming that this exact entry still belongs to the task:

~~~bash
sudo route del -net "$network" gw "$gateway" metric "$metric" dev "$interface"
route -n
~~~

Verify the task's entry is absent and unrelated baseline routes remain. For option differences, use the [net-tools route manual](https://manpages.debian.org/bookworm/net-tools/route.8.en.html).
