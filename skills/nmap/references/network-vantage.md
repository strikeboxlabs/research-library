# Host discovery from an internal network context

Establish the authorized address range from actual interface prefix/routing evidence, not from `hostname -I` or a container-looking address alone. Record the current network namespace, execution identity and Nmap version/data directory. Names returned by reverse DNS are leads for protocol-specific inspection, not proof of service role or a trust boundary.

Define `targets` as the deliberately bounded permitted range and `discovery` as a fresh output prefix:

~~~bash
nmap -sn --reason -oA "$discovery" "$targets"
~~~

`-sn` skips the port scan after host discovery. It does not identify every listening service or prove that silent addresses are absent. Probe behavior depends on local/raw-socket authority and link type: privileged local Ethernet discovery commonly uses ARP; unprivileged Unix discovery uses TCP connect probes. Preserve the responding addresses and reasons, then select individual hosts/ports for service investigation. On an independently reachable selected host, `-Pn` can avoid a mismatched discovery probe; it does not establish that all addresses in a range are online.

A transferred static Nmap binary may lack its data files or have a much older version than the operator's local Nmap. A warning about missing `nmap-payloads` means affected UDP discovery probes are unavailable, not that every other result is invalid or all hosts were covered. Service probing also depends on its data files. Match the actual executable and required data before diagnosing a missing service; do not interpret a copied walkthrough's fixed minimum rate as an accuracy guarantee. Finish with this vantage, completed range/probe coverage and unresolved silent hosts. See [Nmap host discovery](https://nmap.org/book/man-host-discovery.html) and [data files](https://nmap.org/book/data-files.html).
