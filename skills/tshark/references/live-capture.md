# Bounded network observation

Use the environment's established capture permissions. Define `iface` as the actual capture-point interface, `peer` as the selected endpoint visible there, `port` as its decimal TCP port and `pcap` as a fresh private file. List available interfaces if needed:

~~~bash
tshark -D
umask 077
tshark -n -i "$iface" -f "host $peer and tcp port $port" -a duration:15 -w "$pcap"
~~~

This observes that flow for fifteen seconds; adapt the window to the requested event. Start before the event and retain termination status, stderr and capture statistics. `-f` is a capture filter, while `-Y` filters dissected display output. A capture can contain sensitive application bytes; keep the file private.

Return to the entrypoint's `-r` analysis before interpreting the conversation. Missing traffic can reflect timing, interface/namespace or the filter. A successful open of an interface does not prove complete capture; packet drops, truncated frames and a late start limit conclusions. A group name alone does not establish usable dumpcap permissions. No matching application reply is separate from no packets or capture failure.

See the [TShark manual](https://www.wireshark.org/docs/man-pages/tshark.html) for capture-filter and autostop options.
