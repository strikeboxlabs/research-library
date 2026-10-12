---
name: arp
description: Read the Linux net-tools IPv4 neighbor cache for one interface. Use when cached MAC mappings, incomplete entries or presumed gateway identities need careful interpretation.
---

# Read existing IPv4 neighbor mappings

Read this entire SKILL.md before acting. Require Linux net-tools arp and the intended network namespace/interface. No conditional resources are required. Finish with the observed mappings and their limits; this task does not populate or modify the cache.

Define `interface` as the selected observed name:

~~~bash
arp -n -a -i "$interface"
~~~

`-n` avoids name lookups, `-a` selects BSD-style display and `-i` limits entries to this interface. Keep address, hardware address, interface and incomplete-entry state together. An incomplete entry has no resolved hardware mapping at that moment.

The cache reflects existing local neighbor state, not a complete inventory or proof of current reachability. A mapping does not establish that the peer is a router, DHCP server or authenticated device. Confirm the configured next hop from the actual route when that role matters. This IPv4 cache does not describe IPv6 neighbor discovery. Do not use set/delete operations to remedy an unexplained read-only observation.

Reference: [net-tools arp manual](https://manpages.debian.org/bookworm/net-tools/arp.8.en.html).
