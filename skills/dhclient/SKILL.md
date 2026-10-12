---
name: dhclient
description: Acquire and inspect an ISC DHCPv4 lease on one dedicated Linux test interface. Use when association works but address configuration, hooks or competing clients remain unclear.
---

# Obtain one interface's DHCP configuration

Read this entire SKILL.md before acting. Require ISC dhclient, privilege, an approved DHCP network and a dedicated interface with working link/association. No conditional resources are required. Finish with lease, effective address/route/resolver evidence and lifecycle outcome.

No other client or network manager may own the selected interface. Do not use the interface carrying the management session. Review the installed network script and its hooks: they can change routes and resolver configuration beyond the selected interface. Record the original state and the intended restoration before starting.

Define `interface`, `config` as a reviewed client configuration containing no additional interfaces, and fresh absolute `pid_file`/`lease_file` paths in an existing private directory:

~~~bash
dhclient --version
dhclient -4 -d -1 -cf "$config" -pf "$pid_file" -lf "$lease_file" "$interface"
~~~

`-d` stays in the foreground with verbose events. `-1` exits with status2 if initial acquisition fails; success does not mean this foreground renewal process immediately exits. Omitting the interface can configure multiple devices. Retain the actual lease exchange and matching effective configuration. An address alone does not prove its origin. A netlink error can coexist with partial configuration; compare address, routes and resolver state before retrying.

For agreed teardown, verify the PID file still names this owned client, then in another terminal:

~~~bash
dhclient -4 -r -cf "$config" -pf "$pid_file" -lf "$lease_file" "$interface"
~~~

Release stops the recorded client and invokes network cleanup hooks. Verify process exit and the intended restored network state; interruption alone does not establish cleanup. Preserve unresolved hook errors and do not stop unrelated clients.

References: [ISC client options](https://manpages.debian.org/bookworm/isc-dhcp-client/dhclient.8.en.html), [network script and hooks](https://manpages.debian.org/bookworm/isc-dhcp-client/dhclient-script.8.en.html).
