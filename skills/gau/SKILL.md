---
name: "gau"
description: "Fetch known URLs for a domain from wayback, commoncrawl, otx and urlscan providers with gau, with match/filter and date-window controls. Use as the multi-provider historical-URL stage; historical presence is not current presence."
---

# gau multi-provider URL fetch

Installed invocation: `/usr/local/bin/gau` (Go install github.com/lc/gau/v2; providers wayback, commoncrawl, otx, urlscan).

Read this entire SKILL.md before acting. Require an in-scope domain and a new output file. Finish with the URL set and the provider list actually queried; each provider is a separate archive with separate gaps.

Define `domain` as the authorized domain and `out` as a new output path:

~~~bash
/usr/local/bin/gau --providers wayback,commoncrawl,otx,urlscan --threads 5 --subs "$domain" --o "$out"
~~~

`--o` (double dash) names the output file; single-dash `-o` is rejected. `--threads` defaults to 1 and is impractically slow for multi-provider pulls — raise it deliberately. A startup warning about a missing `~/.gau.toml` is benign: defaults apply and the file is only needed to change them. `--subs` includes subdomains (scope check applies); `--from`/`--to` bound the collection window (YYYYMM); `--fp` collapses parameter variants of one endpoint; `--mc`/`--fc` and `--mt`/`--ft` filter by status code and MIME type on providers that recorded them.

Provider archives overlap unevenly: a domain rich in one archive can be absent from another, so per-provider absence is coverage, not evidence. Verify liveness before deeper testing and confirm scope on every returned host. Complements waybackurls for single-archive quick pulls.

References: [project documentation](https://github.com/lc/gau).
