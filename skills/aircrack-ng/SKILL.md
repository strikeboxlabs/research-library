---
name: aircrack-ng
description: Inspect network and handshake metadata in an existing authorized WPA/WPA2 capture with Aircrack-ng. Use when ESSID, BSSID, packet counts or a reported handshake are confused with a recovered credential or completed authentication.
---

# Review saved wireless capture inventory

Read this entire SKILL.md before acting. Require a selected authorized local capture and trusted installed binary; this task inventories saved WPA/WPA2 evidence without a dictionary or radio action. Finish with capture identity, read count, observed network/handshake labels and diagnostic limits. No conditional resources are required.

Define `aircrack_bin` as the installed executable and `capture` as an existing absolute capture path. Inspect help/build identification before choosing the mode:

~~~bash
"$aircrack_bin" --help
"$aircrack_bin" -a 2 "$capture"
~~~

`-a 2` selects WPA/WPA2 mode rather than the default WEP attack mode. Keep dictionary/key-output options absent. Retain the initial network table and read diagnostics; stop after inventory if this build prompts for further action. A missing-dictionary diagnostic is expected when proceeding beyond WPA inventory without candidates, not a reason to add a wordlist for this task. The program's final nonzero status must be retained separately from a successfully displayed table.

**Illustrative:** `Read 6498 packets` and one row labeled `WPA (1 handshake)` identify this analyzer's parsed network and available handshake candidate, not all traffic ever transmitted or a proven successful login. BSSID identifies the selected access point address; ESSID is a network name, not its password or a username. Keep both associated with the original capture; same-name networks can have different BSSIDs.

Inspect packet-level context with an already available capture analyzer when completeness matters. Handshake detection does not imply every four-way packet is present, that the capture is authentic, or that a displayed key-recovery claim applies to another network/service. File-header, malformed/truncated capture and missing network errors are analysis gaps. Wildcards or multiple inputs merge evidence; use only the selected file for this inventory.

An existing `KEY FOUND` transcript is a separate offline candidate result, not current wireless association or SSH authentication. Preserve its actual BSSID/ESSID, input/run coverage and provenance without replaying it. This skill does not create captures, disconnect clients, inject radio traffic or provide password-recovery procedures.

See [upstream mode/input definitions and handshake limits](https://www.aircrack-ng.org/doku.php?id=aircrack-ng).
