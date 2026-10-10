---
name: tcpdump
description: Capture and interpret a narrowly scoped network observation with tcpdump on Linux. Use to verify packet arrival, preserve a pcap and distinguish no observed traffic from an application failure.
---

# Capture a specific network observation

Define the question first: for example, did IPv4 ICMP from a selected lab host reach this machine during a known action? Identify the relevant interface using route information and `tcpdump -D`; do not assume a VPN is always `tun0`. Check `tcpdump --version` and capture permissions.

Define `iface` as that interface, `peer` as the numeric IPv4 host, and `pcap` as a fresh path writable by the capture process. Run with the host's established capture privileges:

~~~bash
umask 077
tcpdump -i "$iface" -nn -c 20 -w "$pcap" "host $peer and icmp"
~~~

`-c 20` stops after 20 matching packets; it is **not a time limit**. Start the capture before the event and stop it with Ctrl-C after the agreed observation window if the count is not reached. Wait for termination so the file and capture statistics are complete.

Read it separately without live capture privileges:

~~~bash
tcpdump -nn -r "$pcap" "host $peer and icmp"
~~~

`-w` saves packet data, whereas ordinary stdout is a decoded text summary. `-nn` keeps addresses and ports numeric. Change the filter to the protocol in question; this example excludes IPv6 ICMP and TCP. Quote compound filters so the shell does not interpret parentheses/operators.

Record timestamps, directions, interface/filter and capture/drop counts. An echo request establishes packet arrival; it does not prove every preceding step claimed by a walkthrough. No matching packets can reflect the wrong interface, namespace, timing, filter, route or upstream loss. It does not independently prove that a remote command failed. Similarly, a TCP handshake establishes transport reachability, not application success.

Permission errors are not empty captures. If privilege dropping prevents writing the file, check the configured capture user and directory rather than broadening directory permissions. Keep captures private, and check reported truncation/drops before relying on payload completeness.

## Preserve a selected container-side TCP conversation

Choose the interface and endpoint **as seen at the capture point**. Docker's default bridge is often `docker0`; user-defined networks, host networking and other namespaces can take different paths. A host publication such as port 8002 can correspond to container port 443 on the bridge, so a filter copied from the browser URL can miss the traffic.

Define `iface` as the verified interface, `peer` as the selected numeric endpoint, `port` as its observed TCP port and `pcap` as a fresh private path. Capture under the established privileges, starting before the relevant handshake:

~~~bash
umask 077
tcpdump -i "$iface" -nn -s 0 -w "$pcap" "host $peer and tcp port $port"
~~~

Stop with Ctrl-C at the agreed deadline and retain the final drop statistics. `-s 0` selects the implementation's large default snapshot length; it is not unlimited storage or a duration bound. This capture includes both directions for the selected host/port. Check packet lengths and gaps before handing it to a TLS analyzer. More `-v` flags do not decrypt TLS or add missing bytes to a saved packet.

File capabilities can permit capture without sudo, but neither their presence nor an interface named docker0 proves that every container flow is visible. If the handshake is absent, preserve that limitation instead of inferring that the server key or application password is wrong.

See the [tcpdump manual](https://github.com/the-tcpdump-group/tcpdump/blob/master/tcpdump.1.in) and [Docker bridge behavior](https://docs.docker.com/engine/network/drivers/bridge/).
