---
name: ffuf
description: Compare HTTP paths or virtual hosts with ffuf using measured baselines and bounded requests. Use when wildcard responses, extension expansion or combined filters hide useful results.
---

# ffuf response comparison

Check `ffuf -V` and `ffuf -h`; inspect any automatically loaded ffufrc for inherited headers, proxies or filters. Define `base_url` as the scoped scheme/authority without a trailing slash, `wordlist` as a small file of path candidates, and `results` as a fresh JSON output path. Start without filters:

~~~bash
ffuf -w "$wordlist:FUZZ" -u "$base_url/FUZZ" -mc all -t 2 -rate 5 -timeout 10 -maxtime 120 -of json -o "$results"
~~~

Include a known absent path and, when available, a known positive. Compare status, body, redirect, bytes, words and lines. A `200` can be a fallback page; a `401` or `403` can identify a distinct protected application. Inspect representative responses individually before excluding them.

For HTTP virtual hosts, define `target_ip` and `domain`, use bare labels in the list, and replace the URL with `http://$target_ip/` plus `-H "Host: FUZZ.$domain"`. This tests server routing, not DNS existence. HTTPS additionally needs correct TLS SNI/certificate routing; changing Host alone does not change SNI, and `-sni` does not accept a fuzz keyword.

Only after measuring stable negatives, add appropriate `-fs` byte, `-fw` word or `-fl` line filters. Their default combination is **OR**: any matching filter hides a response. Use `-fmode and` only when all selected dimensions must match. Reflected hostnames may vary bytes while leaving word count stable. Recheck positives after filtering; `-ac` is a calibration heuristic, not proof of coverage.

`-e .php,.txt` expands extension candidates at `FUZZ`; include the dots and account for the increased requests. A custom keyword must match its `-w file:KEYWORD` declaration. Leave recursion/redirect following off until destinations and budget are understood. A time limit, errors or throttling leave an incomplete scan; JSON contains selected results, not proof every candidate was tested.

Documentation reviewed 2026-10-09; Linux execution untested. Cases: Alert pp. 3–5; Analysis p. 4. Source: [upstream options and examples](https://github.com/ffuf/ffuf#usage).
