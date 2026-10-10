# Change one live forwarding zone and verify the result

Use this when the requested administration or authorized assessment actually requires a live resolver change. Define `config`, `control_endpoint`, the exact owned `zone` and intended `upstream_addr` (IP, optionally `@port`). Establish control access and server command support. A help listing alone cannot prove support on a custom server.

Capture the current zone, relevant local zones and domain-insecure state using `list_forwards`, `list_local_zones` and `list_insecure`. Preserve an existing rule's addresses, TLS and validation settings. Use a fresh narrowly scoped test zone when possible. If policy is unreadable/commands unavailable, obtain a known baseline and recovery route before changing it; do not infer an empty policy from an unknown-command error.

For an intended forward zone that retains normal DNSSEC validation:

~~~bash
unbound-control -c "$config" -s "$control_endpoint" forward_add "$zone" "$upstream_addr"
~~~

Only when disabling validation for this exact zone is part of the intended task:

~~~bash
unbound-control -c "$config" -s "$control_endpoint" forward_add +i "$zone" "$upstream_addr"
~~~

`+i` also adds domain-insecure; it is not a connectivity fix. `+t` selects TLS upstream on supporting versions and needs an appropriate upstream/configuration. Neither flag configures the control channel's own TLS. Use the supported upstream-address syntax and preserve all required upstreams for a replaced rule.

Inspect the command result and active rule, then query through this resolver using an existing DNS client. Record the exact name/type, resolver and returned answer/error. A local-zone rule can answer/refuse a name before forwarding is reached. An included local policy, DNSSEC failure, cached answer or network failure needs its own diagnosis. Successful control mutation is not successful client resolution.

If an intentionally changed policy needs a fresh answer and a zone-scoped cache flush is authorized, `flush_zone "$zone"` is available through the same control invocation. It changes cached state for that zone and cannot restore the prior cache; don't flush the entire resolver by default. Keep cache treatment with the result.

For a newly added zone with no previous domain-insecure rule, undo the matching change:

~~~bash
unbound-control -c "$config" -s "$control_endpoint" forward_remove "$zone"
# For a new +i rule, when its insecure state was also absent before:
unbound-control -c "$config" -s "$control_endpoint" forward_remove +i "$zone"
~~~

Select one removal matching the actual prior state. If forwarding was new but domain-insecure pre-existed, preserve that insecure rule instead of removing it. If a forward rule existed, restore its exact saved settings and verify them; deleting it is not restoration. A custom server lacking remove/read commands needs its separate approved recovery route. Reload/restart affects more than this zone and is not a default cleanup step.

These control changes affect running state rather than saving a new configuration file; verify the installed version's behavior across reload. Finish with the before/after client result and either the retained intended policy or evidenced restoration. See [commands](https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html) and [local/forward-zone policy](https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html).
