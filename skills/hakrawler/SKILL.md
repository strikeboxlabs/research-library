---
name: "hakrawler"
description: "Crawl a small set of live URLs from stdin with Hakrawler, attributing each discovered URL to its source element. Use for quick endpoint and form discovery where a lightweight crawler fits better than a full pipeline stage."
---

# Hakrawler lightweight crawling

Installed invocation: `/usr/bin/hakrawler`, version `2.1` (Kali package hakrawler).

Read this entire SKILL.md before acting. Require authorized live URLs on stdin and a deliberate depth. Finish with discovered endpoints and their source attribution; the crawler reports what pages exposed, not what exists.

Define `base` as the in-scope live URL and `out` as a new output path:

~~~bash
echo "$base" | /usr/bin/hakrawler -d 2 -s > "$out"
~~~

URLs are read from stdin, so it chains directly after probers or historical-URL tools. `-d` is depth (default 2); `-s` annotates each URL with where it was found (href, form, script), which separates attacker-reachable links from framework plumbing faster than raw lists. `-subs` includes subdomains of the input — a scope widening that needs the same authorization as the base host.

A URL that answers with a redirect produces silent emptiness: hakrawler prints nothing and exits when the root redirects (verified live — a 301-ing `www.` host yielded zero output while the redirect target crawled normally). Resolve the final URL first with the prober's result or a HEAD request before piping it in, and never read silence from a redirecting root as an empty surface.

`-h "Header: value;;Second: v"` supplies session headers when content hides behind authentication; treat authenticated crawling results as tenant-specific, not public surface. `-size` caps page size and `-timeout` bounds each fetch.

References: [project documentation](https://github.com/hakluke/hakrawler).
