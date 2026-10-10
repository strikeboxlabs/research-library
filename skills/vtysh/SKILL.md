---
name: vtysh
description: Diagnose local FRR or Quagga BGP sessions, prefix selection and advertisement policy through vtysh. Use when a best path, connected route or no-export community is being mistaken for actual forwarding or remote acceptance.
---

# Follow a prefix from BGP to forwarding

Use the existing router/container context and authorized daemon-socket access. `vtysh --help` identifies supported CLI options; `show version` identifies the routing suite. FRR and older Quagga share the executable name but differ in commands, configuration paths and defaults. A socket/permission failure is incomplete access, not an empty routing table.

## Establish the session and address family

For current FRR, gather separate snapshots:

~~~bash
VTYSH_PAGER=cat vtysh -c 'show version'
VTYSH_PAGER=cat vtysh -d bgpd -c 'show bgp ipv4 unicast summary'
~~~

`-c` runs a VTY command and exits; `-d bgpd` queries that daemon only. `VTYSH_PAGER=cat` prevents an interactive pager from holding the collector. Retain stderr and exit status; `-n` suppresses command-error status and is unsuitable for reliable collection. `-u` is not a secure read-only privilege boundary.

On legacy Quagga use `show ip bgp summary` and `show ip bgp PREFIX`; avoid abbreviated walkthrough commands such as `sh ... summ` in scripts. On FRR specify `ipv4 unicast` deliberately, and the appropriate VRF when this is not the default instance. At an interactive VTY prompt, `show bgp ?` reveals the installed grammar. Shell quotes are not part of a command typed at that prompt.

A numeric `State/PfxRcd` is a prefix count for an established session; zero does not mean the session is down. `Idle`, `Connect` or `Active` is a session state, not a count. If FRR displays `(Policy)`, inspect its required inbound/outbound policy before concluding the peer sent no routes. Record neighbor AS, uptime and queue counters alongside the prefix evidence.

## Separate best path, selected route and kernel lookup

Set `prefix` to the exact observed IPv4 CIDR and `destination` to the affected IPv4 host. These are address inputs, not arbitrary VTY text:

~~~bash
VTYSH_PAGER=cat vtysh -d bgpd -c "show bgp ipv4 unicast $prefix"
VTYSH_PAGER=cat vtysh -d zebra -c "show ip route $destination"
ip -4 route get "$destination"
~~~

The first result compares BGP paths for one prefix. Read next hop, AS path, local preference, origin, validity and best-path marker together. A shorter AS path alone need not win: earlier policy criteria can decide. BGP selection does not measure the fastest application connection.

Zebra's route view compares protocol candidates and their installation state. Its `>`/`*` legend is different from the BGP table's validity/best markers; use the legend printed by that command. A BGP best path can be missing from forwarding because of next-hop resolution, a competing protocol, installation failure or a different VRF/table. The final `ip` lookup must run in the same network namespace and with the relevant source/policy context; it checks a local routing decision, not connectivity.

**Illustrative decision:** the BGP table has a best route for `192.0.2.0/24`, yet the destination lookup follows an installed `192.0.2.0/25`. For addresses in that half, longest-prefix matching chooses the /25 within the selected table. These are different prefixes, not competing BGP paths for the same /24. Inspect the /25's origin and installation instead of tuning /24 path metrics.

## Explain advertisement without changing it

Define `peer` as a known neighbor address. Current FRR can narrow outbound evidence to the selected prefix:

~~~bash
VTYSH_PAGER=cat vtysh -d bgpd -c "show bgp ipv4 unicast neighbors $peer advertised-routes $prefix"
VTYSH_PAGER=cat vtysh -c 'show running-config'
~~~

Check local help for the prefix filter on older builds. Keep configuration output private: it can include authentication material. Inspect the relevant address family, `network`/redistribution statements, outbound route-map attachment and referenced prefix lists. An interface address can create a connected route; BGP advertisement additionally depends on configured origination/redistribution and export policy. Sharing a host or running a routing daemon does not imply automatic advertisement.

The outbound view establishes what this router reports advertising; remote acceptance and installation require the peer's evidence. A configured route-map is intent, not proof of either. `no-export` restricts propagation beyond the receiving AS/confederation boundary; it permits internal propagation. `no-advertise` has the stronger all-peers restriction. Inspect received communities and onward advertisements when verifying containment.

If observations revert periodically, correlate timestamps with daemon uptime, service logs and the actual scheduler/configuration source. Running state and saved files can diverge; newer FRR uses integrated configuration while old Quagga deployments may use per-daemon files. Re-query after a reset rather than combining observations across it. Configuration mode, `clear ...`, `write`, `-b` and service restarts change state and are outside this diagnostic procedure.

References: [VTY options](https://github.com/FRRouting/frr/blob/master/doc/manpages/vtysh.rst), [FRR BGP commands](https://docs.frrouting.org/en/latest/bgp.html), [Zebra route interpretation](https://docs.frrouting.org/en/latest/zebra.html), [legacy Quagga commands](https://github.com/Quagga/quagga/blob/master/doc/bgpd.texi), [community scope](https://www.rfc-editor.org/rfc/rfc1997.html).
