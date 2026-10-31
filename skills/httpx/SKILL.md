---
name: "httpx"
description: "Probe a subdomain list for live HTTP services with ProjectDiscovery httpx, capturing status, title and technology per host. Use to turn name lists into verified-live endpoints; not the unrelated python3-httpx client CLI."
---

# httpx HTTP probing at scale

Installed invocation: `/usr/bin/httpx-toolkit`, version `1.9.0` (Kali package httpx-toolkit). The skill name `httpx` refers to ProjectDiscovery's prober; the image also has python3-httpx's client CLI at `/usr/bin/httpx`, which is a different tool — invoke the prober by its absolute path.

Read this entire SKILL.md before acting. Require an input host list from an authorized enumeration and a new output file. Finish with live endpoints plus what was probed and what failed; an unresponsive host is a failed probe, not evidence the service is absent.

Define `hosts` as the input list file and `live` as a new output path:

~~~bash
/usr/bin/httpx-toolkit -l "$hosts" -silent -sc -title -td -o "$live"
~~~

Both HTTP and HTTPS are attempted per host, so one live name can yield two lines. `-fr` follows redirects and changes what the reported status and title describe — the final hop, not the original endpoint; probe without it first when redirect chains themselves matter. Respect target rate constraints with `-rl` (requests per second) on large lists.

Title, status and `-td` technology hints are fingerprints, not confirmations. Technology guesses in particular misfire on customized stacks; verify a claimed component before reporting it. Output lines are live endpoints suitable for crawling (katana, hakrawler) or template scanning (nuclei).

References: [project documentation](https://github.com/projectdiscovery/httpx).
