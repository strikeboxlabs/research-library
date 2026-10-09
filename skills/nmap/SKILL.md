---
name: nmap
description: Discover services on scoped Linux or Windows lab hosts with Nmap and follow up on selected ports. Use when TCP versus UDP coverage, IPv6, host discovery or uncertain port states need interpretation.
---

# Nmap service discovery

Separate port discovery from service interrogation. Define `target` as one in-scope host/IP and `discovery` as a fresh output prefix in an existing directory. Record `nmap --version`.

~~~bash
nmap -sT -p- --reason -oA "$discovery" "$target"
~~~

This checks TCP ports 1–65535 using connect scans, including without raw-socket privileges. It does not scan UDP. Use a narrower port range when sufficient. If host discovery skips a host independently known to be reachable, retry that host with `-Pn`; this bypasses discovery, not filtering. Avoid copying a fixed `--min-rate` from a walkthrough: forcing probes too quickly can reduce accuracy on a lossy path.

Without a port-selection option, a normal TCP scan checks the 1,000 most common ports. `-A` adds OS/version detection, default scripts and traceroute; it does not select all ports. Report "one open port among those tested", not "the host has only one open port", when reading such a scan.

Read the saved results before continuing. Define `ports` as the nonempty, comma-separated TCP ports actually found open, and `services` as a new output prefix:

~~~bash
nmap -sT -sV -p "$ports" --reason -oA "$services" "$target"
~~~

For automation, parse the XML by host, protocol and `state="open"`; do not derive a mixed TCP/UDP list from human output or scan all hosts using one merged list. An interrupted XML file may be incomplete. Keep the discovery evidence as well as follow-up results.

| Observation | Meaning and next decision |
|---|---|
| `open` | A listener responded. Confirm its protocol; the port-number service label alone is a guess. |
| `closed` | A response indicates no listener at this vantage/time. |
| `filtered` or `open\|filtered` | Reachability/state remains uncertain. Check route and filtering; do not report the service absent. |
| Product, domain or hostname detected | Use as a lead for protocol-specific checks. A banner/certificate does not prove an exact OS build or vulnerability. |

NSE scripts are separate probes. Inspect relevant scripts with `--script-help` and choose them deliberately. `-sC` runs the default script set; it is not a passive version lookup, and default scripts are not all nonintrusive.

For a service expected on UDP, select the observed port with `-sU` and the required raw-socket privileges; retain `-sU` on follow-up version probes. Dropping it silently changes the scan back to TCP. UDP silence commonly yields `open|filtered`; service-specific evidence is needed to resolve that uncertainty. Do not run a whole UDP range merely because TCP found little.

An observed IPv6 address is a separate target: use `-6` and record the exact address/interface scope. IPv4 results do not establish IPv6 exposure or filtering. A name can resolve to several addresses; check which address Nmap actually tested before generalizing to the host.

Finish with the host, vantage, tested protocols/ranges, completed scan status and confirmed versus inferred services.

Documentation reviewed 2026-10-09; Linux execution untested. The first five writeups informed this sequence; Aero/Agile p. 2, Antique pp. 3–4 and APT pp. 5–6 clarified coverage. Sources: [scan techniques](https://nmap.org/book/man-port-scanning-techniques.html), [states](https://nmap.org/book/man-port-scanning-basics.html), [output](https://nmap.org/book/man-output.html), [discovery](https://nmap.org/book/man-host-discovery.html), [NSE](https://nmap.org/book/man-nse.html), [port selection](https://nmap.org/book/man-port-specification.html), [IPv6 and -A](https://nmap.org/book/man-misc-options.html).
