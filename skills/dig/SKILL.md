---
name: dig
description: Query an explicit DNS server, inspect PTR/TXT records or an approved zone transfer. Use to distinguish authoritative records, forward/reverse resolver views, negative responses, published SPF text and transfer completeness.
---

# Verify the answer from the intended server

Read this entire SKILL.md before acting; reuse complete current context. Select a record/resolver comparison, TXT inspection or the approved zone-transfer task below. For one reverse lookup or a small approved address list, read [PTR queries](references/reverse-queries.md) fully first. Required inputs are the intended server and exact name/zone/address, installed dig, network access and the server's permitted authentication context. Finish with the responding server, actual records/status and view or transfer limits; missing access or incomplete output remains a gap.

Check `dig -v`. Define `dns_server` as the authorized server's numeric address and `fqdn` as the exact fully qualified name with a trailing dot. For a server expected to be authoritative:

~~~bash
dig -r @"$dns_server" "$fqdn" A +norecurse +time=2 +tries=1 +noall +comments +answer +authority +stats
~~~

`-r` skips `.digrc`. Keep the header and server information: `+short` alone hides reasons for an empty answer. Confirm the responding server, status, `aa` flag and requested name/type. An **illustrative** `service.lab.example. 60 IN A 192.0.2.40` establishes that answer from this server at this time. `aa` indicates an authoritative answer; merely clearing recursion does not make a server authoritative.

| Observation | Next decision |
|---|---|
| Expected answer | Compare the application's actual resolver view before declaring the change effective there. |
| `NXDOMAIN` | Name error; follow any CNAME chain to identify the absent name. Dig still exits zero for a received response. |
| `NOERROR`, no requested records | Inspect CNAMEs and authority data. A negative type answer and an NS referral are different; blank output is insufficient. |
| `SERVFAIL`, `REFUSED` or timeout | Preserve the status; investigate server policy, processing or transport rather than treating it as an absent record. |

Define `resolver` as the application's actual recursive DNS server and repeat the same query with recursion requested:

~~~bash
dig -r @"$resolver" "$fqdn" A +recurse +time=2 +tries=1 +noall +comments +answer +authority +stats
~~~

Differences can reflect cached positive/negative answers or different DNS views. One displayed TTL is not proof that every cache has expired. Query AAAA separately when relevant; an A change does not replace an IPv6 answer.

TTL controls caching, not authoritative record deletion. AD DNS aging and scavenging use separate server policy: no-refresh plus refresh intervals identify possible staleness, not an exact removal deadline. A scavenging start/end event does not identify which particular record was removed; retain record-specific evidence before assigning that cause to NXDOMAIN.

Dig queries DNS directly. Applications using NSS can instead obtain a name from `/etc/hosts` or another configured source; `getent ahosts "$fqdn"` examines that local lookup path, although applications can use their own resolver. Repeat observations from the consuming namespace. A forward A record neither proves reverse lookup results nor establishes a service's hostname-trust authentication decision.

## Inspect published TXT records

For the defined application `resolver` and exact `fqdn`, request TXT explicitly:

~~~bash
dig -r @"$resolver" "$fqdn" TXT +recurse +time=2 +tries=1 +noall +comments +answer +authority +stats
~~~

Apply the same status/server/negative-answer decisions above. Quoted chunks on one TXT record concatenate without inserted spaces; separate answer records remain separate. Retain owner/type and the entire selected record rather than searching raw stdout for a substring. A published `v=spf1` record is SPF policy data, not proof that a particular sender is authorized: SPF evaluates an SMTP identity and client IP against that policy, including DNS-dependent mechanisms and errors. A contact form's substring test is not that evaluation or an email-delivery result. See [SPF records and evaluation](https://www.rfc-editor.org/rfc/rfc7208).

## Inspect an approved zone transfer

For a zone you administer and a client permitted by its transfer policy, define `zone` as the exact zone name and `dns_server` as the selected authoritative server:

~~~bash
dig -r @"$dns_server" "$zone" AXFR +time=5 +noonesoa
~~~

If policy requires an already provisioned TSIG key, add `-k "$tsig_key"` with its protected local file path. AXFR uses TCP. Preserve transfer errors and the opening/closing matching SOA records plus server/transfer summary; a partial list is not a complete zone. `REFUSED` is a policy result, not proof the zone is absent. Returned DNS names and addresses do not establish configured HTTP virtual hosts or reachable services. Keep any exported zone inventory private. See [AXFR completeness](https://www.rfc-editor.org/rfc/rfc5936).

See [BIND's dig reference](https://bind9.readthedocs.io/en/latest/manpages.html#dig-dns-lookup-utility), [negative-answer semantics](https://www.rfc-editor.org/rfc/rfc2308) and [getent/NSS behavior](https://man7.org/linux/man-pages/man1/getent.1.html).
