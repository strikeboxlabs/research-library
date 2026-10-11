---
name: zenmap
description: Open saved Nmap results in the Zenmap GUI and inspect the actual scan command and coverage. Use when a profile name, selected Ports/Hosts rows or a historical GUI screenshot is mistaken for complete scan evidence.
---

# Inspect an existing scan in Zenmap

Read this entire SKILL.md before acting. Require a trusted existing Zenmap installation, graphical session and selected saved Nmap XML or Zenmap results file. Finish with original scan command, host/state observations, completion and display limits. No conditional resources are required.

Define `zenmap_bin` as the installed executable and `results` as the existing absolute results path:

~~~bash
"$zenmap_bin" --help
"$zenmap_bin" -f "$results"
~~~

`-f` opens results for viewing. It does not request a new scan. Avoid scan-launch options for this saved-file task: `-n` supplies a command to execute, and combining target/profile options can automatically start scanning. An absent GUI or unsupported file is a prerequisite/format gap; do not convert review into a new network scan to recover missing evidence.

Inspect Nmap Output and the saved command alongside Ports/Hosts. A profile title such as **illustrative** “Intense scan, all TCP ports” is a configuration label; inspect the actual command and results for port range, transport, discovery, timing, scripts and version detection. An all-TCP-port label establishes no UDP coverage. Loaded/merged scans can have different commands and times; keep each original run separate.

Selected rows omit other output and errors. `filtered` means the scanner could not determine open/closed at that vantage, not a service conclusively stopped. A second SSH port does not by itself establish Docker or another isolation mechanism. Banner strings, inferred service labels and confirmed version evidence differ. Retain Nmap version, target resolution, start/end, final host/port summary and relevant errors from the original run before claiming completeness.

A successful GUI import establishes file readability, not current reachability, target ownership or a successful worker outcome. Keep the original results unchanged; screenshot crops are presentation evidence and do not substitute for scan XML/output. See [Zenmap file versus scan-launch options](https://nmap.org/book/zenmap-command-line.html) and [interpreting Nmap port states](https://nmap.org/book/man-port-scanning-basics.html).
