# Discover paths using the same routing/session context

Establish the scoped URL prefix, correct hostname/TLS route, HTTP method and session state. Define `path_wordlist` as a bounded list of relevant names containing known positive and random-negative controls, and `url_template` as the exact URL with a single `FUZZ` replacement at the intended path position:

~~~bash
wfuzz -w "$path_wordlist" -t 2 -s 0.5 "$url_template"
~~~

Start without filters. Inspect status, redirect destinations and line/word/character counts for the controls. `--hl N` hides a line count, `--hh N` hides characters and `--hc 404` hides a status; they are presentation filters, not proof that every hidden response was irrelevant. A dynamic error can share a count with a genuine route. Apply only observed stable filters, recheck representative hidden responses, and preserve processed versus filtered totals. Authentication expiry can turn every candidate into the same login response.

`/FUZZ`, `/api/FUZZ` and a reviewed alias hypothesis such as `/assets../FUZZ` are different task-specific templates. Do not assume a candidate at one prefix exists at another, or sweep sensitive filenames without that scope. A parent directory's 403 does not rule out a readable child such as a selected `.git/HEAD`; confirm expected content rather than status alone. A route's 500 is a failure response and possible source/debug lead, not a valid successful API call. Follow a 301 only after checking its destination/method and scope. Keep the hostname and session context unchanged during individual confirmation.

Use the installed option contract for authentication/cookies and output captures; secrets should not enter reusable examples. Finish with the confirmed paths/responses, list/filter coverage and unresolved candidates. See [Wfuzz path and request examples](https://wfuzz.readthedocs.io/en/latest/user/basicusage.html) and [filter options](https://github.com/xmendez/wfuzz/blob/master/src/wfuzz/ui/console/clparser.py).
