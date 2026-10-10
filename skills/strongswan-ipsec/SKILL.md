---
name: strongswan-ipsec
description: Inspect existing strongSwan VPN sessions and diagnose established IPsec connections that carry no application traffic. Distinguish IKE authentication, CHILD SAs, transport selectors and kernel policy.
---

# Inspect an existing strongSwan connection

Read this entire skill before acting, plus the applicable reference; complete current context need not be re-read. Identify the installed strongSwan control interface and intended connection before interpreting status. Finish with the observed IKE/CHILD state and evidence for the requested traffic, or the specific missing access/evidence. This workflow inspects an existing deployment; it does not configure credentials or restart it.

When a CHILD SA is present but the application fails, or a legacy transport-mode configuration needs interpretation, read [traffic selectors and packet path](references/traffic-selectors.md) fully before its procedure.

Use the existing deployment's interface. An executable named `ipsec` alone does not identify strongSwan; other implementations use that name too. Confirm with `ipsec --version`. For a strongSwan starter/stroke deployment, set `connection` to its configured connection name:

~~~bash
ipsec statusall "$connection"
~~~

For a deployment using swanctl/VICI instead, define `ike_name` as the intended IKE connection name:

~~~bash
swanctl --list-sas --ike "$ike_name"
~~~

Use the interface already available, not both as a mandatory sequence. A missing control socket, command or permission is a local prerequisite failure, not proof of peer failure. Do not load configurations or restart the daemon to make a status query work.

| Evidence | What it supports |
|---|---|
| A configured connection, without an established SA | Configuration exists; authentication and data traffic remain unproved. |
| IKE `ESTABLISHED` | The management association is established. Inspect dependent CHILD SAs next. |
| CHILD `INSTALLED` with mode, SPIs and selectors | A data association exists for those selectors; application reachability remains a separate question. |
| Relevant in/out counters increase across an approved application check | Traffic crossed the observed SA. Correlate the time/flow and application response before claiming success. Other traffic can advance counters too. |

Inspect the actual status text. A zero exit from the legacy `ipsec statusall` wrapper can describe the running service rather than the requested connection's health. Empty filtered output also does not establish why the named SA is missing. Preserve relevant names, endpoint identities, selectors, timestamps and errors without copying secrets into reports.

Sources: [legacy controls](https://github.com/strongswan/strongswan/blob/master/README_LEGACY.md), [status wrapper](https://github.com/strongswan/strongswan/blob/master/src/ipsec/_ipsec.in), [swanctl SA output](https://docs.strongswan.org/docs/latest/swanctl/swanctlListSas.html).
