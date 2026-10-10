---
name: openvpn
description: Use an approved OpenVPN client profile and diagnose tunnel, route and service reachability separately. Use when initialization succeeds but an internal address or hostname remains unreachable.
---

# Connect a reviewed client profile

Read this entire SKILL.md before acting; reuse complete current context. Starting a VPN changes interfaces/routes and can affect the worker's connection. Use only an approved profile and existing network-administration rights. For a connection that starts but cannot reach its intended service, read [route diagnosis](references/routes.md) completely before following that branch. Finish with the tunnel state, selected route and observed service result; initialization alone is a partial result.

Define `profile_dir` as the existing absolute directory containing the approved profile and its relative resources, and `profile_name` as the profile filename. Review its remote/transport, trust and client credentials, included configurations, scripts/plugins, and route/DNS directives first. A downloaded `.ovpn` file is configuration with possible executable hooks, not passive data. Preserve required server-certificate verification; do not disable it to make a connection succeed.

In a retained foreground session, under the identity authorised to create the tunnel:

~~~bash
openvpn --cd "$profile_dir" --config "$profile_name" --verb 3
~~~

`--cd` resolves relative profile resources from the intended directory. Keep interactive authentication in the approved secret channel. Capture the actual interface name and address, pushed options, route errors and subsequent reconnects. Do not assume `tun0`: another VPN can already occupy it. `Initialization Sequence Completed` reports initialization, not permission to reach every routed system or proof that an application works.

Stop this owned foreground instance with Ctrl-C when its task is over and check that its routes/interface were removed as expected. Preserve other VPN sessions. A profile using persistence, management or daemon options needs its own lifecycle review before use.

If startup fails, distinguish missing TUN/privileges, certificate/name/time validation, authentication rejection and cipher negotiation. Match the installed client's options and peer configuration instead of blindly copying compatibility or compression switches. OpenVPN 2.6 TLS-mode cipher negotiation uses `data-ciphers`; an old `cipher` line alone does not set that policy.

See the [OpenVPN manual](https://openvpn.net/community-docs/community-articles/openvpn-2-6-manual.html) for profile resolution, hooks, lifecycle and version-specific options.
