# Read selected Squid manager reports

Require an owned known manager endpoint, its current ACL/action policy and an already provisioned password if required. Set `manager_base` to the verified `http[s]://host:port/squid-internal-mgr` URL and `manager_user` to the configured client username. Use private fresh `headers` and `body` files for each report:

~~~bash
umask 077
curl --noproxy '*' --user "$manager_user" --silent --show-error --connect-timeout 5 --max-time 30 --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\npeer=%{remote_ip}\n' "$manager_base/menu"
report_status=$?
~~~

This connects directly to the selected endpoint, intentionally bypassing inherited proxies. `--user` supplies origin HTTP authentication and prompts for the password when needed; `--proxy-user` authenticates to a transport proxy instead. Keep TLS verification. Historical manager clients can use an arbitrary username with the action password; a literal `cachemgr_passwd` username in a walkthrough is not a universal account requirement.

Check transport status, HTTP status and actual body. The menu describes available actions and access labels for that Squid version. A protected or disabled action is not an invitation to guess a password. Action passwords and manager ACLs are separate controls. Even GET manager actions can change state: select only a confirmed read-only report.

For the permitted FQDN-cache report, repeat the capture with fresh outputs and `"$manager_base/fqdncache"`. Interpret the report's flags and version-specific columns. `H` identifies hosts-file entries; it does not establish a current DNS lookup. Negative TTL and cached names do not prove host availability. `Cnt` counts names for an entry, not connected clients. Treat these as metadata, not authorization to contact listed addresses or expand to their surrounding subnets.

A custom `Intranet-Host` response header is a deployment assertion, not authenticated backend identity or proof of a live load-balancing topology. Correlate configuration/logs when that distinction matters.

References: Squid [manager client authentication](https://wiki.squid-cache.org/Features/CacheManager/SquidClientTool), [FQDN-cache report](https://wiki.squid-cache.org/Features/CacheManager/FqdnCache), [version-specific action passwords](https://www.squid-cache.org/Doc/config/cachemgr_passwd/).
