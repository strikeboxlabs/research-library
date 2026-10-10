---
name: whatweb
description: Fingerprint a selected web endpoint with WhatWeb and interpret technology/version matches. Use when choosing a protocol-specific investigation from headers, HTML or redirects without treating a banner as proof of a vulnerability.
---

# Web technology evidence

Read this entire skill before acting; complete current context need not be re-read. Start with the exact scoped URL and bounded request behavior. Finish with observed matches, their evidence and uncertainty; a fingerprint is a lead for the next task, not confirmation of installation, exploitability or access.

Check `whatweb --version` and `--help`. Define `url` with its intended scheme, hostname, port and path, and `report` as a fresh private log file:

~~~bash
umask 077
whatweb --aggression=1 --follow-redirect=never \
  --open-timeout=5 --read-timeout=10 --log-verbose="$report" "$url"
~~~

Level 1 inspects the response from an HTTP request; it is still active traffic. Redirect following is normally enabled, so explicitly disabling it keeps the initial observation at the selected endpoint. Inspect a returned Location and its scope before scanning the next URL. Connect/read timeouts bound those operations, not a complete multi-target job.

| Result | Interpretation and next check |
|---|---|
| A server, language or CMS match | Inspect the plugin's evidence. Several labels may all derive from one header rather than independent observations. |
| A version string | Compare its source with the actual deployment when available. Reverse proxies, altered headers and backports can make a banner insufficient for a version/CVE conclusion. |
| A login, denial or generic fallback page | The fingerprint describes that response. Preserve the route/authentication context before comparing it with another endpoint. |
| No match or a transport error | Missing plugins/evidence and failed retrieval are different. Keep errors; absence of a plugin match does not prove absence of the technology. |

**Illustrative:** `PHP[8.2.15]` and `X-Powered-By[PHP/8.2.15]` may be the same header observation. The PHP plugin also examines server headers, errors and URL extensions, so inspect the match rather than assuming it measured a running interpreter. Likewise, an IIS version alone does not identify an exact Windows edition/build.

Use `--info-plugins=PHP` to inspect that plugin's description when relevant. Prefer the installed plugin's rules when a particular detection is ambiguous. Level 3 can make additional requests after a level-1 match; level 4 tries aggressive checks more widely. Escalating aggression changes the task's request footprint, not just output detail. Select a relevant plugin and permitted checks only if a specific unresolved question warrants them.

Sources: [upstream usage and aggression](https://github.com/urbanadventurer/WhatWeb/blob/master/README.md), [PHP detection rules](https://github.com/urbanadventurer/WhatWeb/blob/master/plugins/php.rb).
