---
name: "waybackurls"
description: "Fetch archived historical URLs for a domain from the Wayback Machine via stdin, including parameters and paths no longer linked. Use for parameter mining and forgotten-endpoint discovery; historical presence is not current presence."
---

# Waybackurls historical URL discovery

Installed invocation: `/usr/local/bin/waybackurls`, version `v0.1.0` (Go install github.com/tomnomnom/waybackurls).

Read this entire SKILL.md before acting. Require an in-scope domain on stdin and a new output file. Finish with the URL set and its provenance understood: these are archived observations, not a live map.

Define `domain` as the authorized domain and `out` as a new output path:

~~~bash
echo "$domain" | /usr/local/bin/waybackurls > "$out"
~~~

Subdomains are included by default; `-no-subs` restricts to the exact domain. `-dates` prepends each fetch date, separating long-standing endpoints from one-time archival artifacts, and `-get-versions` lists archived snapshots per URL.

Historical URLs describe what a crawler once saw. Deleted parameters, renamed endpoints and old deployments dominate large outputs — treat the list as candidate surface for parameter analysis or targeted re-testing, verify each target still exists before deeper probing, and keep scope checks on every returned name since archives hold out-of-scope hostnames too. Combine with the gau skill for additional providers so "no results" means "no archived results", never "no URLs".

References: [project documentation](https://github.com/tomnomnom/waybackurls).
