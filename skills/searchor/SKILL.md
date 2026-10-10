---
name: searchor
description: Generate search-engine URLs with Searchor's CLI and inspect its local history. Use when a supported installed URL generator avoids custom URL construction, without assuming it retrieves search results.
---

# Generate a search URL

Read this entire file before acting. Verify the installed Searchor build and supported engine name. Finish with the generated URL and any local history or optional browser/clipboard effects; URL generation is not a completed web search.

The documented CLI is `searchor search ENGINE QUERY`. Inspect `searchor --help` and `searchor search --help`; engine names are case-sensitive identifiers in the reviewed implementation. With `engine` and `query` defined:

~~~bash
searchor search "$engine" "$query"
~~~

For example, `searchor search Google 'site:example.org incident response'` generates an engine URL. Keep a multiword query as one shell argument. Let the engine implementation perform its expected encoding; do not pre-encode without checking whether this would double-encode the query. The URL identifies the requested search, not the existence, relevance or trustworthiness of results.

Without `--open` or `--copy`, the reviewed 2.4.2 CLI still updates local history. It stores queries and URLs under the user's home directory in `.searchor-history.json`; avoid secrets in queries. `searchor history` reads that history, while `searchor history --clear` modifies it. A missing/unreadable history file or malformed JSON is a local-state failure, not evidence that the engine rejected the search.

`--open` asks the desktop browser to open the URL, and `--copy` uses clipboard integration. These can fail in a headless worker even when URL generation works. Preserve the URL output and separate those effects rather than replacing the generator with a custom browser workflow automatically.

Searchor 2.4.0 built an expression using `eval`; the reviewed 2.4.2 source uses an engine method directly. Check the installed build before passing untrusted input to an old version. A web application's displayed Searchor version is not proof that its deployed handler matches that source. If the engine is unknown, verify supported identifiers; do not automatically substitute a similarly named service.

See the [project](https://github.com/ArjunSharda/Searchor), [2.4.2 CLI](https://github.com/ArjunSharda/Searchor/blob/v2.4.2/src/searchor/main.py) and [history behavior](https://github.com/ArjunSharda/Searchor/blob/v2.4.2/src/searchor/history.py).
