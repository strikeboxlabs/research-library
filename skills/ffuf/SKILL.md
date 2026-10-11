---
name: ffuf
description: Compare HTTP paths or virtual hosts with ffuf using measured baselines and bounded requests. Use when wildcard responses, extension expansion or combined filters hide useful results.
---

# ffuf response comparison

Read this entire SKILL.md before acting; reuse complete current context. For new requests, select a bounded candidate set and controls before filtering. For an acquired result, use the saved-format guidance below without making another request. For username candidates derived from CMS profile aliases, read [account alias comparisons](references/account-aliases.md) fully before that procedure. Finish with confirmed response differences or the supported saved-result interpretation, retaining completed versus interrupted coverage; a result list alone does not establish route validity.

Check `ffuf -V` and `ffuf -h`; inspect any automatically loaded ffufrc for inherited headers, proxies or filters. Define `base_url` as the scoped scheme/authority without a trailing slash, `wordlist` as a small file of path candidates, and `results` as a fresh JSON output path. Start without filters:

~~~bash
ffuf -w "$wordlist:FUZZ" -u "$base_url/FUZZ" -mc all -t 2 -rate 5 -timeout 10 -maxtime 120 -of json -o "$results"
~~~

Include a known absent path and, when available, a known positive. Compare status, body, redirect, bytes, words and lines. A `200` can be a fallback page; a `401` or `403` can identify a distinct protected application. Inspect representative responses individually before excluding them.

Use an observed framework clue to narrow the next wordlist: a Spring-style error page can justify selected framework paths, but does not establish an exact version or that every management endpoint exists. Reuse the same controls and request budget. If an endpoint returns a discovery map, inspect its advertised paths/methods before expanding another scan. `-ic` ignores wordlist comments; it does not validate, deduplicate or authorize the remaining candidates.

For a specifically scoped API method test, `-X POST` changes the method; even an empty POST can mutate state. A FastAPI `422` may reveal a route needing fields or a different encoding. A `405` is a method clue, so copying a `-fc 404,405` filter can hide valid paths. Retain method/body/authentication context and prefer a known OpenAPI schema to blind method expansion.

For HTTP virtual hosts, define `target_ip` and `domain`, use bare labels in the list, and replace the URL with `http://$target_ip/` plus `-H "Host: FUZZ.$domain"`. This tests server routing, not DNS existence. HTTPS additionally needs correct TLS SNI/certificate routing; changing Host alone does not change SNI, and `-sni` does not accept a fuzz keyword.

Only after measuring stable negatives, add appropriate `-fs` byte, `-fw` word or `-fl` line filters. Their default combination is **OR**: any matching filter hides a response. Use `-fmode and` only when all selected dimensions must match. Reflected hostnames may vary bytes while leaving word count stable. Recheck positives after filtering; `-ac` is a calibration heuristic, not proof of coverage.

`-e .php,.txt` expands extension candidates at `FUZZ`; include the dots and account for the increased requests. A custom keyword must match its `-w file:KEYWORD` declaration. In the reviewed v2.0.0 normal wordlist mode, extension expansion is specifically tied to the `FUZZ` keyword: a consistent custom `FFUZ` still substitutes candidates, but `-e` does not expand that input. The extension is appended literally, so `txt` would produce `nametxt`, not `name.txt`, for the expanding keyword. Use the default keyword plus dotted extensions when that is the intended task; dirsearch compatibility mode is a separate expansion contract. See the [versioned wordlist expansion](https://github.com/ffuf/ffuf/blob/v2.0.0/pkg/input/wordlist.go) if a scan silently omits expected variants. Leave recursion/redirect following off until destinations and budget are understood. A time limit, errors or throttling leave an incomplete scan; JSON contains selected results, not proof every candidate was tested.

Reference: [upstream options and examples](https://github.com/ffuf/ffuf#usage).

Read a saved `-of json -o` result as the actual JSON document, regardless of a `.txt` suffix. This differs from `-json` stdout's newline-delimited records on releases supporting that option. Verify format/root/results fields and preserve parse errors; processing each line as a complete object or retaining only the last line can lose evidence. Neither successful JSON parsing nor extracted href strings proves completed scan coverage or authorizes another request.
