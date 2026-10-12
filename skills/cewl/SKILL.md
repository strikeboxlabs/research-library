---
name: cewl
description: Collect words from selected website content for an authorised offline password audit. Use when crawl depth, word filters, case or mixed output could distort a site-specific candidate list.
---

# CeWL website wordlists

Read this entire SKILL.md before acting. Establish the selected site's crawl boundary and output format before collecting words. No conditional resources are required. Finish with crawl status, reviewed source content and the candidate-file format; a failed crawl or unverified response leaves collection incomplete.

Use CeWL when the relevant vocabulary comes from a known website. It collects words; it does not establish a username, recover a password or verify that a candidate works.

Check `cewl --help` for the installed options. Define `url` as one approved page with an explicit scheme, and `words` and `log` as fresh absolute output paths:

~~~bash
umask 077
cewl -d 0 -m 5 --with-numbers -w "$words" "$url" > "$log" 2>&1
~~~

`-d 0` limits collection to the starting page. If linked pages are needed, deliberately raise depth after checking scope. Depth is not a request budget or a URL-path boundary. Leave `--offsite` off for same-site collection; review redirects and the collected content before treating the output as in-scope evidence. CeWL does not enforce robots.txt as a crawl boundary.

Use `-w` for the candidate file: redirecting stdout alone also captures the startup banner. The example retains case and includes alphanumeric words of at least five characters. Lowering `-m` includes shorter terms; `--lowercase` changes candidate bytes. Neither choice reconstructs arbitrary concatenations or suffixes.

Inspect the log and a sample of the file before passing it to an offline checker. **Illustrative decisions:**

| Observation | Interpretation and next step |
|---|---|
| Expected short names are absent | Check minimum length and source content before increasing crawl depth. |
| Most words describe login or error pages | Verify which response was collected; a nonempty list does not prove access to the intended content. |
| Lines contain `word, 14` | `--count` produced frequency records; regenerate without it for a plain wordlist. |
| Browser-visible terms are absent | Browser JavaScript may generate them; CeWL does not render the page as a browser does. |

Keep email/metadata extraction separate when using those options; their headers and records are not ordinary word candidates. An interrupted or failed crawl establishes only partial coverage. A completed crawl still says nothing about candidate acceptance or exhaustion of possible passwords.

For option differences, use the [project documentation](https://digi.ninja/projects/cewl.php) and [upstream implementation](https://github.com/digininja/CeWL/blob/master/cewl.rb). CeWL 6.3.1 disables HTTPS peer verification; an HTTPS URL alone does not establish an authenticated source. Resolve transport trust before using protected content or credentials.
