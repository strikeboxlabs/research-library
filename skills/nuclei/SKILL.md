---
name: "nuclei"
description: "Run template-based checks against authorized live endpoints with Nuclei, filtered by severity and tags. Use for known-vulnerability and exposure detection at scale; a template match is a lead requiring confirmation, not a verified finding."
---

# Nuclei template scanning

Installed invocation: `/usr/bin/nuclei`, version `3.11.1` (Kali package nuclei).

Read this entire SKILL.md before acting. Require authorized live targets, current templates, and severity/tag selection deliberate enough to stay inside scope. Finish with results plus the template set and version used; unmatched templates are not evidence of absence.

Update templates before scanning so checks reflect current signatures, then run against a live-host list:

~~~bash
/usr/bin/nuclei -ut
/usr/bin/nuclei -l "$live" -severity high,critical -o "$findings"
~~~

`-rl` caps requests per second (default 150) and `-c` concurrency; some templates send intrusive payloads or fuzz — tag/severity filtering is a scope instrument, not only a noise filter. Default exclusions for known-bad hosts still apply per template configuration; the operator remains responsible for every request the engine makes.

A match reports that a template's detection condition held — version banners, response shapes and known-PATH probes all misfire on modified deployments. Confirm each finding with the affected component before reporting it as a vulnerability. Info-severity output is reconnaissance texture, not findings.

References: [project documentation](https://github.com/projectdiscovery/nuclei), [template docs](https://github.com/projectdiscovery/nuclei-templates).
