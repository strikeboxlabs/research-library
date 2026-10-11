---
name: enyx
description: Retrieve IPv6 address-index observations from one known SNMP agent with the legacy Enyx wrapper. Use when its padded hexadecimal output is useful, while checking parser failures and inaccurate address-class labels against raw SNMP evidence.
---

# Interpret the legacy SNMP IPv6 wrapper

Read this entire SKILL.md before acting. Require an already reviewed installed Enyx script, its Python 2 interpreter, `/usr/bin/snmpwalk`, one approved numeric IPv4 agent and known SNMP v1/v2c read access. Complete with raw-query status, returned addresses and actual coverage limits; wrapper labels or no-output messages are insufficient.

Define `enyx_script` and `python2_bin` as verified installed absolute paths. The reviewed upstream script is Python 2, not a Python 3 module; a skill does not install that interpreter or port the tool. It checks a hardcoded snmpwalk path and invokes a shell pipeline. Restrict `version` to `1` or `2c`, `agent` to one validated numeric IPv4 address and `community` to a known value containing only ASCII letters, digits, underscore, dot or hyphen. Quoting the outer invocation does not make shell-interpolated input safe inside the script. If access requires v3 or incompatible secret syntax, this wrapper does not meet the prerequisite; use an appropriate direct SNMP client.

~~~bash
"$python2_bin" "$enyx_script" "$version" "$community" "$agent"
~~~

This reads the IPv6 address-index branch; it does not test IPv6 service reachability. Community values are exposed in argv and unencrypted on the network. The wrapper has no timeout/retry controls or reliable propagated snmpwalk status, so retain stderr and verify ambiguous results with a bounded numeric-OID query:

~~~bash
snmpwalk -v "$version" -c "$community" -t 2 -r 1 -On "$agent" .1.3.6.1.2.1.4.34.1.3.2.16
~~~

Preserve the 16 address octets from the OID index and the returned interface index separately. The wrapper's fixed field offsets depend on output formatting. It incorrectly treats exactly one result as no IPv6 address, labels all addresses starting `0000` as loopback and labels other non-`fe80` addresses Unique-Local. Check actual `::1`, `fe80::/10` and `fc00::/7` membership. A lab's `dead:beef` prefix is not Unique-Local. Missing/inaccessible rows and transport failures remain unknown inventory.

Attribution and implementation: [Enyx by Thanasis Tserpelis, Trickster0](https://github.com/trickster0/Enyx). See [IP address table indices](https://www.rfc-editor.org/rfc/rfc4293) and [Unique Local addressing](https://www.rfc-editor.org/rfc/rfc4193).
