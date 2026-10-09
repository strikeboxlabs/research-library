---
name: iptables-save
description: Capture an iptables ruleset with understood backend, family, counters and output-file effects. Use when saving firewall evidence or reviewing a restore without confusing serialization, persistence and live policy changes.
---

# Save rules as firewall data

Identify the matching backend and address family before capture. `iptables-save` and `ip6tables-save` cover IPv4 and IPv6 respectively; legacy and nft variants query different interfaces. Record the selected executable, namespace and time. A host capture does not inventory every container, and an iptables-format dump is not proof that all native nftables objects or other network controls were captured.

Define `save_bin` as the verified save executable and `snapshot` as a new absolute file in a private task directory. With the required existing administration rights:

~~~bash
(umask 077; set -C; "$save_bin" -c > "$snapshot")
~~~

The no-clobber subshell refuses an existing output. Check status and stderr immediately; a failed command can still leave an empty/partial file. `-c` includes packet/byte counters without zeroing them. Retain the complete table sections and COMMIT records; do not treat one visible rule as a complete snapshot.

The tool normally writes stdout; `-f filename` makes the program open an output file using its execution privileges. It does not read that file or restore rules. Shell redirection is instead performed by the invoking shell. Keep both mechanisms confined to intended evidence files: Backfire's privileged save into `authorized_keys` demonstrates a file-writing capability, not ordinary firewall persistence. Comments are user-controlled rule text; serialized output must not be reused as trusted input to an unrelated configuration format.

Without `-t`, the reviewed manual describes all available tables and no module loading. Selecting `-t table` limits coverage and may load that table's kernel module. Preserve those capture conditions. A snapshot does not make rules survive reboot; persistence depends on the system's separate service/configuration mechanism.

For a requested restore review, use the matching restore binary's supported `--test` mode to parse/construct without committing. It is not proof that applying the rules will preserve connectivity. A real restore normally flushes the affected tables; even `--noflush` can rebuild declared user chains. Account for intervening policy changes and retain an independent recovery path before applying anything. Do not call restore merely to validate that saving worked.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Backfire p. 13. Sources: [save](https://man7.org/linux/man-pages/man8/iptables-save.8.html), [restore and test mode](https://man7.org/linux/man-pages/man8/iptables-restore.8.html), [backend distinctions](https://man7.org/linux/man-pages/man8/xtables-nft.8.html).
