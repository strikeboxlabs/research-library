---
name: dirsearch
description: Discover web paths with dirsearch and distinguish real findings from wildcard pages, redirects and authentication responses. Use for scoped web-content enumeration with a supplied wordlist.
---

# Dirsearch path discovery

Read this entire SKILL.md before acting. Require the scoped URL/virtual host, existing selected wordlist and measured response controls before discovery; all task instructions are inline. Finish with completed versus interrupted coverage and individually confirmed response differences. If the list, intended host or authorization is missing, retain that prerequisite rather than expanding another target.

Confirm the intended virtual host and URL prefix first. An IP URL can reach the wrong site; for HTTPS, an HTTP Host header alone does not necessarily select the right TLS virtual host. Inspect one real page and a deliberately nonexistent path to establish status, redirect and body behaviour.

Define `url` as the in-scope base URL, `wordlist` as an existing local list, and `report` as a fresh output path. Check the installed `dirsearch --help`; source checkouts may use `python3 dirsearch.py`. For a PHP site and a list of bare path stems:

~~~bash
dirsearch -u "$url" -w "$wordlist" -e php -f -t 4 --max-rate 5 -o "$report"
~~~

These are conservative starting concurrency/rate values, not performance requirements. `-e php` normally replaces `%EXT%` markers; `-f` also expands plain entries. Omit forced expansion when the list already contains the exact filenames wanted. Do not assume the distro includes the walkthrough's wordlist.

Inspect the active configuration and startup summary: settings files can alter defaults. Start without recursion or redirect following; add them for selected in-scope paths only. A redirect to another hostname is a finding to assess before expanding the target.

Compare interesting responses with the nonexistent-path baseline. A `200` may be a soft 404; repeated `302` responses may all reach login. `401`/`403` are useful access-control observations and should not automatically be discarded. Use size/text/redirect filters only after checking representative bodies. Slow down or stop on sustained `429`, timeouts or server errors; they make coverage incomplete.

Re-request promising paths with the same method/session and retain URL, status, redirect destination and relevant body evidence. A browser's authenticated response can differ from the scan. A parent path returning `403` may still contain readable child files; test relevant filenames or a selected subdirectory instead of assuming the entire tree is blocked. Discovery of an admin page does not establish access. An empty report is limited by the wordlist, extensions, authentication and filters used.

## Use partial-name evidence to narrow discovery

An IIS short alias such as the **illustrative** `TRANSF~1.ASP` constrains candidates without revealing the full filename or distinguishing `.asp` from `.aspx`. Select plausible stems from a local wordlist using that prefix and the observed framework; inspect the reduced list before scanning. For an ASP.NET hypothesis, define `candidates` as that small stem list and `candidate_report` as a fresh output path:

~~~bash
dirsearch -u "$url" -w "$candidates" -e aspx -f -t 1 --max-rate 2 -o "$candidate_report"
~~~

If candidates already contain complete filenames, omit extension forcing. Older dirsearch examples may expand entries differently; verify the installed help instead of assuming `-e` expands every bare stem. A redirect can reveal a canonical directory spelling, but the short alias alone cannot. Recheck promising full URLs and bodies before claiming the guessed filename exists.

Output-format switches differ across releases; check local help before requesting a particular format. See [upstream usage](https://github.com/maurosoria/dirsearch/blob/master/docs/usage.md) and the [option parser](https://github.com/maurosoria/dirsearch/blob/master/lib/parse/cmdline.py) for expansion and version differences.
