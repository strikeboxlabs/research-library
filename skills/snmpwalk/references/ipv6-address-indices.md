# Read IPv6 addresses from the IP-MIB index

Require one approved agent, known SNMP read context and installed Net-SNMP. Use existing v3 authentication/privacy when required. For a known legacy v1/v2c view, define `version` as its actual `1` or `2c`, `agent` and `community` as established values and `output` as a fresh private file:

~~~bash
umask 077
snmpwalk -v "$version" -c "$community" -t 2 -r 1 -On "$agent" .1.3.6.1.2.1.4.34.1.3 > "$output"
~~~

Preserve status/stderr and complete numeric OIDs/types. This `ipAddressIfIndex` column has its address in the **OID index**; the returned integer identifies the associated interface. The suffix contains address type, length and address octets. For ordinary IPv6, the suffix starts `2.16` followed by exactly 16 decimal bytes. IPv4 (`1.4`) and zone-index-bearing address types require different parsing; do not silently trim them to 16 bytes. The remote interface index is not automatically a client's local scope/interface identifier.

For one acquired ordinary-IPv6 row, isolate only those 16 bytes into `octets`, excluding the OID prefix, `2.16` and returned INTEGER. The required supplied helper is [scripts/decode_ipv6_index.py](../scripts/decode_ipv6_index.py); define `decoder` as its installed package-local path and use Python 3:

~~~bash
python3 "$decoder" "$octets"
~~~

It rejects wrong counts, nondecimal and out-of-range bytes, preserves zero bytes and prints the compressed address with exact loopback/link-local/Unique-Local membership. Failure is invalid input, not an absent IPv6 interface. The source's zero-skipping/unpadded Bash conversion is not a general decoder: zeros and octet width matter.

An address-table row is inventory evidence, not a routed reachable service or proof of a globally assigned address. Link-local communication requires the correct local link/scope. IPv6 URL literals require brackets around the address; transport and authorization still need separate evidence. Enyx's labels are not an address-class authority. Finish with the exact acquired row, decoded address/interface index and query/coverage limits. See [IP-MIB](https://www.rfc-editor.org/rfc/rfc4293), [IPv6 architecture](https://www.rfc-editor.org/rfc/rfc4291) and [Unique Local prefix](https://www.rfc-editor.org/rfc/rfc4193).
