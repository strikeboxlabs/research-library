---
name: snmp-check
description: Collect read-only SNMP metadata from one owned device using its provisioned community. Use when a human-readable system report, protocol-version selection or a partial/empty enumeration needs interpretation.
---

# Read an owned device's SNMP metadata

Read this entire SKILL.md before acting. Require one known owned device, permission for the enumerated metadata, its established read-only community and the intended management route. Complete with version, response fields, diagnostics and coverage limits. Missing access or a timeout leaves the report unresolved.

Check `snmp-check -h` and `-i`; historical `snmpcheck` variants have different target/timeout syntax. For the v1.9 interface, define `device_ip`, `snmp_port`, `community` and `report` as verified inputs and a fresh private output:

~~~bash
umask 077
snmp-check -v 1 -p "$snmp_port" -c "$community" -t 5 -r 1 -d "$device_ip" > "$report"
report_status=$?
~~~

Select `-v 2c` only for an established v2c service. This interface does not provide SNMPv3 authentication/privacy. Community values appear in arguments and the report; use the intended private management environment. Do not rely on the default `public` as an access test or enable `-w`, which tests write access.

`-d` omits TCP-connection enumeration, not every network/system section. The tool can collect process, user, route and interface information; it is broader than one scalar query. Inspect actual returned sections and errors. Hostname, contact and location are configured assertions, not verified identity/location; agent uptime differs from system uptime. An empty section does not prove absence when MIB support or access views are restricted. A port-number label or UDP silence does not resolve service state.

References: [Matteo Cantoni's snmpcheck](https://www.nothink.org/codes/snmpcheck/), [packaged v1.9 interface](https://www.kali.org/tools/snmpcheck/).
