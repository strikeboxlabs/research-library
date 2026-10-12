---
name: nslookup
description: Query a selected DNS server for MX and address records with BIND nslookup. Use when resolver choice, MX preference or an empty reply is being confused with mail-service availability.
---

# Keep resolver and answer identity

Read this entire SKILL.md before acting. Require the selected name/server and retain complete replies and status. No conditional resources are required. Finish with the requested DNS evidence and unresolved routing or authority questions.

Confirm BIND `nslookup -version`. Define `domain` as an absolute domain ending in a dot and `resolver` as the intended numeric DNS-server address:

~~~bash
nslookup -timeout=3 -retry=1 -type=MX "$domain" "$resolver"
status=$?
~~~

Omitting the server uses configured resolution. Supplying a server does not establish its authority for that zone. Keep timeout, NXDOMAIN, SERVFAIL and a successful answer without the requested records distinct; status alone cannot identify the cause.

Retain every MX preference/hostname pair. Lower **numeric** preferences come first; lexical sorting can put 10 before 2. Preserve equal-preference alternatives. Define `exchange` as one returned absolute hostname, then inspect addresses separately:

~~~bash
nslookup -type=A "$exchange" "$resolver"
nslookup -type=AAAA "$exchange" "$resolver"
~~~

Resolver address lines are not exchange addresses. DNS results do not prove SMTP reachability or delivery.

Sources: [BIND nslookup](https://bind9.readthedocs.io/en/v9.18.49/manpages.html#nslookup-query-internet-name-servers-interactively), [MX preference](https://www.rfc-editor.org/rfc/rfc5321.html#section-5).
