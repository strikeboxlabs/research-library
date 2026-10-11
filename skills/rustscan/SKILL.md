---
name: rustscan
description: Discover TCP ports quickly with RustScan and hand selected results to Nmap. Use when choosing scan scope, controlling concurrency or investigating missing ports and failed service follow-up.
---

# Discover ports, then identify services

Read this entire file before acting. For Nmap handoff or incomplete results, also read [scan decisions](references/scan-decisions.md). Finish with the addresses/port range actually tested, discovered ports and follow-up evidence; an empty result is not proof that no service exists.

`rustscan` is not available on the worker PATH. Treat that as a missing prerequisite for the commands below; do not plan a RustScan-first workflow or install it implicitly. For an authorized TCP discovery task, the installed `/usr/bin/nmap` is an alternative, with its own scope and completion evidence.

RustScan is useful independently of another scanner skill. Its default scripting stage can invoke Nmap, so choose discovery-only or service follow-up explicitly. Check `rustscan --help` for the installed flags and `rustscan --version` for the build; newer upstream options are not present in every packaged release.

Set `target` to one authorized IP and `ports` to a comma-separated numeric list. Start with deliberate scope and moderate concurrency:

~~~bash
rustscan --no-config -a "$target" -p "$ports" -b 100 -t 3000 --tries 2 -g
~~~

`-g` suppresses the Nmap stage. `-b` controls concurrent socket work, while `-t` is a connection timeout in milliseconds. Neither is a requests-per-second guarantee. `--no-config` avoids inherited scan/script settings. If all TCP ports are in scope, replace `-p "$ports"` with `-r 1-65535`; do not silently widen a selected-port request.

An **illustrative** `192.0.2.10 -> [22,80,443]` records successful connections from this scanner's vantage point. It does not identify SSH or HTTP versions. Preserve stderr and the chosen scope alongside results. Treat DNS resolution failures, socket exhaustion and interrupted runs as incomplete coverage.

Use the [upstream options](https://github.com/bee-san/RustScan/blob/master/src/input.rs) and [usage guide](https://github.com/bee-san/RustScan/wiki/Usage) for build differences.
