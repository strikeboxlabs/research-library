---
name: iw
description: Inspect Linux wireless interface roles, PHY grouping and the current client association with iw. Use when local interface addresses, peer BSSIDs, P2P devices or shared radios are being confused.
---

# Identify the existing wireless interface

Read this entire SKILL.md before acting. Require the selected Linux network namespace, installed iw and a driver exposing nl80211 information. This task reads existing state; no conditional resources are required. Finish with interface/PHY/type and association evidence, preserving missing-device or unsupported-operation diagnostics.

~~~bash
iw help
iw dev
~~~

Record each named interface, its ifindex/wdev, local address, type and PHY group. Multiple interfaces under one PHY share that wireless device; they are not necessarily separate physical cards. A PHY can also be supplied by a simulated driver. An unnamed/non-netdev P2P-device entry is separate from a neighboring named managed interface, even under the same PHY.

`AP`, `managed` and `monitor` identify different roles. Managed mode alone does not establish association; monitor mode alone does not prove a working capture. A displayed local interface address is not automatically the peer AP's BSSID. Preserve the actual channel/frequency where reported rather than inferring it from an IP subnet or interface name.

For the selected managed interface, define `interface` from the listing:

~~~bash
iw dev "$interface" link
~~~

Read the reported peer, SSID, frequency and connection state. `Not connected` describes this interface at this observation time. A successful association does not establish DHCP, routes, DNS or application connectivity. Missing fields and permission/driver errors leave the requested fact unresolved; do not fix inspection by changing the interface type, channel or service state. Correlate the selected interface with the existing network manager's status when configuration and observed state disagree.

References: [iw help and link observations](https://wireless.docs.kernel.org/en/latest/en/users/documentation/iw.html), [interface query mapping](https://wireless.docs.kernel.org/en/latest/en/users/documentation/iw/replace-iwconfig.html).
