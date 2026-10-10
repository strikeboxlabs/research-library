# Match hardware inventory to its table row

Define `agent` as the scoped endpoint and `community` as the known v2c credential; use the deployment's existing v3 options where required. Community values and responses are exposed by v2c. For a device inventory question, the ENTITY-MIB physical table is `.1.3.6.1.2.1.47.1.1.1`; its serial-number **column** is `.1.3.6.1.2.1.47.1.1.1.1.11`. A particular serial needs the row index after that column. Using the same known `agent`/`community`, retain numeric OIDs and types:

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


Source: [ENTITY-MIB definitions](https://www.rfc-editor.org/rfc/rfc6933.html).
