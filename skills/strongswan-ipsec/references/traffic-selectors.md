# An installed SA does not cover every packet

Use this for an existing strongSwan connection with mismatched traffic or legacy transport-mode settings. Obtain its status/logs, the intended local/remote application addresses and protocol/ports, and the application's network namespace. These are different from IKE endpoint identities and its UDP transport ports.

In transport mode ESP protects the payload while retaining the original IP header. Tunnel mode encapsulates the original IP packet. In legacy `ipsec.conf`, `leftprotoport`/`rightprotoport` restrict protected traffic; current upstream marks them deprecated in favor of selectors attached to subnets. A value of `tcp` does not change IKE from UDP to TCP. An ICMP ping or UDP probe cannot test a TCP-only selector.

**Illustrative log interpretation:** a CHILD SA with selectors `192.0.2.10/32[tcp] === 192.0.2.20/32[tcp]` covers TCP between those addresses, subject to its other policy conditions. It says nothing about traffic from a different source address, a routed subnet or ICMP. Retain the negotiated selectors rather than assuming the configured proposal was accepted unchanged.

For a Linux kernel-XFRM deployment, inspect policy in the namespace carrying the application, using the required existing read permissions:

~~~bash
ip xfrm policy list
~~~

Compare `src`, `dst`, protocol/ports, `dir`, marks/interface IDs when present, and the template's mode/`reqid` with the relevant SA. Missing permission is not empty policy. A matching route alone does not prove policy selection or encryption. Plain `ip xfrm state` may disclose key material; policy and daemon status are sufficient for this initial comparison. A userspace IPsec backend requires its own diagnostics instead of assuming kernel policy applies.

For the next observation, use the approved application protocol from the intended source/namespace. If service discovery is the task, a selected-port Nmap `-sT` uses the operating system's `connect()` path; raw-packet probes can take a different path. This is a diagnostic choice, not a universal firewall bypass. Compare that one check with the SA's counters and returned application data. When only outgoing counters advance, inspect the peer/return path and filters; when neither changes, check source/selector selection first. Counters may aggregate concurrent traffic and reset at rekey.

When reading a legacy configuration, `ike=` and `esp=` govern different negotiations. Historical `3des-sha1-modp1024` settings are not deployment defaults to copy. Secret-file selectors identify authentication identities, which need not be IP addresses; do not treat them as an unconditional source/destination pair or expand `%any` to solve a mismatch. Record the discrepancy for the connection owner rather than rewriting authentication or restarting all connections during diagnosis.

Sources: [IPsec packet model](https://docs.strongswan.org/docs/latest/howtos/ipsecProtocol.html), [legacy configuration](https://github.com/strongswan/strongswan/blob/master/man/ipsec.conf.5.in), [secret selectors](https://github.com/strongswan/strongswan/blob/master/man/ipsec.secrets.5.in), [XFRM policy](https://man7.org/linux/man-pages/man8/ip-xfrm.8.html), [Nmap connect scans](https://nmap.org/book/scan-methods-connect-scan.html).
