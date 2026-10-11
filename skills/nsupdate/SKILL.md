---
name: nsupdate
description: Add one fresh owned DNS A record with an existing TSIG key and remove exactly that record using conditional dynamic updates. Use to verify an approved change against the selected authoritative server and distinguish record TTL from zone aging.
---

# Make one conditional owned DNS change

Read this entire SKILL.md before acting. Require installed nsupdate/dig, the selected primary server and zone, an existing protected TSIG key permitted for this name, and an approved fresh test name/address/TTL. Read the rollback section before applying a temporary change. Finish with update status, authoritative verification, resolver limits and any cleanup still required.

Check `nsupdate -V` and installed help. Define `dns_server` as the primary's numeric address, `zone` and `fqdn` as exact names with trailing dots, `address` as the approved IPv4 address, `ttl` as positive seconds and `tsig_key` as the existing private key file. Validate these as single DNS input tokens, without whitespace/newlines; select a fresh owned test name rather than an application's service name. Define `change_file` as a fresh file in an owned private directory.

~~~bash
umask 077
printf 'server %s 53\nzone %s\nprereq nxdomain %s\nupdate add %s %s IN A %s\nsend\nanswer\n' \
  "$dns_server" "$zone" "$fqdn" "$fqdn" "$ttl" "$address" > "$change_file"
~~~

Review the generated transaction before sending it. `nxdomain` requires the name to have no records of any type; the server checks this with the update, avoiding a query/write race. `-v` selects TCP, with a bounded timeout; it does not select TLS. TSIG authenticates the update, not confidentiality. Keep the key out of argv/logs; do not replace `-k` with an inline secret.

~~~bash
nsupdate -v -t 10 -k "$tsig_key" "$change_file"
~~~

Preserve status and returned answer. `REFUSED`, signature errors or failed prerequisites leave a failed change; a timeout can leave an uncertain outcome. Query before retrying:

~~~bash
dig -r @"$dns_server" "$fqdn" A +norecurse +time=2 +tries=1 +noall +comments +answer +authority +stats
~~~

Verify the intended server, authoritative `aa` response and exact A data. Then compare the consuming resolver when needed. Dig's zero exit alone does not prove a positive answer. TTL controls caching; it is not a timer that deletes the authoritative record. Zone aging/no-refresh/refresh periods and scavenging schedules are separate server policy.

## Remove the temporary record

Only remove the exact owned record once the requested observation is complete. Define `rollback_file` as another fresh private file:

~~~bash
printf 'server %s 53\nzone %s\nprereq yxrrset %s IN A %s\nupdate delete %s IN A %s\nsend\nanswer\n' \
  "$dns_server" "$zone" "$fqdn" "$address" "$fqdn" "$address" > "$rollback_file"
nsupdate -v -t 10 -k "$tsig_key" "$rollback_file"
~~~

The prerequisite requires the whole A RRset to match that one address; changed/multiple A data therefore aborts cleanup for review. The deletion names exact type/data, preserving unrelated records. Repeat the authoritative query and retain status: no A answer, NXDOMAIN and a timeout are different outcomes. Record unresolved cleanup rather than widening the deletion.

See [BIND nsupdate](https://bind9.readthedocs.io/en/latest/manpages.html#nsupdate-dynamic-dns-update-utility) and [conditional DNS update model](https://www.rfc-editor.org/rfc/rfc2136).
