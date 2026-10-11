# Interpret the running-software table

Use for an owned agent's running-software inventory with known SNMP access parameters. Require the selected agent/view and preserve numeric OIDs/types. A short system-only response can reflect a restricted view rather than the absence of other software.

Define `agent`, `community` and a fresh private `names` output as in the entrypoint. For known v2c access, query only the name column:

~~~bash
umask 077
snmpwalk -v2c -c "$community" -t 2 -r 1 -On "$agent" .1.3.6.1.2.1.25.4.2.1.2 >"$names"
~~~

Use the established v3 configuration instead when that is the deployment's contract. Inspect status/errors and complete rows. For one observed integer `index`, inspect its corresponding name and path, without assuming output order:

~~~bash
snmpget -v2c -c "$community" -t 2 -r 1 -On "$agent" \
  ".1.3.6.1.2.1.25.4.2.1.2.$index" \
  ".1.3.6.1.2.1.25.4.2.1.4.$index"
~~~

These HOST-RESOURCES-MIB columns describe the software name and location from which it loaded. The index is intended to use native identification where possible, but is not a universal PID guarantee. Rows can change between separate requests; disappearance or reused indices require a fresh correlated observation. A filename does not identify its publisher, effective account or security status.

An acquired parameter-column row, ending in .5 followed by the software index, describes startup parameters rather than a protocol-defined password or live OS identity. Such captures can expose private arguments; retain them privately and report redacted evidence. Do not infer a valid application credential, replay it or assume a later shell has the same token from a matching string.

When two established read contexts differ, compare the same selected OIDs and actual agent/view configuration. A timeout, inaccessible object and empty value are separate outcomes. Do not brute-force a community to resolve incomplete inventory or perform a write probe as a supposed read check. Finish with returned rows, capture time/context and visibility limits.

See the [HOST-RESOURCES-MIB running-software definitions](https://datatracker.ietf.org/doc/html/rfc2790#section-5).
