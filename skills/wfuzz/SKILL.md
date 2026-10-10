---
name: wfuzz
description: Use Wfuzz for controlled HTTP virtual-host and parameter comparisons. Use when wildcard responses, filters, paired payload counts or changing authentication state obscure real findings.
---

# Wfuzz HTTP comparison

Read this entire SKILL.md before acting; reuse complete current context. Establish the endpoint, negative/positive controls and bounded request set before filtering. Finish with confirmed response distinctions and completed coverage; a filtered display or status code alone does not prove a valid host, parameter or identity.

This procedure varies HTTP's Host header against one known server. It does not perform DNS discovery and does not prove that a discovered name has a public DNS record. Check the installed `wfuzz --help`; use a small relevant wordlist before increasing requests.

Define `target_ip` as the scoped numeric IPv4 server, `domain` as the intended DNS suffix, and `wordlist` as a local file of bare labels. Include a deliberately nonexistent label and a known valid label when available. Start **without result filters**:

~~~bash
wfuzz -w "$wordlist" -t 2 -s 0.5 -H "Host: FUZZ.$domain" "http://$target_ip/"
~~~

`FUZZ` marks the replacement location; a list of complete hostnames instead needs `Host: FUZZ`. Check both the destination and generated header. The example is plain HTTP. For HTTPS, an HTTP Host header alone does not change the TLS SNI hostname; first establish the correct TLS routing and certificate context.

Compare status, Location header, body and Wfuzz's line/word/character counts for the baseline and candidates. Default sites can return `200` for every name; reflected hostnames, dynamic tokens and timestamps can change body size without identifying a different application.

After observing stable negative responses, `--hh N` hides matching character counts and `--hw N` hides word counts. Do not copy the walkthrough's numeric threshold to a different page. Equal size does not establish equal content; keep a known positive control visible and recheck representative filtered responses. Avoid hiding every `403` merely to reduce output.

Confirm interesting names with individual requests using the same method, path, Host and authentication state. Record the response distinction and redirect destination before following it; another hostname may expand scope. Reduce concurrency/delay or stop on throttling, sustained errors or unreliable baselines. An empty filtered display describes this list and filter, not all possible virtual hosts.

For parameter-name discovery, `FUZZ` can appear in a query key (`?FUZZ=test`), not only its value. Establish a stable unknown-key response with the same session and method. For multiple inputs, `-z file,first -z file,second -m zip` pairs corresponding lines and stops when the **shorter** input ends; default product behavior generates combinations. Check expected versus completed request counts before claiming full coverage. `range,1000-9999` excludes values with leading zeros and does not cover all four-digit strings.

`--ss regex` selects responses matching an expression; `--hs` hides them. A match such as `dotnet` can come from an error or reflected input, so re-fetch the exact candidate. For a scoped numeric-ID search, bound the range deliberately. A PID range of 1–30000 neither covers every possible PID nor guarantees a stable process during the scan; absence from the filtered display is not proof that no matching process exists.

For form requests, preserve the actual content type, encoding, required cookie and CSRF state. Expired sessions, `429` responses or a changed negative baseline invalidate comparisons; stop and diagnose rather than changing source headers to evade limits. Keep secret request material out of reusable skill examples.

References: [usage and request controls](https://wfuzz.readthedocs.io/en/latest/user/basicusage.html), [filter/option parser](https://github.com/xmendez/wfuzz/blob/master/src/wfuzz/ui/console/clparser.py), [payload iterators](https://wfuzz.readthedocs.io/en/latest/user/advanced.html#iterators).
