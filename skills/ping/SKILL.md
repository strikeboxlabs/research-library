---
name: ping
description: Use Linux iputils ping for a bounded ICMP echo check to one selected peer. Use when reply counts, deadlines or a missing echo response are confused with application reachability.
---

# Check one selected echo path

Read this entire SKILL.md before acting. Require the permitted numeric peer and intended network namespace. Confirm iputils with `ping -V`; Windows/BusyBox options differ. No conditional resources are required. Finish with counts, timing, status and scope.

Define `peer` as the selected IPv4 address:

~~~bash
ping -4 -n -c 3 -w 5 "$peer"
status=$?
~~~

The count bounds requests; the deadline also bounds waiting. Retain the final summary. With both options, status1 can mean fewer than three replies by the deadline; status2 is an error. Inspect diagnostics separately.

Replies support this ICMP exchange at this time, not HTTP/SSH availability. No reply can reflect filtering, routing or loss rather than a down host. A request observed at the peer does not prove its reply reached the sender. Read address/direction/sequence when correlating a capture. Select the actual interface/namespace instead of assuming a VPN name.

Reference: [iputils ping manual](https://manpages.debian.org/bookworm/iputils-ping/ping.8.en.html).
