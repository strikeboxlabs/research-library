---
name: nmap
description: Discover services on scoped Linux or Windows lab hosts with Nmap and follow up on selected ports. Use when TCP versus UDP coverage, IPv6, host discovery or uncertain port states need interpretation.
---

# Nmap service discovery

Read this entire SKILL.md before acting; complete current context need not be re-read. Select the scoped host, protocol and useful port range before probing. For an unexpected option-denial message, follow the wrapper attribution below before interpreting upstream behavior. Retain scan completion, vantage and confirmed versus uncertain services; a skipped or interrupted scan is incomplete evidence.

Installed invocation: `/usr/bin/nmap`, version `7.99`. `/usr/bin/masscan` version `1.3.2` is also present; `rustscan` is not available on the worker PATH. Tool availability does not establish equivalent probe behavior or completeness across a VPN.

For scoped subnet discovery from a container/internal namespace or a transferred static binary, read [network vantage and host discovery](references/network-vantage.md) fully first.

Separate port discovery from service interrogation. Define `target` as one in-scope host/IP and `discovery` as a fresh output prefix in an existing directory. Record `/usr/bin/nmap --version`.

~~~bash
/usr/bin/nmap -sT -p- --reason -oA "$discovery" "$target"
~~~

This checks TCP ports 1–65535 using connect scans, including without raw-socket privileges. It does not scan UDP. Use a narrower port range when sufficient. If host discovery skips a host independently known to be reachable, retry that host with `-Pn`; this bypasses discovery, not filtering. Avoid copying a fixed `--min-rate` from a walkthrough: forcing probes too quickly can reduce accuracy on a lossy path.

On a high-latency path (a ~100 ms RTT VPN, for example), a full-range connect scan can spend tens of minutes in retransmit backoff when nonresponsive ports drop silently. Track elapsed time against covered ports and treat a crawling scan as incomplete evidence, not as absence of services. A threaded userspace connect sweeper (one socket per port with an explicit timeout) is a legitimate coverage fallback, but it must record the error class per port: reporting only "open" silently merges filtered (timeout) into closed (refused). Separately, `masscan` run over such a tunnel can report zero open ports for a host with known services — its raw SYN packets are not traversing the tunnel. A zero-result masscan is unverified evidence; the connect() path that `nmap -sT` uses is the source of truth.


Without a port-selection option, a normal TCP scan checks the 1,000 most common ports. `-A` adds OS/version detection, default scripts and traceroute; it does not select all ports. Report "one open port among those tested", not "the host has only one open port", when reading such a scan.

When a quick common-port result is useful, retain it separately from any broader scan requested for coverage. If both scans run concurrently, keep their combined traffic within the approved budget and report completion independently. A port omitted from the quick selection has not been tested by that scan; neither a running full-range scan nor a timing estimate establishes completed coverage.

Read the saved results before continuing. Define `ports` as the nonempty, comma-separated TCP ports actually found open, and `services` as a new output prefix:

~~~bash
/usr/bin/nmap -sT -sV -p "$ports" --reason -oA "$services" "$target"
~~~

For automation, parse the XML by host, protocol and `state="open"`; do not derive a mixed TCP/UDP list from human output or scan all hosts using one merged list. An interrupted XML file may be incomplete. Keep the discovery evidence as well as follow-up results.

| Observation | Meaning and next decision |
|---|---|
| `open` | A listener responded. Confirm its protocol; the port-number service label alone is a guess. |
| `closed` | A response indicates no listener at this vantage/time. |
| `filtered` or `open\|filtered` | Reachability/state remains uncertain. Check route and filtering; do not report the service absent. |
| Product, domain or hostname detected | Use as a lead for protocol-specific checks. A banner/certificate does not prove an exact OS build or vulnerability. |

After an IPsec connection changes reachability, compare the same target and selected ports from the intended source/namespace. `-sT` uses the operating system's `connect()` path, whereas raw-packet probes can behave differently. A TCP-only IPsec selector excludes ICMP and UDP, so failed ping is not a TCP service result. Where reachability is independently established, `-Pn -sT` avoids a mismatched discovery probe. Confirm negotiated selectors and application responses; neither a VPN status line nor new open ports means the firewall was disabled.

NSE scripts are separate probes. Inspect relevant scripts with `--script-help` and choose them deliberately. `-sC` runs the default script set; it is not a passive version lookup, and default scripts are not all nonintrusive.

For an unexpected option-denial message, establish the executable/wrapper actually selected and read its complete accessible source as text. A custom wrapper's message is not evidence that upstream Nmap lacks that option. Track its argument handling, downstream executable and checked status separately; a scan banner can come from the child. A substring check over joined arguments is not a complete argument grammar. Preserve the exact denied operation and wrapper identity without retrying through a different executable to evade the restriction. An aborted child is an incomplete scan and does not prove that no earlier script/helper effect occurred.

For a service expected on UDP, select the observed port with `-sU` and the required raw-socket privileges; retain `-sU` on follow-up version probes. Dropping it silently changes the scan back to TCP. UDP silence commonly yields `open|filtered`; service-specific evidence is needed to resolve that uncertainty. Do not run a whole UDP range merely because TCP found little.

An observed IPv6 address is a separate target: use `-6` and record the exact address/interface scope. IPv4 results do not establish IPv6 exposure or filtering. A name can resolve to several addresses; check which address Nmap actually tested before generalizing to the host.

Finish with the host, vantage, tested protocols/ranges, completed scan status and confirmed versus inferred services.

Sources: [connect path](https://nmap.org/book/scan-methods-connect-scan.html), [scan techniques](https://nmap.org/book/man-port-scanning-techniques.html), [states](https://nmap.org/book/man-port-scanning-basics.html), [output](https://nmap.org/book/man-output.html), [discovery](https://nmap.org/book/man-host-discovery.html), [NSE](https://nmap.org/book/man-nse.html), [port selection](https://nmap.org/book/man-port-specification.html), [IPv6 and -A](https://nmap.org/book/man-misc-options.html).
