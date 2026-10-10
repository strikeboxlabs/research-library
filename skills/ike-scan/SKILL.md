---
name: ike-scan
description: Probe a known IKE/IPsec endpoint and interpret its initial proposal response, notify errors and vendor fingerprints. Use when UDP 500 responds but VPN negotiation requirements remain unclear.
---

# IKE endpoint and proposal evidence

Read this entire skill before acting; current complete context need not be re-read. Use one authorised peer and retain the offered proposal, response and probe conditions. Completion is a supported statement about the response; this probe does not establish an authenticated VPN or recover a PSK.

Check `ike-scan --version` and `--help` for the installed implementation. The procedure below uses the default **IKEv1 Main Mode**. It sends an initial proposal and decodes the reply without completing that exchange. An IKEv2-only peer needs a different probe; upstream labels `--ikev2` experimental with limited proposal support, so do not assume feature parity.

Define `peer` as the selected IP and `output` as a fresh private file:

~~~bash
umask 077
ike-scan --multiline --retry=2 "$peer" >"$output"
~~~

`--retry=2` means two total attempts per host. `--multiline` separates decoded payloads. The default source and destination ports are UDP 500; binding the source may require privilege and will fail if another local process owns it. A bind error says nothing about the peer. Do not stop an existing VPN daemon to free the port. A high source port is an alternative only where the peer permits it; some require 500.

The default proposals include old algorithms. They are probe inputs, not recommended VPN settings. If the question concerns a particular approved proposal, specify it using this version's documented `--trans` syntax and record that input. A response selects from what was offered; it does not enumerate every supported suite.

| Observation | Interpretation and next decision |
|---|---|
| `Handshake returned` with an SA transform | The peer accepted an initial proposal. Record encryption, hash, DH group and authentication method; no completed authentication or usable data SA has been demonstrated. |
| `NO-PROPOSAL-CHOSEN` | A responder rejected this proposal. Compare protocol/proposal requirements before another bounded probe; the endpoint is not absent. |
| No matching reply | Protocol/version, proposal, source port, packet loss and filtering remain candidates. Preserve the probe conditions rather than declaring IKE unavailable. |
| Vendor IDs or a backoff fingerprint | Implementation clues, potentially shared between products/releases. Confirm independently before claiming an exact operating system or patch level. |

For a known NAT-T endpoint, `--nat-t` supplies its IKE framing and changes default source/destination ports to 4500; merely changing the destination port is not equivalent. Do not infer that an inner TCP-only IPsec policy means IKE itself uses TCP.

Sources: [upstream scanner behavior](https://github.com/royhills/ike-scan), [option definitions](https://github.com/royhills/ike-scan/blob/master/ike-scan.1).
