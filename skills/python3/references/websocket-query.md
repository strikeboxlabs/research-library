# Bridge a verified application message to a bounded SQL test

Use this for an authorized SQL-injection assessment when the input/result travels through a native WebSocket rather than an HTTP form. Read [the WebSocket exchange](websocket-exchange.md) fully for its existing-library, greeting/token, heartbeat and bounded receive prerequisites. Use that connection/receive logic only when the observed protocol matches; Socket.IO requires its matching client/framing instead.

First reproduce a legitimate application request and retain its result. Identify the message field, scalar/array input, current token and response type carrying the result. Use JSON serialization to encode the request; do not interpolate SQL text into raw JSON. A stale token, malformed envelope or a transport close is not a negative SQL result.

For an observed numeric `params` input where the assessment permits testing, compare the known available/unavailable values with a single condition variation. Hold the URL, message type, session and schema constant. A changed application response is a lead; repeat with a discriminating false condition/control before treating it as database evaluation. An ordinary available record is not proof all injected conditions executed.

Once the actual query shape confirms a two-column UNION and a returned second expression, a bounded metadata request can look like this **illustrative, schema-specific** Python message construction:

~~~python
payload = "1 UNION SELECT 1, VERSION() ORDER BY name DESC; -- -"
ws.send(json.dumps({"token": token, "message": "available", "params": payload}))
reply = receive_object()
debug = reply.get("debug")
if not isinstance(debug, str):
    raise ValueError("Expected result field absent; SQL result is unresolved")
~~~

Here `ws`, `token`, `json` and `receive_object` come from the selected verified exchange. `available`, two columns, a string params field and the `name` ordering expression must come from this application's evidence; they are not universal. When adapting this branch, replace the help request in that exchange rather than blindly sending both, and update the token from intervening responses only according to the observed contract. SQL comment/quoting rules and union column types still need to match the identified database.

Treat `debug` as an application serialization boundary. Parse its documented format, or preserve a bounded private raw reply while resolving it. Splitting on `name: ` and the first `]` can truncate brackets/newlines in a result or select the legitimate row instead of the injected one. A default subscription name is not database success. Vary sorting only when the observed query requires it, and confirm the returned marker/scalar rather than assuming whichever row was displayed was the injected one.

For scoped schema/table inspection, keep database and table conditions explicit. Prefer separate bounded rows over comma-joined `GROUP_CONCAT`: commas in values, NULL expressions and the aggregate length cap can lose entries. An outer LIMIT on an aggregate does not cap its internal entries. Report truncation/unknown completeness instead of calling the result a full dump.

If a selected server-side file read is authorized, `LOAD_FILE(absolute_path)` returns a value through SQL; it needs FILE privilege, readable server filesystem access, applicable secure_file_priv rules and size below max_allowed_packet. NULL is ambiguous among unmet conditions. It does not read the Python worker's path, establish write access or grant filesystem privileges. Keep returned files private and preserve exact bytes where the result wrapper permits; do not repair missing characters by guesswork.

These steps establish the tested input/result boundary and a selected bounded result, not a complete assessment. Source-specific credentials, account creation or browser session riding require their separate intended tasks/evidence. See [MySQL LOAD_FILE](https://dev.mysql.com/doc/refman/8.4/en/string-functions.html#function_load-file) and [aggregate behavior](https://dev.mysql.com/doc/refman/8.4/en/aggregate-functions.html#function_group-concat).
