---
name: dnstool
description: Query, add and remove a selected AD-integrated DNS A record with krbrelayx dnstool from Linux. Use to distinguish LDAP bind, DNS-node permissions, stored changes and actual DNS resolution.
---


# Work on one AD DNS record

Read this entire SKILL.md before acting. Require the selected zone/record, known identity, DC and intended change/restore state. Finish with LDAP result and DNS read-back; a successful bind or group name alone is insufficient.

This is `dnstool.py` from dirkjanm's krbrelayx, not an unrelated DNS utility. Define `script` as its reviewed local path and inspect `python3 "$script" -h`. The script uses LDAP to manage AD DNS nodes; `--tcp` selects TCP for its DNS queries, not a different LDAP security policy.

Define `dc` as the selected directory server, `identity` as `DOMAIN\account`, and `record` as the exact FQDN. Query before changing:

~~~bash
python3 "$script" -u "$identity" -r "$record" -a query "$dc" --tcp
~~~

The reviewed CLI prompts for an omitted password. Inspect the actual zone, node DN, type, values and tombstone state. A missing node and an unreadable partition are different outcomes. `--forest` and `--legacy` select other AD DNS partitions; `--zone` chooses a different zone. Do not cycle partitions or create similarly named nodes to hide an unknown scope.

For an approved new A record, define `record_ip` as its intended IPv4 address:

~~~bash
python3 "$script" -u "$identity" -r "$record" -a add -t A -d "$record_ip" "$dc" --tcp
~~~

Confirm it was absent or that adding a value to the existing node is intended. The normal refusal on an existing A record protects that distinction; `--allow-multiple` changes the operation. `insufficientAccessRights` after `Bind OK` means this object operation was denied for this principal, not that all identities cannot create DNS records. Group membership is a lead for checking effective node/container permissions, not a successful write.

Re-run the query and perform a DNS query against the actual server/vantage used by the client. LDAP persistence can precede DNS service visibility, replication or cache expiry. Keep a missing resolution separate from failed LDAP mutation.

For removal of the owned A value, retain the exact original/new values and use:

~~~bash
python3 "$script" -u "$identity" -r "$record" -a remove -t A -d "$record_ip" "$dc" --tcp
~~~

The reviewed implementation deletes a matching value when several exist; for the last value it tombstones the node. `ldapdelete` deletes the node instead, and `resurrect` is another change. Do not substitute a hard delete for owned-value cleanup or erase unrelated records. Query the node and resolver again; old client caches can outlive the write. See [upstream CLI and record handling](https://github.com/dirkjanm/krbrelayx/blob/master/dnstool.py).
