---
name: snmpwalk
description: Query bounded SNMP subtrees and individual OIDs with Net-SNMP. Use when default walk coverage, timeouts, hardware inventory, numeric OIDs or BITS/hex output lead to incorrect conclusions.
---

# Net-SNMP query interpretation

Check `snmpwalk --version` and local help. Establish the agent, SNMP version, known credentials and intended subtree; do not assume a default community. The example uses v2c, which exposes community/data on the network and the `-c` value to process inspection. Use the deployment's existing v3 authentication/privacy configuration when required.

Define `agent` as the scoped endpoint, `community` as the known v2c value, `subtree` as a numeric OID, and `output` as a private file:

~~~bash
umask 077
snmpwalk -v2c -c "$community" -t 2 -r 1 -On "$agent" "$subtree" >"$output"
~~~

`-t` is the per-request timeout and `-r` the retry count, not an overall walk deadline. Choose a small subtree before walking a large device. Without an OID, the default walk covers MIB-2; vendor objects under `.1.3.6.1.4.1` are outside that default. Select the relevant enterprise branch from device evidence rather than treating a short default walk as complete coverage.

For one known instance, use `snmpget` with the same connection options and its exact OID. Scalars commonly require `.0`; tables require their actual index. `-On` prints numeric OIDs and avoids confusing local MIB naming with server capabilities. Preserve the OID and reported type alongside values.

Timeout can mean filtering, credentials, version or reachability; it does not identify which. `No Such Object/Instance` and the end of a subtree are different from a transport failure. An access-limited SNMP view can hide otherwise existing objects.

Decode output according to its type. Net-SNMP's normal `BITS` rendering includes hex bytes **followed by set-bit numbers/names**. Concatenating all whitespace-separated tokens corrupts the value. Re-query the selected OID with `-Oqv` when appropriate; the reviewed BITS formatter then emits quoted hex without the bit annotations. Check the actual output before decoding. `-Ox` controls string rendering and does not universally override BITS formatting or MIB display hints. Not every octet value represents text.

## Match hardware inventory to its table row

For a device inventory question, the ENTITY-MIB physical table is `.1.3.6.1.2.1.47.1.1.1`; its serial-number **column** is `.1.3.6.1.2.1.47.1.1.1.1.11`. A particular serial needs the row index after that column. Using the same known `agent`/`community`, retain numeric OIDs and types:

~~~bash
snmpwalk -v2c -c "$community" -t 2 -r 1 -On "$agent" .1.3.6.1.2.1.47.1.1.1.1.11
~~~

**Illustrative:** `.1.3.6.1.2.1.47.1.1.1.1.11.7 = STRING: "LAB-SERIAL-7"` identifies row 7, not necessarily the chassis. Define `index` as that observed integer, then query associated fields:

~~~bash
snmpget -v2c -c "$community" -t 2 -r 1 -On "$agent" \
  ".1.3.6.1.2.1.47.1.1.1.1.2.$index" \
  ".1.3.6.1.2.1.47.1.1.1.1.4.$index" \
  ".1.3.6.1.2.1.47.1.1.1.1.5.$index" \
  ".1.3.6.1.2.1.47.1.1.1.1.7.$index"
~~~

These are description, containing-entity index, physical class and name. Join columns by index, not output order; the first serial may belong to a module. A zero-length serial is permitted when unknown or inapplicable. Missing/denied inventory does not prove that the device lacks a serial. Preserve the exact value; stripping vendor prefixes or interpreting inventory as an application credential requires separate product evidence.

References: [walk coverage](https://www.net-snmp.org/docs/man/snmpwalk.html), [Net-SNMP options](https://www.net-snmp.org/docs/man/snmpcmd.html), [ENTITY-MIB definitions](https://www.rfc-editor.org/rfc/rfc6933.html), [BITS formatter](https://github.com/net-snmp/net-snmp/blob/master/snmplib/mib.c).
