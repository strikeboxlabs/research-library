# API request construction

Establish the exact route, method, authentication and request schema. An application's signup endpoint may accept JSON while its login endpoint accepts form data. Similar names do not imply identical formats. Prefer the application's available OpenAPI schema over guessing fields or repeatedly sending malformed writes.

For an intended JSON request, define `url`, `method` (such as `POST` or `PUT`), `request_json` as the reviewed UTF-8 JSON file, `auth_headers` as a private file containing the required `Authorization: Bearer ...` header, and `headers`/`body` as fresh private response files:

~~~bash
umask 077
curl --silent --show-error --connect-timeout 5 --max-time 30 --request "$method" --header "@$auth_headers" --header 'Content-Type: application/json' --data-binary "@$request_json" --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\n' "$url"
~~~

Omit the authentication-header option for an unauthenticated endpoint. Construct JSON with a serializer; replacing quotes and newlines manually can corrupt backslashes, control characters and embedded text. `--data-binary @file` preserves the file's bytes; `--data @file` strips carriage returns, newlines and NULs. On supporting versions, `--json` supplies JSON headers but does not validate JSON.

For a documented form login, define `login_url`, the known `username` and a private `password_file` containing the exact password bytes without an accidental trailing newline. Choose fresh response files:

~~~bash
curl --silent --show-error --connect-timeout 5 --max-time 30 --data-urlencode "username=$username" --data-urlencode "password@$password_file" --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\n' "$login_url"
~~~

This selects POST with form encoding; do not add a JSON Content-Type. Check curl's exit status, HTTP status and response body before parsing a token. Keep token-bearing files private; avoid verbose traces that retain credentials.

A bearer token is not automatically a cookie. A protected documentation page and its OpenAPI document are separate requests that may each need authentication. An account-role change need not update an already issued token: distinguish current server-side state from claims captured at issuance, and reauthenticate when testing that distinction.

`405` can identify a route with the wrong method; inspect Allow/schema evidence. `422` in these FastAPI cases identifies request validation failure, not proof that the guessed operation is safe or correctly authorized. A success-looking response field does not establish the resulting state. After an ambiguous mutating response, inspect state before retrying. Review redirect destinations before forwarding authentication.

Documentation reviewed 2026-10-09; Linux execution untested. Cases: Backend pp. 4–10, 14–16; BackendTwo pp. 5–16. Sources: [curl options](https://curl.se/docs/manpage.html), [FastAPI form data](https://fastapi.tiangolo.com/tutorial/request-forms/).
