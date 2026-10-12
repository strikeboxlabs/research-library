---
name: iwconfig
description: Read legacy Wireless Extensions interface status with iwconfig. Use to distinguish operating mode, AP association and driver-dependent signal statistics without changing wireless configuration.
---

# Read the selected wireless status

Read this entire SKILL.md before acting. Require installed wireless-tools and the intended Linux namespace/interface. No conditional resources are required. Finish with observed mode/association and display limitations; missing Wireless Extensions support is not proof that the machine has no wireless device.

~~~bash
iwconfig --version
iwconfig
~~~

Define `interface` as the observed selected name. A name without setting operands queries it:

~~~bash
iwconfig "$interface"
~~~

Master denotes the AP role; Managed denotes a client role; Monitor denotes monitoring mode. A Managed interface may still be Not-Associated. Read its Access Point field separately from its own link-layer address and the ESSID network name. An IP address alone establishes none of these wireless roles.

Link Quality, Signal level and error counters depend on the driver. Preserve units and observation time; do not convert a quality fraction directly into a percentage of throughput or infer a persistent fault from one cumulative counter. A displayed bitrate is not measured application throughput.

Wireless Extensions are legacy. Unsupported or absent fields require the driver's supported status mechanism, often nl80211 through iw; changing modes or setting keys is not a remedy for a missing display. Keep any key-bearing output private.

References: [wireless-tools display and mode semantics](https://manpages.debian.org/bookworm/wireless-tools/iwconfig.8.en.html), [Linux wireless query alternatives](https://wireless.docs.kernel.org/en/latest/en/users/documentation/iw/replace-iwconfig.html).
