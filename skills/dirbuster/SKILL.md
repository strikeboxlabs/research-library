---
name: dirbuster
description: Discover selected web directories and extensionless or suffixed files with DirBuster's headless CLI. Use an explicit wordlist and bounded recursion/concurrency, then separate real routes from fallback responses and incomplete scans.
---

# DirBuster without the GUI

Read this entire SKILL.md before acting. Select the authorized base URL, starting path and readable wordlist before requests; constrain recursion and HTML parsing to the intended scope. Finish with the saved report, completion/errors and individually confirmed routes. A found name or HTTP 200 alone is not proof of the route's purpose.

Use the existing `dirbuster` launcher and inspect `dirbuster -h`. The 1.0-RC1 CLI supports `-H` for headless operation; no display is needed for this branch. Some original shell launchers ignore arguments; a wrapper that does not forward them is a deployment problem, not absence of headless support. If necessary use the verified installed Java/JAR invocation, without guessing their locations or installing a runtime.

Define `base_url` as the exact scoped origin including its port, `start_path` as an approved path such as `/`, `wordlist` as a selected existing list, `threads` as the allowed positive concurrency, and `report` as a fresh absolute path in a private task directory:

~~~bash
umask 077
dirbuster -H -u "$base_url" -l "$wordlist" -s "$start_path" \
  -t "$threads" -g -P -R -r "$report"
~~~

`-g` chooses GET requests; `-P` disables HTML-derived paths and `-R` disables recursion. These reduce automatic expansion but do not make enumeration passive. Threads control concurrent connections, not a packets/requests-per-second limit. Use the task's total runtime budget; preserve interruption/errors rather than claiming complete coverage. The headless help documents automatic report saving on exit: inspect that the report actually exists and distinguish normal completion from forced termination.

For a selected suffix list, add `-e "$extensions"`, for example `extensions=php,txt`. The reviewed CLI defaults to `php`; do not infer from this default that the application uses PHP, or that an extensionless route cannot be found. Check the effective build/report for extensionless candidates such as `/feed` and `/upload`; do not invent an empty-extension spelling if the installed help does not establish it. A small task-specific wordlist containing independently supported candidate names can be more useful than a huge generic list. An empty result covers only the tested list, suffixes, start path and completed portion.

Compare an ordinary known route and one unique nonexistent path before interpreting hits. A fallback/login page can return the same 200, size or redirect for both. Request each selected hit separately with the expected hostname, port, cookies and method and retain its body/status. An XML upload form is a lead to inspect its field names and accepted document schema, not proof of unsafe XML parsing. A large `/feed` body is content evidence, not a file or deserialization finding by itself.

If the selected task requires recursive or HTML-derived discovery, deliberately omit `-R` or `-P` after checking the resulting request scope. Do not silently expand a scan to make the report longer. A GUI thread count, estimated remaining time or stopped status does not establish the headless command's settings or completed coverage.

Resolve launcher and option differences with the [distribution CLI help](https://www.kali.org/tools/dirbuster/) and [argument-forwarding patch](https://gitlab.com/kalilinux/packages/dirbuster/-/blob/kali/master/debian/patches/allow-commandline-argument.patch). These establish a supported CLI adaptation; the controlled image's executable paths remain its own facts.
