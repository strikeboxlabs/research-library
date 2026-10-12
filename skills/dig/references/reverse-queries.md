# Query the selected reverse records

Require the intended DNS server and an exact address, or a small explicit list from the owned network inventory. Define `dns_server` as its numeric endpoint and `address` as the selected IPv4/IPv6 literal:

~~~bash
dig -r @"$dns_server" -x "$address" +time=2 +tries=1 +noall +comments +answer +authority +stats
status=$?
~~~

`-x` constructs the reverse name and selects IN PTR: reversed octets under in-addr.arpa for IPv4, nibble format under ip6.arpa for IPv6. Retain response status and responding server. Zero process status can accompany NXDOMAIN; empty answer-only output cannot distinguish absent records from a failed query.

For the approved small list, define a Bash array `addresses` containing only those exact literals:

~~~bash
for address in "${addresses[@]}"; do
  printf 'Address=%s\n' "$address"
  dig -r @"$dns_server" -x "$address" +time=2 +tries=1 +noall +comments +answer +authority +stats
  printf 'dig_status=%s\n' "$?"
done
~~~

Retain each result; the loop's final status is not every query's status. A PTR publishes a name for that address. It does not establish a live host, service, identity trust or matching forward A/AAAA. Query the returned name separately when forward/reverse agreement is required, preserving the same resolver view.

Reference: [BIND dig reverse lookup](https://bind9.readthedocs.io/en/latest/manpages.html#dig-dns-lookup-utility).
