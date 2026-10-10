---
name: iptables
description: Inspect Linux packet-filter rules with explicit backend, table, chain and address family. Use when rule order, counters, namespace context or a firewall command's mutation effects obscure a connectivity diagnosis.
---

# Identify the ruleset being inspected

Read this entire SKILL.md before acting. Identify the backend, family, namespace and packet path before listing rules; use the actual ports and state of the flow when interpreting them. Finish with applicable ordered rules/counters and any unverified configuration or traffic assumptions.

Check `iptables --version` and the actual selected executable. The version identifies `legacy` versus `nf_tables`; these are different kernel interfaces. Do not switch alternatives to make a listing look familiar. `iptables` covers IPv4, while `ip6tables` covers IPv6. Commands inspect the current network namespace, which may differ between host and container.

With the existing firewall-administration rights, define `table` and `chain` from the relevant packet path, for example `filter` and `INPUT` for traffic delivered locally:

~~~bash
iptables -w 5 -t "$table" -S "$chain"
iptables -w 5 -t "$table" -L "$chain" -n -v -x --line-numbers
~~~

`-S` preserves rule specifications and chain policies. The numeric verbose listing exposes interfaces and exact counters without name resolution. Filter is only the default table; it is not the whole firewall. Forwarded packets use a different path from local INPUT/OUTPUT, and NAT/other hooks can affect the result. Correlate with the actual flow and other applicable rulesets.

Rules are order-sensitive. An appended ACCEPT may never be reached after an earlier terminating rule; a built-in policy applies when traversal reaches the end. Counters describe matching traffic, not necessarily application success. Do not combine listing with `-Z`: that resets counters and destroys the observation baseline. Rule numbers can change between observations and should not become stale deletion targets.

An acquired `rules.v4` is saved configuration, not proof of the currently installed rules. Read state and port predicates together: an OUTPUT rule matching TCP `--sport 80` tests the source port, not a request's destination port. An earlier `ESTABLISHED,RELATED` accept may permit replies despite a DROP policy. Describe the specific flow and chain traversal rather than concluding that every outbound packet is blocked.

A missing callback or listener event alone does not identify a firewall drop. Check the application's attempted operation, endpoint/address family, route and applicable rule counters; lack of execution or another network failure can produce the same absence. See [state and TCP match definitions](https://man7.org/linux/man-pages/man8/iptables-extensions.8.html).

`-C chain rule-specification` checks for a matching installed rule without adding it. Its nonzero status can mean absence or an operational error; inspect stderr. A matching rule does not prove the complete flow is accepted. `-A`, `-I`, `-D`, `-F` and `-P` change live policy; a comment-bearing example still changes the firewall. Plan an exact before/after change and recovery path before a requested mutation, especially over the connection it could interrupt.

`-w 5` bounds the legacy xtables lock wait; it does not retry application traffic or make a multi-command workflow atomic. The nft backend handles updates differently and documents this wait option as a no-op. Permission, lock, missing-extension and wrong-backend errors require different fixes; flushing rules is not a diagnostic repair.

Consult backend-specific behavior in the [iptables manual](https://man7.org/linux/man-pages/man8/iptables.8.html), [nft versus legacy](https://man7.org/linux/man-pages/man8/xtables-nft.8.html).
