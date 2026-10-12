---
name: airodump-ng
description: Observe an owned access point and save a bounded passive wireless diagnostic capture with explicit BSSID, channel and output paths.
---

# Observe an owned wireless access point

Read this entire SKILL.md before acting. Require an owned monitor interface, known approved BSSID/channel and private output directory. No conditional resources are required. Finish with the observation interval, actual files and capture limitations.

Define `monitor`, `bssid`, `channel` and a fresh absolute `prefix` inside that directory. Confirm local options, then capture without inducing client activity:

~~~bash
airodump-ng --help
airodump-ng --bssid "$bssid" --channel "$channel" --write "$prefix" --output-format pcap,csv "$monitor"
~~~

End with Ctrl-C at the agreed time. Record the actual generated filenames; numbered suffixes change across runs. Keep captures private.

Use BSSID alongside ESSID: several radios can advertise the same name. Advertised authentication/cipher fields do not establish successful authentication, usable credentials or complete client visibility. Missing traffic may reflect reception, channel, driver or observation-time limits. Resolve a channel mismatch instead of suppressing its warning. Channel hopping can miss exchanges; `--band abg` does not promise every modern band.

Restore the owned monitor interface separately after the capture exits. Report retained frame evidence, not a claim that the entire network was observed.

Reference: [airodump-ng options and fields](https://www.aircrack-ng.org/doku.php?id=airodump-ng).
