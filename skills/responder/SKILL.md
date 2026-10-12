---
name: responder
description: Distinguish Responder name-resolution observation from active authentication listeners in a scoped lab. Use to verify the enabled modules, diagnose missing captures and preserve complete NetNTLMv2 evidence.
---

# Responder modes and capture evidence

Read this entire SKILL.md before acting; complete current context need not be re-read. Select the observation or direct-listener task below, then require the installed entrypoint, scoped interface, reviewed module configuration and private evidence location before starting. No package-local references are required. Finish with the enabled modules, bind results, observation window, actual events and remaining gaps; unavailable listeners or incomplete records are partial evidence, not a successful capture.

Responder combines name-resolution responders with independent authentication servers. Check the installed entrypoint/help and the actual `Responder.conf` it loads. Upstream reads the configuration beside its installation; changing the current directory alone does not select a different file. Use a reviewed lab configuration with a private log/database location, not unexplained global defaults.

Choose the intended behavior before starting:

| Task | Configuration and meaning |
|---|---|
| Observe selected LLMNR/NBT-NS/mDNS requests | Keep the required name listeners enabled, disable authentication servers and unrelated DHCP/IPv6/proxy features, and use `-A`. |
| Receive an explicitly planned direct SMB authentication | Enable SMB only, disable name poisoners and unrelated servers/features, and use `-A` as an additional name-poisoning guard. This still actively answers SMB and collects authentication material. |

`-A` suppresses LLMNR/NBT-NS/mDNS poisoning. It does **not** globally disable authentication servers; do not call the second configuration passive. An icon reference to a literal UNC address can reach SMB directly without name poisoning. Reproducing the client-side trigger is a separate operation, not a prerequisite for observing existing events.

Define `interface` as the verified scoped Linux interface and `log` as a fresh private transcript. Run with the lab's approved listener privileges for the selected ports:

~~~bash
responder -I "$interface" -A -v > "$log" 2>&1
~~~

Inspect the startup configuration and listener diagnostics immediately. Avoid `ALL` when one interface is intended. Configured `RespondTo` filters name-response decisions; do not assume it restricts every authentication listener. Ensure the lab/network boundary also matches the collection scope. A port-bind failure can coexist with other running modules. An SMB bind failure leaves that capture path unavailable even if other modules remain running. Resolve the actual conflict before changing any services.

## Interpret what arrived

An **illustrative** `[SMB] NTLMv2-SSP Username: LAB\testuser` labels challenge-response material, not a raw NT password hash or recovered password. Preserve the complete saved record, client address, domain/account, protocol and timestamp. Console excerpts or PDF records containing ellipses cannot be used for offline verification.

For a subsequent authorized offline check, a complete `user::domain:challenge:response:blob` NetNTLMv2 record maps to Hashcat mode `5600`; a raw NT hash maps to `1000`. The captured response cannot substitute for an NT hash in a service-key option. Successful capture does not establish that a password is recoverable, valid for another service or associated with the person viewing a particular folder.

If no new credential line appears, check the selected interface/address, listener bind status, client reachability/egress, configured modules and whether the client actually requested authentication. The database can suppress repeated console results; inspect existing records/logs rather than deleting evidence to force a new capture. Stop the selected process after the observation window and retain its actual coverage and errors.

Resolve version differences with the [project guide](https://github.com/lgandx/Responder), [startup code](https://github.com/lgandx/Responder/blob/master/Responder.py), [configuration loader](https://github.com/lgandx/Responder/blob/master/settings.py) and [logging/filter handling](https://github.com/lgandx/Responder/blob/master/utils.py).
