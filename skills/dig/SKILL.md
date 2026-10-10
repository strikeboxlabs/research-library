---
name: dig
description: Query an explicit DNS server and distinguish authoritative answers, cached views, negative responses and application name resolution. Use when checking a selected record or explaining why a DNS change has not affected a client.
---

# Verify the answer from the intended server

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

Dig queries DNS directly. Applications using NSS can instead obtain a name from `/etc/hosts` or another configured source; `getent ahosts "$fqdn"` examines that local lookup path, although applications can use their own resolver. Repeat observations from the consuming namespace. A forward A record neither proves reverse lookup results nor establishes a service's hostname-trust authentication decision.

See [BIND's dig reference](https://bind9.readthedocs.io/en/latest/manpages.html#dig-dns-lookup-utility), [negative-answer semantics](https://www.rfc-editor.org/rfc/rfc2308) and [getent/NSS behavior](https://man7.org/linux/man-pages/man1/getent.1.html).
