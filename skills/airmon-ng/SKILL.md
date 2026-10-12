---
name: airmon-ng
description: Create and remove a monitor interface on an owned dedicated wireless radio for passive diagnostics, while tracking managed-interface restoration.
---

# Manage a diagnostic monitor interface

Read this entire SKILL.md before acting. Require a dedicated owned radio, supported driver, permitted channel and privilege to change its mode. No conditional resources are required. Finish with the actual interface names, diagnostics and restored interface state.

Use a radio that does not carry the management session. Inventory interfaces and potentially competing processes:

~~~bash
airmon-ng
airmon-ng check
~~~

Resolve ownership of that radio before changing it; a listed process is not proof it interferes. Avoid blanket `check kill`, which can stop unrelated networking. Define `interface` and `channel` from the owned configuration:

~~~bash
airmon-ng start "$interface" "$channel"
~~~

Read the reported monitor name and any managed-interface change. Do not construct a name by appending `mon`. If creation fails, resolve driver, rfkill or channel restrictions before capture.

After the owned capture process exits, set `monitor` to its observed interface:

~~~bash
airmon-ng stop "$monitor"
airmon-ng
~~~

Verify the intended managed interface and restore any network-manager state changed for this task; removing monitor mode does not prove reconnection.

Reference: [airmon-ng](https://www.aircrack-ng.org/doku.php?id=airmon-ng).
