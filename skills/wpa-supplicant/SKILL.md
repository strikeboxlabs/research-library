---
name: wpa-supplicant
description: Run a foreground wpa_supplicant connection using an existing approved network configuration. Use to separate initialization, wireless authentication and later IP configuration.
---

# Connect a selected test interface

Read this entire SKILL.md before acting. Require an enabled owned wireless interface, sufficient privilege and an existing private configuration for the approved network and legitimately supplied credentials. No conditional resources are required. Finish with association/authentication evidence and the owned process lifecycle.

Confirm that another network manager or supplicant does not control this interface. Use a dedicated test interface; avoid disrupting the connection carrying the session. Define `interface`, absolute `config`, and `driver` selected from installed help:

For an enterprise EAP profile, obtain the approved CA trust and authentication-server name from the network administrator before connecting. The profile must validate both: `ca_cert` selects a trusted CA file; `domain_match` restricts an exact server name, while `domain_suffix_match` allows the stated domain and its subdomains. Select the intended scope deliberately. An SSID or successful TLS connection alone does not identify the legitimate authentication server. Missing trust/name constraints are a profile prerequisite failure; do not disable certificate checks to recover from rejection. Keep credentials out of diagnostic output. These fields belong in the existing private network block, not shell arguments.

~~~bash
wpa_supplicant -v
wpa_supplicant -h
wpa_supplicant -i "$interface" -c "$config" -D "$driver"
~~~

This stays in the foreground; `-B` instead backgrounds it. Initialization success alone is incomplete. Inspect subsequent authentication/key-negotiation and connection events. Driver or rfkill errors require their own diagnosis; do not infer success from a startup banner. Avoid `-K`, which logs keys.

DHCP, routes and DNS are separate subsequent work. Keep this process running while testing the connection. End only the owned foreground process with Ctrl-C when finished, then verify the intended interface state; stopping it is not a rollback of separately applied IP settings.

Reference: [wpa_supplicant options and connection stages](https://manpages.debian.org/bookworm/wpasupplicant/wpa_supplicant.8.en.html).

Enterprise profile reference: [upstream configuration shipped in Android](https://android.googlesource.com/platform/external/wpa_supplicant_8/+/refs/heads/main/wpa_supplicant/wpa_supplicant.conf).
