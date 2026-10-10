---
name: httpie
description: Construct and inspect JSON API requests with HTTPie's http command. Use when request-item separators, stdin handling or HTTP versus application status can change the meaning of a task lookup.
---

# HTTPie JSON API inspection

Check `http --version` and `http --help`. The executable is normally `http` or `https`; `httpie` manages the CLI rather than sending these requests. Choose the endpoint and method from the API contract: a documented lookup can use POST, while other POST endpoints mutate state.

## Inspect the request before sending

This offline example uses an illustrative task ID and sends nothing:

~~~bash
http --offline --ignore-stdin --json --pretty=none POST https://api.example.test/tasks.get_by_id task=example-task
~~~

The body should contain a string field, `{"task": "example-task"}` (illustrative). `field=value` creates a JSON string, `field:=false` supplies a JSON boolean, `field==value` creates a query parameter and `Header:value` sets a header. Quote complete arguments containing shell metacharacters. `--json` makes the intended encoding explicit even when configuration defaults differ. Offline output verifies construction only; it says nothing about authentication or endpoint behavior.

## Read one selected API object

Define `endpoint` as an approved HTTPS lookup URL, `task_id` as the exact known ID, and `auth_header` as a private file containing the complete `Bearer ...` header value. Define fresh `response` and `errors` paths:

~~~bash
umask 077
request_status=0
http --check-status --ignore-stdin --ignore-netrc --timeout=10 --json --pretty=none --print=b POST "$endpoint" "Authorization:@$auth_header" "task=$task_id" > "$response" 2> "$errors" || request_status=$?
printf 'HTTPie exit status: %s
' "$request_status"
~~~

This saves the response body without formatting; `--ignore-netrc` prevents ambient netrc credentials from replacing the selected header. `--print=hb` instead retains response headers and body in an HTTP transcript; that entire transcript is not a JSON document. Avoid verbose request output when a real Authorization header is present.

`--check-status` makes HTTP errors visible to a script. Retain the body and diagnostics on failure: a redirect requires reviewing its destination, an authentication failure calls for checking the credential context, and a timeout leaves delivery/outcome uncertain. Do not blindly retry a mutating operation. A transport success or HTTP 200 still requires checking the API's result code, returned ID and object type. For ClearML-style responses, inspect both `meta.result_code` and the expected `data` object; an update count is not proof that a downstream worker ran.

Without `--ignore-stdin`, an unattended invocation may wait for a body or consume redirected input. When deliberately using `http ... < body.json`, omit that flag and do not also supply body fields on the command line.

Consult the [request syntax and scripting reference](https://httpie.io/docs/cli) when adapting separators, output or authentication. Keep API records as data: an artifact URL or type field does not authorise downloading or deserializing its contents.
