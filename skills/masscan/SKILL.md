---
name: masscan
description: Discover scoped TCP and selected UDP responders with Masscan, preserve host and protocol in results, and hand selected ports to a service probe. Use for bounded discovery and diagnosing incomplete or misleading scan output.
---

# Masscan discovery and follow-up

Read this entire SKILL.md before acting. Review effective scope/interface/rate before sending probes; preserve per-host/protocol discovery and follow-up evidence. Finish with completed coverage and separately confirmed services or the specific route/loss gap.

Installed invocation: `/usr/bin/masscan`, version `1.3.2`. For a tunneled destination, compare the adapter in the `--echo` preview with the selected route before interpreting an empty scan. Define the interface from current route evidence rather than assuming `tun0`; validate a small approved known-listening port selection before expanding to the requested range.

Masscan sends raw packets using its own network stack. Use it for port discovery; a responsive port still needs protocol confirmation. Check the installed version and raw-packet privileges. Targets are IP addresses/ranges, not DNS names. A working TCP connection through a VPN or proxy does not establish that Masscan's selected adapter can send and receive raw probes there.

For one scoped IPv4 address, define `target`, an explicit comma-separated TCP `ports` selection, a packet-per-second `rate`, and the verified outbound `interface`. Use fresh absolute `results` and `config` paths in an existing directory. Preview the effective configuration without scanning:

~~~bash
/usr/bin/masscan "$target" -p "$ports" --rate "$rate" -e "$interface" -oL "$results" --echo > "$config"
~~~

Review the generated ranges, ports, adapter, rate, output and exclusions; `/etc/masscan/masscan.conf` can contribute defaults. Do not assume an old tunnel name or a walkthrough's rate fits this route. Once the resulting scope and options are correct, run with the environment's approved raw-packet privileges:

~~~bash
/usr/bin/masscan -c "$config"
~~~

Retain diagnostics and wait for completion, including the final receive interval (`--wait`). Interruptions or excessive loss leave discovery incomplete. An empty result does not prove the host has no listeners; inspect adapter, route, exclusions and packet loss before repeating a smaller selection.

## Preserve the target when selecting follow-up ports

`-oL` writes list records in the order **state, protocol, port, IP, POSIX timestamp**, plus comments and possibly other record types. For example, this is **illustrative**:

~~~text
open tcp 80 192.0.2.20 1700000000
open tcp 443 192.0.2.21 1700000001
open udp 53 192.0.2.20 1700000002
~~~

For `target=192.0.2.20`, only TCP port 80 belongs in this TCP follow-up. After inspecting the completed discovery, derive a deduplicated list for exactly that host:

~~~bash
ports_found=$(awk -v host="$target" '$1 == "open" && $2 == "tcp" && $4 == host {print $3}' "$results" | sort -nu | paste -sd, -)
if [ -n "$ports_found" ]; then
    /usr/bin/nmap -n -Pn -sT -sV -p "$ports_found" "$target"
else
    printf '%s\n' 'No matching open TCP records; review discovery before follow-up.'
fi
~~~

This Nmap command actively connects and probes services on the selected ports; `-Pn` skips host discovery. Repeat separately for other scoped hosts. Keep UDP observations separate and use a UDP-capable follow-up. Never drop an empty `-p` argument and accidentally fall back to Nmap's default port set.

## Mixed TCP and UDP discovery

On a build supporting Nmap-style protocol selectors, a selection such as `ports=1-65535,U:53,U:161` includes that TCP range and the two explicit UDP ports; use `--echo` to review it before the scan above. `U:1-65535` instead requests the whole UDP range, a separate scope/cost decision. The configured packet rate applies to probes, not a guarantee of coverage or useful UDP payloads. Do not infer the tested protocol from a familiar service port number.

If a mixed scan displays only TCP responders, that is not a completed proof that UDP services are absent. Preserve UDP scope, probe support, loss and final receive status separately; follow selected UDP observations with a UDP-capable protocol probe. Passing their port numbers to the TCP Nmap command above changes the protocol and cannot confirm them. See the [upstream protocol/port selectors](https://github.com/robertdavidgraham/masscan/blob/master/doc/masscan.8).

Masscan banner collection can fail when the host kernel sends resets for connections handled by Masscan's separate stack. A missing banner does not negate an open-port observation. Prefer a normal service probe before considering source-IP or firewall changes. Retain the tested ranges, vantage, completion status and discovery/service results separately.

Resolve format and interface differences with the [upstream guide](https://github.com/robertdavidgraham/masscan), [manual](https://github.com/robertdavidgraham/masscan/blob/master/doc/masscan.8) and [list writer](https://github.com/robertdavidgraham/masscan/blob/master/src/out-text.c).
