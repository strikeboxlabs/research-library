---
name: ufw
description: Add and remove one approved source-specific IPv6 TCP ingress rule on an already active UFW firewall. Use to distinguish stored rule acceptance, rule ordering, effective filtering and actual service connectivity.
---

# Make one selected ingress-rule change

Read this entire SKILL.md before acting. Require installed UFW, approved administrative privileges, an already active firewall with IPv6 enabled, the existing rule baseline and one owned service/source/interface. Read the removal steps before a temporary change. Finish with the exact rule, status, actual service check and any unresolved restoration.

Check `ufw --version` and `--help`. Under the approved administrative context, inspect `ufw status verbose`, `ufw status numbered` and the deployment's IPv6 setting. Inactive status or disabled IPv6 is a separate prerequisite; adding a rule does not prove effective IPv6 filtering. Enabling/reloading/resetting or changing default policy is a different task with connection effects.

Define `interface`, `source_ipv6`, `destination_ipv6` and `port` as the verified ingress interface, single approved peer, owned local IPv6 address and TCP service port. Preview:

~~~bash
ufw --dry-run allow in on "$interface" proto tcp from "$source_ipv6" to "$destination_ipv6" port "$port"
~~~

Compare with the baseline. If the exact rule already exists, record it instead of claiming ownership or later deleting it. For a new approved rule:

~~~bash
ufw allow in on "$interface" proto tcp from "$source_ipv6" to "$destination_ipv6" port "$port"
ufw status numbered
~~~

Record acceptance and placement, then check the intended service from the approved peer. Earlier matching rules, other filtering, routing and service binding can change the outcome; a rule-added message is not a successful connection. Explicit TCP avoids an omitted protocol allowing both TCP and UDP. An ingress rule is not a forwarded-traffic rule.

For removal of this newly owned rule, preserve the same selectors:

~~~bash
ufw --dry-run delete allow in on "$interface" proto tcp from "$source_ipv6" to "$destination_ipv6" port "$port"
~~~

Review the deletion preview, then apply:

~~~bash
ufw delete allow in on "$interface" proto tcp from "$source_ipv6" to "$destination_ipv6" port "$port"
ufw status numbered
~~~

Compare the final baseline and preserve failures. Numbered positions can shift; exact rule deletion avoids stale-number selection. Generic IPv4/IPv6 paired rules have different deletion effects from a specific IPv6 rule. Do not remove a pre-existing shared rule as temporary cleanup. See the [packaged UFW manual](https://manpages.ubuntu.com/manpages/noble/man8/ufw.8.html) for rule syntax and management effects.
