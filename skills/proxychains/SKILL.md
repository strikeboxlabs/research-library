---
name: proxychains
description: Route compatible Linux TCP clients through an explicit ProxyChains-NG configuration. Use when SOCKS reachability, DNS behavior or unsupported raw/UDP traffic causes misleading failures.
---

# ProxyChains-NG routing checks

Identify the installed implementation and executable, commonly `proxychains4`. ProxyChains-NG hooks libc networking in dynamically linked programs using a preload library. It supports TCP; it is not a system-wide VPN and does not carry raw SYN scans, ICMP or UDP. Static binaries, privileged execution and some runtimes/subprocesses can bypass or break interception.

Define `proxy_config` as a private task-specific file. For one already-running local SOCKS5 endpoint, a minimal example is:

~~~text
strict_chain
proxy_dns
tcp_read_time_out 15000
tcp_connect_time_out 8000
[ProxyList]
socks5 127.0.0.1 1080
~~~

Replace the endpoint with the observed listener. Use only one chain mode, inspect bypass rules such as `localnet`, and do not alter the machine's global config for one task. `strict_chain` requires every configured proxy; dynamic mode can skip unavailable proxies, changing the actual route.

Define `url` as a known authorized HTTP endpoint reachable through the exit host:

~~~bash
proxychains4 -f "$proxy_config" curl --connect-timeout 5 --max-time 20 "$url"
~~~

Keep proxy diagnostics visible until the connection and exit path are established. A wrapper banner alone does not prove all network traffic used the proxy. Confirm using an endpoint/log you control, not an unrelated public address-checking service. For tools with native SOCKS support, explicit native configuration is usually easier to verify; DNS-at-proxy support remains a separate choice.

For selected numeric targets/ports with Nmap, use TCP connect mode `-sT -Pn -n` through the wrapper, not raw-packet discovery. This limits protocol mismatch; it does not make scanning cost-free or guarantee every Nmap subsystem is proxied.

Kerberos libraries may try UDP first. MIT's `udp_preference_limit = 1` in a task-specific configuration makes normal requests prefer TCP, but fallback is still possible. Verify the real client transport rather than declaring UDP tunneled. DNS errors, proxy authentication errors and destination refusals require different fixes. Report the actual application, configuration and tested route.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Anubis pp. 8–9, 17. Sources: [NG compatibility](https://github.com/rofl0r/proxychains-ng), [configuration](https://github.com/rofl0r/proxychains-ng/blob/master/src/proxychains.conf), [MIT transport preference](https://web.mit.edu/kerberos/krb5-latest/doc/admin/conf_files/krb5_conf.html#libdefaults).
