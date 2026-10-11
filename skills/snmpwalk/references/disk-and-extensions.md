# Correlate disk rows and monitoring output

Require the owned agent, established access view and known connection options. Use existing deployment v3 settings when required. For the UCD-SNMP disk task, use the entrypoint's agent/community variables and a bounded subtree:

~~~bash
snmpwalk -v2c -c "$community" -t 2 -r 1 -On "$agent" .1.3.6.1.4.1.2021.9
status=$?
~~~

Preserve OID, type and row index. dskPath is the reported mount path; dskDevice identifies its partition device. Match them by index, not neighboring lines. Monitoring configuration and access views limit the table; missing rows do not prove missing mounts. A device-mapper path does not by itself establish LVM, and a path under a conventional web directory does not establish the selected virtual host's document root or HTTP accessibility.

For a known monitoring extension, inspect its acquired configuration/output before issuing a query. NET-SNMP-EXTEND-MIB rows are indexed by their name token. Retain command, arguments, execution/run type and cache time with the output/result fields. The usual enterprise root can be relocated by configuration; do not treat a numeric example as universal.

An output-related read of a run-on-read entry can invoke its configured program when the cached result is stale. Treat that as execution with the agent's service identity and actual program effects, even though the request is an SNMP GET. A run-on-set entry behaves differently; reading its configuration is not a request to execute it. Use an existing approved exact output instance for routine monitoring, with the entrypoint's selected-instance query, only when those effects are part of the task. Do not walk an entire extension branch as a supposedly passive inventory.

Report returned output, result status, cache/context and capture time separately. A script's text declaring a database healthy is not independent database verification, and cached output is not necessarily current process state. A service's Unix identity and SELinux domain are distinct; an output string is not proof of unrestricted host privileges. Retain sensitive arguments privately. Missing config, denied view or snipped output leaves that specific conclusion unresolved.

References: [disk MIB definitions](https://github.com/net-snmp/net-snmp/blob/master/mibs/UCD-SNMP-MIB.txt), [extension execution and cache definitions](https://github.com/net-snmp/net-snmp/blob/master/mibs/NET-SNMP-EXTEND-MIB.txt), [agent monitoring configuration](https://www.net-snmp.org/docs/man/snmpd.conf.html).
