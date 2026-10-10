---
name: gobuster
description: Discover selected web paths or HTTP virtual hosts with Gobuster and interpret wildcard, redirect and access-control responses. Use when choosing enumeration mode, wordlist/extension expansion and filters for a scoped web application.
---

# Gobuster web paths

Read this entire SKILL.md before acting; reuse complete current context. Establish mode, route and response controls before choosing filters. Finish with confirmed response differences and completed request scope; interrupted or filtered output cannot establish absent paths.

For HTTP virtual-host candidates, read [virtual-host selection](references/virtual-hosts.md) fully before that procedure.

Choose the mode deliberately: `dir` probes URL paths, `vhost` varies HTTP hostnames, and `dns` queries DNS. Their wordlists and switches are not interchangeable. Check `gobuster version` and `gobuster dir --help` for the installed release.

Establish the correct virtual host, application prefix and authentication context. Request a known page and several nonexistent paths to identify wildcard/default responses. Define `url` as the in-scope base URL, `wordlist` as a relevant local file, and `report` as a new output path. For a PHP application and bare filename stems:

~~~bash
gobuster dir -u "$url" -w "$wordlist" -x php,txt -t 4 --delay 250ms -o "$report"
~~~

Extensions increase requests; omit `-x` when exact filenames are already supplied. Delay is per worker, not a global requests-per-second limit. Start with a short candidate list and observe actual service behaviour. Stop or slow down on throttling and repeated server errors.

If wildcard checks prevent scanning, inspect the negative response first. Use supported status/length filters only after comparison; forcing past the precheck does not fix false positives. Positive status lists and the default blacklist can conflict, so inspect local help before combining them. Do not treat a length filter as proof that hidden responses contain nothing useful. Blacklisting status 200 suppresses real 200 routes as well as a 200 catch-all; confirm interesting children directly before claiming that the filtered listing covers readable content.

Repeated timeouts under one prefix can reflect a proxy route or an upgrade endpoint. Inspect one request and available routing/client evidence before widening the list; a timeout alone proves neither a directory nor WebSocket support.

Keep redirects visible initially. A `302` to login is a discovered route with an authentication requirement, not successful access to its contents. Re-request an interesting result with the same session context; a browser's authenticated result may differ. A parent path returning `403` can still contain individually readable files. Selected child requests or a more specific prefix can be more useful than a much larger root wordlist.

For an explicitly scoped API method test, supported `dir --method POST` changes the method but does not construct the required body. Empty POSTs are not inherently read-only. A FastAPI `422` can be a validation clue; a `405` can identify a valid path with another method. Inspect before blacklisting either. Preserve the exact scheme and route: `/user` and `/users` are different paths, even when a walkthrough confuses them.

Retain URL, status, redirect and distinguishing body evidence. An empty report is bounded by mode, base path, wordlist, extensions, authentication, filters and completion state. For `vhost` work with bare labels, verify this version's `--append-domain` behaviour; finding an HTTP host is not evidence of DNS resolution.

References: [modes and release changes](https://github.com/OJ/gobuster), [directory filters](https://github.com/OJ/gobuster/blob/master/cli/dir/dir.go), [worker options](https://github.com/OJ/gobuster/blob/master/cli/options.go).
