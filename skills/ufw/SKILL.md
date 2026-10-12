---
name: ufw
description: Add and remove one approved source-specific IPv4 or IPv6 TCP ingress rule on an already active UFW firewall. Use to distinguish stored rule acceptance, rule ordering, effective filtering and actual service connectivity.
---

# Make one selected ingress-rule change

Read this entire SKILL.md before acting. Require installed UFW, approved administrative privileges, an already active firewall, the existing rule baseline and one owned service/source/interface. IPv6 rules additionally require IPv6 firewalling enabled. Read the removal steps before a temporary change. Finish with the exact rule, status, actual service check and any unresolved restoration.

Check `ufw --version` and `--help`. Under the approved administrative context, inspect `ufw status verbose`, `ufw status numbered` and the deployment's selected address-family setting. Inactive status, or disabled IPv6 for an IPv6 task, is a separate prerequisite; adding a rule does not prove effective filtering. Enabling/reloading/resetting or changing default policy is a different task with connection effects.

Define `interface`, `source_address`, `destination_address` and `port` as the verified ingress interface, single approved peer, owned local address in the same family and TCP service port. Preview:

~~~bash
ufw --dry-run allow in on "$interface" proto tcp from "$source_address" to "$destination_address" port "$port"
~~~

Compare with the baseline. If the exact rule already exists, record it instead of claiming ownership or later deleting it. For a new approved rule:

~~~bash
ufw allow in on "$interface" proto tcp from "$source_address" to "$destination_address" port "$port"
ufw status numbered
~~~

Record acceptance and placement, then check the intended service from the approved peer. Earlier matching rules, other filtering, routing and service binding can change the outcome; a rule-added message is not a successful connection. Explicit TCP avoids an omitted protocol allowing both TCP and UDP. An ingress rule is not a forwarded-traffic rule.

For removal of this newly owned rule, preserve the same selectors:

~~~bash
ufw --dry-run delete allow in on "$interface" proto tcp from "$source_address" to "$destination_address" port "$port"
~~~

Review the deletion preview, then apply:

~~~bash
ufw delete allow in on "$interface" proto tcp from "$source_address" to "$destination_address" port "$port"
ufw status numbered
~~~

Compare the final baseline and preserve failures. Numbered positions can shift; exact rule deletion avoids stale-number selection. Generic IPv4/IPv6 paired rules have different deletion effects from a specific IPv6 rule. Do not remove a pre-existing shared rule as temporary cleanup. See the [packaged UFW manual](https://manpages.ubuntu.com/manpages/noble/man8/ufw.8.html) for rule syntax and management effects.
