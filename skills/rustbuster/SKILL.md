---
name: rustbuster
description: Discover web paths, DNS names or virtual hosts with Rustbuster. Use when an installed Rustbuster fits the task and status/body filters or the distinction between DNS and Host-header discovery matter.
---

# Choose the discovery surface

Read this entire file before acting. For virtual-host or custom request fuzzing, read [request modes](references/request-modes.md) fully. Finish with reproducible candidate responses and the filters, wordlist and surface tested; discovery output is a lead, not proof of a vulnerability.

Rustbuster is a web fuzzer, distinct from RustScan. Check `rustbuster --version` and the selected subcommand's `--help`; its modes have different options.

| Need | Mode |
|---|---|
| Paths beneath one URL | `dir` |
| DNS A/AAAA names beneath a domain | `dns` |
| HTTP Host-header routing on one endpoint | `vhost` |
| A marker in a URL/header/body | `fuzz` |

Set `base_url` to the authorized origin/path ending in `/`, `wordlist` to reviewed relative path candidates and `results` to a fresh file:

~~~bash
rustbuster dir -u "$base_url" -w "$wordlist" -t 5 -o "$results"
~~~

Test a known path and a deliberately nonexistent path first. If both return the same login page or HTTP 200 body, a status-only scan cannot distinguish them. Keep redirects and authorization responses as leads; a 403 can identify a real path. `-S` excludes status codes, `-s` includes them, and `-e php` adds extension candidates when the application evidence warrants it. `-f` adds slash variants; this changes request count and routing. Verify the installed mode's filter precedence rather than combining contradictory filters.

`-t` is concurrency, not a total time limit. `-K` stops on connection errors when continuing would produce misleading coverage. Do not use `-k` just to suppress a TLS problem: supply the correct trusted endpoint or document why certificate verification cannot yet succeed. Save transport failures separately from negative path results.

For DNS discovery, define the authorized `domain` and use `rustbuster dns -d "$domain" -w "$wordlist" -t 5`. Compare against a random nonexistent label to detect wildcard DNS. DNS resolution neither proves an HTTP virtual host exists nor finds hosts configured only in HTTP routing.

See [upstream mode help](https://github.com/phra/rustbuster#usage).
