# API request construction

Establish the exact route, method, authentication and request schema. An application's signup endpoint may accept JSON while its login endpoint accepts form data. Similar names do not imply identical formats. Prefer the application's available OpenAPI schema over guessing fields or repeatedly sending malformed writes.

For an intended JSON request, define `url`, `method` (such as `POST` or `PUT`), `request_json` as the reviewed UTF-8 JSON file, `auth_headers` as a private file containing the actual required authentication header (such as `Authorization: Bearer ...`, `x-access-token` or `x-api-key`), and `headers`/`body` as fresh private response files:

~~~bash
umask 077
curl --silent --show-error --connect-timeout 5 --max-time 30 --request "$method" --header "@$auth_headers" --header 'Content-Type: application/json' --data-binary "@$request_json" --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\n' "$url"
~~~

Omit the authentication-header option for an unauthenticated endpoint. Construct JSON with a serializer; replacing quotes and newlines manually can corrupt backslashes, control characters and embedded text. `--data-binary @file` preserves the file's bytes; `--data @file` strips carriage returns, newlines and NULs. On supporting versions, `--json` supplies JSON headers but does not validate JSON.

JSON `\uXXXX` sequences escape characters inside a string; they do not change the request body's transport encoding to UTF-16. Use UTF-8 for interoperable JSON exchange and inspect saved bytes when encoding matters. A Content-Type label alone neither converts nor validates those bytes. See [JSON strings and character encoding](https://www.rfc-editor.org/rfc/rfc8259#section-8.1).

For a documented form login, define `login_url`, the known `username` and a private `password_file` containing the exact password bytes without an accidental trailing newline. Choose fresh response files:

~~~bash
curl --silent --show-error --connect-timeout 5 --max-time 30 --data-urlencode "username=$username" --data-urlencode "password@$password_file" --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\n' "$login_url"
~~~

This selects POST with form encoding; do not add a JSON Content-Type. Curl URL-encodes the value once. If a verified backend requires an extra decoding layer, put exactly one pre-encoded value in a private field file and use `--data-urlencode "username@$field_file"`; percent signs are then encoded by the outer form pass. Compare captured wire bytes and controls before adding that pass: `%252A` becomes literal `%2A` after one form decode, whereas `%2A` becomes `*`. Ordinary credentials or base64 fields should not be pre-encoded by default. Check curl's exit status, HTTP status and response body before parsing a token. Keep token-bearing files private; avoid verbose traces that retain credentials.

For an observed endpoint requiring GET query fields, define `field_name` as its actual parameter name, `field_file` as the exact private value bytes and `url` as the endpoint; use `curl --get --data-urlencode "$field_name@$field_file"` with the same status/header/body capture. `--get` places these data options in the URL instead of their ordinary POST body. Curl encodes the value; the server still decides whether it is data or a command. Shell quoting does not authorize server execution. A harmless identity response can establish execution under that observed account; neither HTTP 200 nor a changed template alone establishes it. Query values can be retained in URL/log history, so select only the task's intended data/action.

A bearer token is not automatically a cookie. A protected documentation page and its OpenAPI document are separate requests that may each need authentication. An account-role change need not update an already issued token: distinguish current server-side state from claims captured at issuance, and reauthenticate when testing that distinction.

`405` can identify a route with the wrong method; inspect Allow/schema evidence. `422` in these FastAPI cases identifies request validation failure, not proof that the guessed operation is safe or correctly authorized. A success-looking response field does not establish the resulting state. After an ambiguous mutating response, inspect state before retrying. Review redirect destinations before forwarding authentication.


## Send a multipart file form

For an authorized upload, use the endpoint's actual field names, authentication and CSRF requirements. Define `url`, `file_field`, `upload_file` as a reviewed absolute local path, `note_field`/`note` as a documented text field/value, and fresh `headers`/`body` paths. This example assumes ordinary field names and a path without double quotes, commas, semicolons or newlines:

~~~bash
umask 077
curl --silent --show-error --connect-timeout 5 --max-time 30 \
  --form "$file_field=@$upload_file" --form-string "$note_field=$note" \
  --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\n' "$url"
~~~

`--form` constructs multipart POST data and its boundary; setting Content-Type alone does not build that body. `@` attaches file bytes, while `<` supplies a form value from a file without file-upload metadata. `--form-string` preserves text such as `@name` literally. Use curl's form-value quoting rules for more complex filenames; shell quotes alone do not disable curl's own form syntax.

A per-part `;type=...` only labels the content; it neither converts nor verifies the bytes. Do not combine this form body with a JSON header or `--upload-file` PUT. A UI error can coexist with a successful stored upload, and a 200 can contain an application error. Inspect the response and the selected object's state before retrying a write or claiming execution. Omit the text field when it is not part of the contract.

## Upload exact file bytes with HTTP PUT

For an authorized file replacement, define `upload_file` as the exact local file (without upload-glob metacharacters) and `url` as the complete destination URL including its filename. Use fresh `headers`/`body` response files and the endpoint's required authentication:

~~~bash
curl --silent --show-error --connect-timeout 5 --max-time 30 --upload-file "$upload_file" --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\n' "$url"
~~~

For HTTP(S), `--upload-file` selects PUT. A trailing-slash URL instead lets curl append the local filename. `-X PUT` changes the method word; it does not repair body transformations. In Bash, `"$(cat file)"` loses trailing newlines before curl sees the value. Use a file-based upload for exact bytes.

A zero curl exit or empty response body does not establish replacement. Inspect HTTP status and, when the endpoint supports it, retrieve the selected object to compare bytes. A timeout leaves the write outcome uncertain; inspect state before retrying. PUT can overwrite existing data, so choose the destination deliberately.

See [curl's upload/body options](https://curl.se/docs/manpage.html) and the [FastAPI form-data distinction](https://fastapi.tiangolo.com/tutorial/request-forms/).
