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

Documentation reviewed 2026-10-09; Linux execution untested. Case: AdmirerToo pp. 11–12. Source: [upstream tcpdump manual](https://github.com/the-tcpdump-group/tcpdump/blob/master/tcpdump.1.in).
