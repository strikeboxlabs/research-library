---
name: iptables-save
description: Capture an iptables ruleset and interpret chain order, owner matches, backend and counters. Use when firewall evidence or a restore review depends on packet origin, output-file effects or incomplete coverage.
---

# Save rules as firewall data

Read this entire SKILL.md before acting; reuse complete current context. Require the matching installed backend/family, intended namespace and existing capture rights. Save the complete ruleset before interpreting its chain order and local owner context; the restore review below is conditional on a requested restore. Finish with capture status, complete table evidence and coverage limits, rather than a claim that serializing rules changed or proved connectivity.

Identify the matching backend and address family before capture. `iptables-save` and `ip6tables-save` cover IPv4 and IPv6 respectively; legacy and nft variants query different interfaces. Record the selected executable, namespace and time. A host capture does not inventory every container, and an iptables-format dump is not proof that all native nftables objects or other network controls were captured.

Define `save_bin` as the verified save executable and `snapshot` as a new absolute file in a private task directory. With the required existing administration rights:

~~~bash
(umask 077; set -C; "$save_bin" -c > "$snapshot")
~~~

The no-clobber subshell refuses an existing output. Check status and stderr immediately; a failed command can still leave an empty/partial file. `-c` includes packet/byte counters without zeroing them. Retain the complete table sections and COMMIT records; do not treat one visible rule as a complete snapshot.

The tool normally writes stdout; `-f filename` makes the program open an output file using its execution privileges. It does not read that file or restore rules. Shell redirection is instead performed by the invoking shell. Keep both mechanisms confined to intended evidence files: Backfire's privileged save into `authorized_keys` demonstrates a file-writing capability, not ordinary firewall persistence. Comments are user-controlled rule text; serialized output must not be reused as trusted input to an unrelated configuration format.

For an egress question, evaluate the whole relevant chain in order, including earlier terminal ACCEPT/DROP decisions, jumps/returns, protocol/port/state conditions and the final chain policy. An earlier allowed-port rule can settle a packet before a later owner-based drop; one drop line is not a blanket subnet prohibition. `-m owner --uid-owner` matches local socket ownership in OUTPUT/POSTROUTING, not the remote user's directory identity or arbitrary forwarded packets. Preserve negation (`!`) and the generating namespace/backend. A ruleset can explain a possible policy path but does not prove route, DNS, peer service or packet traversal; use existing connection/counter evidence to distinguish those gaps.

Without `-t`, the reviewed manual describes all available tables and no module loading. Selecting `-t table` limits coverage and may load that table's kernel module. Preserve those capture conditions. A snapshot does not make rules survive reboot; persistence depends on the system's separate service/configuration mechanism.

For a requested restore review, use the matching restore binary's supported `--test` mode to parse/construct without committing. It is not proof that applying the rules will preserve connectivity. A real restore normally flushes the affected tables; even `--noflush` can rebuild declared user chains. Account for intervening policy changes and retain an independent recovery path before applying anything. Do not call restore merely to validate that saving worked.

Sources: [save](https://man7.org/linux/man-pages/man8/iptables-save.8.html), [restore and test mode](https://man7.org/linux/man-pages/man8/iptables-restore.8.html), [backend distinctions](https://man7.org/linux/man-pages/man8/xtables-nft.8.html) and [owner match](https://manpages.debian.org/bookworm/iptables/iptables-extensions.8.en.html#owner).
