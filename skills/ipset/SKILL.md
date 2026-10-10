---
name: ipset
description: Inspect Linux kernel IP sets and test a selected member with ipset. Use when ban-list exports, set types, expiring entries or firewall references make an address's effective policy unclear.
---

# IP-set evidence behind a firewall list

Read this entire SKILL.md before acting; reuse complete current context. Use the intended network namespace and sufficient existing permissions, select the observed set/type, and preserve status plus membership evidence. Finish with that set's state at the observation time; membership alone does not establish packet blocking.

~~~bash
ipset version
ipset list -name
~~~

Choose `set_name` from the actual names and define `snapshot` as a fresh private file:

~~~bash
umask 077
ipset list "$set_name"
ipset save "$set_name" >"$snapshot"
~~~

Read the type/family/header and complete members. `save` emits restore syntax; recording it does not restore or change a set. A permission, namespace or unsupported-type error is not an empty set. Do not infer that a name containing fail2ban identifies every ban source.

Define `entry` in the selected type's syntax: an address for hash:ip, an address/network for hash:net, or the required tuple for composite types. Retain the diagnostic and immediate status:

~~~bash
ipset test "$set_name" "$entry"
result=$?
printf 'ipset-test-status=%s\n' "$result"
~~~

Zero indicates a match; nonzero needs the diagnostic to distinguish no match from an operation error. A list:set tests member set names, not recursively an IP address. Inspect network prefixes, exceptions and family rather than grepping an exact IPv4 string.

A fixed `grep -A 7` block and loose dotted-number regex can omit later members, IPv6, CIDRs or tuple context. Take an actual set snapshot. Timeout entries can expire during comparison, and header counts can lag expiry cleanup. Avoid optional name resolution for numeric evidence.

Correlate the selected set with the actual firewall rule, chain order, packet direction and namespace. A generated banned.txt may be stale or incomplete; an unlisted address may still be blocked elsewhere. Keep set membership, web export and observed traffic separate.

Reference: [upstream ipset manual](https://ipset.netfilter.org/ipset.man.html).
