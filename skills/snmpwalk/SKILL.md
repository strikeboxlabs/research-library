---
name: snmpwalk
description: Query bounded SNMP subtrees and individual OIDs with Net-SNMP. Use when disk, process, hardware or IPv6 inventory, extension execution, default coverage, timeouts or typed output need careful interpretation.
---

# Net-SNMP query interpretation

Read this entire SKILL.md before acting; current complete context need not be re-read. Use the known connection parameters and a bounded OID scope, preserving types, indices and failures. For hardware inventory or serial-to-component mapping, read [hardware inventory](references/hardware-inventory.md) fully first. For selected disk rows or an existing monitoring extension, read [disk and extension evidence](references/disk-and-extensions.md) fully first; reading extension output can execute its configured program. Finish with the observed values and access/coverage limits, not inferred credentials or missing-device claims.

For IPv6 address-table observations, read [IPv6 address indices](references/ipv6-address-indices.md) fully before querying/decoding. Its selected-row procedure requires the package-local [decoder](scripts/decode_ipv6_index.py), Python 3 and exactly 16 acquired address octets.

Check `snmpwalk --version` and local help. Establish the agent, SNMP version, known credentials and intended subtree; do not assume a default community. The example uses v2c, which exposes community/data on the network and the `-c` value to process inspection. Use the deployment's existing v3 authentication/privacy configuration when required.

For HOST-RESOURCES-MIB running-software inventory or differences between known access views, read [process inventory](references/process-inventory.md) fully before its queries. It distinguishes software indices, startup metadata and current process evidence.

Define `agent` as the scoped endpoint, `community` as the known v2c value, `subtree` as a numeric OID, and `output` as a private file:

~~~bash
umask 077
snmpwalk -v2c -c "$community" -t 2 -r 1 -On "$agent" "$subtree" >"$output"
~~~

`-t` is the per-request timeout and `-r` the retry count, not an overall walk deadline. Choose a small subtree before walking a large device. Without an OID, the default walk covers MIB-2; vendor objects under `.1.3.6.1.4.1` are outside that default. Select the relevant enterprise branch from device evidence rather than treating a short default walk as complete coverage.

For one known instance, use `snmpget` with the same connection options and its exact OID. Scalars commonly require `.0`; tables require their actual index. `-On` prints numeric OIDs and avoids confusing local MIB naming with server capabilities. Preserve the OID and reported type alongside values.

To inspect a system contact note, query the exact `sysContact.0` instance with the known connection parameters:

~~~bash
snmpget -v2c -c "$community" -t 2 -r 1 -On "$agent" .1.3.6.1.2.1.1.4.0
~~~

This is administratively supplied contact text. A label such as "VPN password" is source content, not a protocol-defined secret field or proof that the value still authenticates. Preserve its OID/type and redact any sensitive value in the report. A 32-character hex string alone cannot identify a hash algorithm; use application/configuration evidence before selecting a decoder or recovery task.

Timeout can mean filtering, credentials, version or reachability; it does not identify which. `No Such Object/Instance` and the end of a subtree are different from a transport failure. An access-limited SNMP view can hide otherwise existing objects.

Decode output according to its type. Net-SNMP's normal `BITS` rendering includes hex bytes **followed by set-bit numbers/names**. Concatenating all whitespace-separated tokens corrupts the value. Re-query the selected OID with `-Oqv` when appropriate; the reviewed BITS formatter then emits quoted hex without the bit annotations. Check the actual output before decoding. `-Ox` controls string rendering and does not universally override BITS formatting or MIB display hints. Not every octet value represents text.


References: [walk coverage](https://www.net-snmp.org/docs/man/snmpwalk.html), [Net-SNMP options](https://www.net-snmp.org/docs/man/snmpcmd.html), [system MIB definitions](https://www.rfc-editor.org/rfc/rfc3418.html), [BITS formatter](https://github.com/net-snmp/net-snmp/blob/master/snmplib/mib.c).
