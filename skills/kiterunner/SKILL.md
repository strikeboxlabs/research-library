---
name: "kiterunner"
description: "Discover API routes with kiterunner's structured route wordlists and method-aware scanning, beyond path-based fuzzing. Use on API-heavy authorized targets where ffuf wordlists miss method+path combinations."
---

# kiterunner API route discovery

Installed invocation: `/usr/local/bin/kiterunner` (Go install github.com/assetnote/kiterunner/cmd/kiterunner).

Read this entire SKILL.md before acting. Require an authorized API base URL and a route wordlist appropriate to the target's framework. Finish with discovered routes including method, and the wordlist used.

~~~bash
/usr/local/bin/kiterunner scan https://$host/ -w "$routes" -x 20
~~~

kiterunner scans structured route files that encode method and path together (swagger-derived lists from the project's data releases), so a discovery includes `POST /api/v1/thing`, not just `/api/v1/thing` — the difference between route found and route callable. `-x` bounds concurrent connections; API gateways rate-limit aggressively, so start low and watch for 429 patterns as signal about the target's front line.

Routes answering non-404 status codes are leads: 405 (wrong method, route real), 401/403 (route real, protected) are discoveries even without content. Validate discovered routes individually before reporting them as attack surface; wordlists carry framework bias and stale guesses.

References: [project documentation](https://github.com/assetnote/kiterunner).
