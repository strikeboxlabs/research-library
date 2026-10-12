---
name: iwlist
description: Inspect wireless-tools scan results on one Linux interface. Use to distinguish cached AP advertisements from a fresh scan, association or negotiated security.
---

# Inspect wireless scan observations

Read this entire SKILL.md before acting. Require the selected interface, a Wireless Extensions capable driver and permission for any requested active scan. No conditional resources are required. Finish with interface, observation time, scan mode and limitations.

Define `interface` as the owned interface. Read cached results first:

~~~bash
iwlist --version
iwlist "$interface" scanning last
~~~

`last` retrieves previous results without initiating scanning. Their age and completeness may be unknown. When a fresh scan is required for the approved wireless diagnostic:

~~~bash
iwlist "$interface" scanning
~~~

Triggering a scan normally requires privilege and may transmit probes. Driver support determines available results; permission, busy-device or unsupported-operation errors are not evidence that no AP exists.

Record each relevant BSSID, SSID, channel/frequency and advertised security information. Advertisements do not prove current association, a completed authentication exchange or a security weakness. A BSSID is the advertised peer address, not the local interface MAC. Inspect the existing connection status separately. Legacy field availability varies; preserve unknown values rather than inferring them.

Reference: [wireless-tools iwlist manual](https://manpages.debian.org/bookworm/wireless-tools/iwlist.8.en.html).
