---
name: "subfinder"
description: "Passively enumerate subdomains for in-scope domains with Subfinder before any HTTP probing or scanning. Use when building the asset list a pipeline consumes; distinguish queried sources from verified-live hosts."
---

# Subfinder passive subdomain discovery

Installed invocation: `/usr/bin/subfinder`, version `2.17.0` (Kali package subfinder).

Read this entire SKILL.md before acting. Require one explicitly in-scope domain and a new output file before starting. Finish with the subdomain list on disk and an honest statement of which sources ran; passive enumeration output is names, not verified-live hosts.

Define `domain` as the authorized base domain and `out` as a new output path:

~~~bash
/usr/bin/subfinder -d "$domain" -silent -o "$out"
~~~

Without configured API keys most passive sources return nothing, so a short result usually reflects missing credentials, not an exhausted attack surface: check the non-silent output for source failures before concluding coverage. Many providers only unlock after keys are configured in subfinder's provider config file (`-config` to point at one explicitly). `-all` enables every source and is markedly slower; it is a breadth trade-off, not a completeness guarantee.

Output names have not been resolved or contacted. Feed the list to an HTTP prober (see the httpx skill) before treating anything as live, and confirm each finding is inside the authorized scope — subdomain sources include historical and third-party-hosted records that may be out of scope. A zero-result run is bounded by configured sources, not proof the domain has no subdomains.

References: [project documentation](https://github.com/projectdiscovery/subfinder).
