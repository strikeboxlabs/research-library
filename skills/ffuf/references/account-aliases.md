# Compare CMS account aliases without equating 403 with a valid login

Use for an authorized comparison of a known CMS profile-route pattern. Backdrop's documented default account alias pattern is `accounts/[user:name]`, but deployments can change it, sanitize names, retain older aliases or omit generation. Query routing such as `/?q=accounts/name` works without a clean-URL rewrite; it is not itself an alias or an authentication bypass.

Require a scoped `base_url`, bounded `usernames` file containing reviewed URL-safe name candidates and known absent/positive controls where available. Start without a status filter:

~~~bash
ffuf -w "$usernames:FUZZ" -u "$base_url/?q=accounts/FUZZ" \
  -mc all -t 2 -rate 5 -timeout 10 -maxtime 120 -of json -o "$results"
~~~

Quote the URL so its query remains one argument. Arbitrary input containing spaces, &, #, % or slashes needs deliberate encoding/path handling rather than assuming ffuf is a URI-component serializer. Keep redirect following off and inspect status/body/Location for the actual session. Log an interrupted/error/throttled run as incomplete.

In a deployment where known profiles consistently produce an access-denied page and absent names produce a different 404, a selected follow-up may use `-mc 403` with a fresh result file and the same controls. `-v` adds verbose result/redirect display and `-c` colors output; neither strengthens the username conclusion. The source's identical-size 403 hits were useful candidates, not the enumeration of every account or proof of passwords/admin roles.

A blanket WAF/access rule or wildcard alias can make every name return 403. Calibration and filters can also hide useful differences. Inspect representative bodies and absent controls before claiming the response is tied to account existence. A redirect may be login routing rather than success, and a sanitized alias need not equal the exact login name.

The route comparison is a GET, distinct from repeatedly attempting logins. It can still consume server resources; if throttling/timeouts appear, narrow the list/rate and preserve partial coverage. Passing an account candidate to an explicitly authorized selected credential test is a later decision; do not turn the result file into an automatic password sweep.

See [ffuf options](https://github.com/ffuf/ffuf#usage), [Backdrop alias patterns](https://docs.backdropcms.org/documentation/url-aliases) and [clean URL routing](https://docs.backdropcms.org/documentation/clean-urls).
