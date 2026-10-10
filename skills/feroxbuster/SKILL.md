---
name: feroxbuster
description: Discover scoped web paths with Feroxbuster while controlling recursion, request rate and link extraction. Use when wildcard responses, parent paths, redirects or an interrupted scan need interpretation.
---

# Bounded web-path discovery

Define `url` as one approved base URL with the intended hostname and path, `wordlist` as a selected local list, and `report` as a fresh private output path. Check `feroxbuster --version` and `--help`: options and automatic link extraction differ across releases. Review loaded configuration and startup settings for inherited headers, proxies, methods, extensions and collection features.

~~~bash
umask 077
feroxbuster --url "$url" --wordlist "$wordlist" --threads 4 --scan-limit 1 --rate-limit 5 --time-limit 2m --no-recursion --dont-extract-links --json --output "$report"
~~~

This limits the run to one active directory scan, five requests/second per directory and two minutes. `--threads` controls concurrent work within a scan; it is not a request-rate setting. `--no-recursion` and `--dont-extract-links` control different expansions. Avoid inheriting `--smart`/`--thorough` collection behavior when assessing this bounded run. Do not substitute `--depth 0`: zero means unlimited recursion. For an approved recursive follow-up, choose a finite depth and account for per-directory limits across concurrent scans.

Before filtering, compare a known path and a deliberately nonexistent path under the same hostname, method and authentication context. A wildcard response can resemble a real hit. Add size/status filters only after measuring the baseline, and retain the settings: both explicit filters and automatic wildcard filtering can hide useful responses. A blank report does not establish that no content exists.

**Illustrative observations and next decisions:**

| Observation | Interpretation and next check |
|---|---|
| Many `/content/WEB-INF/...` paths return identical 404 bodies | Likely generic handling. Verify the parent `/content/` separately; a missing child does not establish that its parent is absent. |
| `/assets/` returns 403 while an observed CSS/JS child returns 200 | Directory listing may be disabled while individual files are served. Verify that known child under the same session; do not interpret the parent as wholly inaccessible or infer a traversal flaw. |
| A parent redirects to a login page | An application route may exist; this does not establish access. Inspect the Location and scope before enabling `--redirects`. |
| A selected path gives 500 | Preserve the specific response and compare a control path; the status alone proves neither content disclosure nor code execution. |
| Timeout, 429 or repeated connection failures | Reduce load or stop and resolve transport/rate restrictions; a truncated scan has incomplete coverage. |

Aiohttp, for example, returns 403 for static directories by default unless directory indexes are enabled; see its [static-file behavior](https://docs.aiohttp.org/en/stable/web_advanced.html#static-file-handling). A route prefix and a version banner do not establish the backing filesystem path or configuration. Check the deployed route/options before attributing a version-specific file-access vulnerability.

For private CAs, use the installed version's `--server-certs` support. `--insecure` disables TLS verification; it does not repair DNS, SNI or a wrong virtual host. Record any deliberate use when interpreting results.

Retain the complete JSON output plus effective settings and completion status; JSON entries can include more than discovered URLs. If resuming, inspect the saved state's target/configuration before `feroxbuster --resume-from "$state"`; a state file is not a URL list and resume does not establish that scope or credentials are still valid.

Resolve version differences against the [CLI reference](https://epi052.github.io/feroxbuster-docs/configuration/command-line/) and [upstream option definitions](https://github.com/epi052/feroxbuster/blob/main/src/parser.rs).
