---
name: tcpdump
description: Capture and interpret a narrowly scoped network observation with tcpdump on Linux. Use to verify packet arrival, preserve a pcap and distinguish no observed traffic from an application failure.
---

# Capture a specific network observation

Read this entire SKILL.md before acting. Select the capture point, protocol/filter and observation window, confirm capture and output-file prerequisites, then inspect the saved capture and termination statistics. For container-side TCP, use the conditional section below before selecting the endpoint/filter. Finish with the observed packets and capture limits; a permission failure or missing traffic is not application-failure proof.

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

`-w` saves packet data, whereas ordinary stdout is a decoded text summary. Adding `-v` to a live `-w` capture provides capture-count reporting, not the usual per-packet decode; inspect the completed savefile with `-r`. `-nn` keeps addresses and ports numeric. Change the filter to the protocol in question; this example excludes IPv6 ICMP and TCP. Quote compound filters so the shell does not interpret parentheses/operators.

For a selected local service, `lo` is the loopback interface in the capture process's network namespace. It is not synonymous with every packet addressed to this machine or every container's localhost. Verify that the requested conversation actually traverses it. An observed port number alone does not identify the application or establish whether transport encryption was negotiated.

Record timestamps, directions, interface/filter and capture/drop counts. An echo request establishes packet arrival; it does not prove every preceding step claimed by a walkthrough. No matching packets can reflect the wrong interface, namespace, timing, filter, route or upstream loss. It does not independently prove that a remote command failed. Similarly, a TCP handshake establishes transport reachability, not application success.

Permission errors are not empty captures. If privilege dropping prevents writing the file, check the configured capture user and directory rather than broadening directory permissions. Keep captures private, and check reported truncation/drops before relying on payload completeness.

When mandatory access control is active, correlate the error with the matching timestamp/PID and policy record. An AppArmor `DENIED` record for `operation="exec"` identifies a blocked helper execution; it is distinct from denial of capture-file creation or packet access. Capture counts can therefore coexist with a failed later helper. Preserve the profile name, requested/denied operation and process/file identity; a profile file on disk alone does not prove the effective loaded policy. Resolve the failed operation rather than reporting an empty capture or successful post-processing. See the [AppArmor documentation](https://ubuntu.com/server/docs/how-to/security/apparmor/) for policy/log interpretation.

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
