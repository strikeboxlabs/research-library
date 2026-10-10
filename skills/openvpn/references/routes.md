# A running tunnel is not a working application path

Use the current client's log and the same network namespace as the worker. Define `vpn_if` as the actual tunnel interface and `destination_ip` as one approved service address. These commands inspect state without sending application traffic:

~~~bash
ip -brief address show dev "$vpn_if"
ip route get "$destination_ip"
~~~

**Illustrative:** interface `tun2` has `10.8.0.2/24`, while a pushed route covers `10.9.0.0/24`. The interface subnet is not the destination scope. A route lookup selecting `tun2` and the expected source address supports the local path choice, not remote reachability. A route selecting Ethernet or another tunnel suggests a missing/overlapping route or policy mismatch. Check applicable `ip rule`/route tables and the actual source/namespace before altering anything.

Compare the selected route with the profile and server-pushed routes. `redirect-gateway` can change the default path. `route-nopull` rejects pushed routes and DNS-related options but still allows interface configuration; it is not a read-only mode and can explain missing reachability when deliberately used.

If the numeric address works in a separately authorised service check but the hostname does not, inspect resolver results and profile DNS integration. A pushed DNS option need not update the Linux resolver without the relevant integration. Preserve the service hostname for TLS/SNI and HTTP routing; changing `/etc/hosts` or using an IP URL can conceal the actual issue.

Use the intended protocol/port for the final service observation. ICMP silence does not establish TCP failure. Report a route error, authentication rejection, reconnect loop or application denial at its own layer; do not describe an unavailable service as a failed VPN solely because no response arrived.

References: [OpenVPN route options](https://openvpn.net/community-docs/community-articles/openvpn-2-6-manual.html), [route lookup semantics](https://man7.org/linux/man-pages/man8/ip-route.8.html).
