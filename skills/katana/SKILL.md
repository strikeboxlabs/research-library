---
name: "katana"
description: "Crawl live web endpoints with Katana at a chosen depth, including JavaScript and known files, emitting discovered URLs for downstream tools. Use when endpoint discovery on in-scope hosts feeds fuzzing or template scanning."
---

# Katana crawling

Installed invocation: `/usr/bin/katana`, version `1.8.0` (Kali package katana).

Read this entire SKILL.md before acting. Require one authorized live base URL and a deliberate depth. Finish with the discovered URL set and the boundaries actually crawled; a completed depth bound is not a claim that every endpoint was reached.

Define `base` as the in-scope live URL and `urls` as a new output path:

~~~bash
/usr/bin/katana -u "$base" -d 3 -fs '(^|\.)envo-it\.dk$' -kf robotstxt,sitemapxml -silent -o "$urls"
~~~

`-fs` restricts crawling to a field scope (`dn`, `rdn`, `fqdn` or a custom regex as shown) — set it explicitly to the authorized scope. Do not rely on the default alone: in a verified live run with defaults, off-site hosts referenced by the target (vendor consoles, documentation CDNs) appeared in the output — only about one in eight returned URLs was actually in scope. Treat the same filter as a mandatory post-step as well: match every output URL against the authorized domain before feeding anything downstream.

`-d` sets maximum depth (default 3); `-kf robotstxt,sitemapxml` adds the standard known files, and the help notes a minimum depth of 3 is needed for all known-file crawling to complete. `-jc` extends crawling into JavaScript-referenced endpoints, multiplying requests — make that an explicit choice under the target's load tolerance.

Output URLs pipe directly into nuclei or the ffuf skill for path-targeted work, after the scope filter.

References: [project documentation](https://github.com/projectdiscovery/katana).
