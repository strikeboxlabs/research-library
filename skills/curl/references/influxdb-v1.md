# InfluxDB v1 HTTP queries and authentication

Use for a scoped InfluxDB **v1** HTTP endpoint. This is InfluxQL's `/query` API, not v2 Flux or its token model. Required inputs are the correct endpoint as reachable from the executing host, the selected authentication context and private response files. A remote host's `127.0.0.1:8086` is not the workstation's loopback; use the established local session or an authorized mapped forward.

## Identify the service and authentication boundary

Define `base` as its exact base URL and `headers`/`body` as fresh private paths. Capture `/ping`:

~~~bash
curl --silent --show-error --connect-timeout 5 --max-time 30 --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\n' "$base/ping"
~~~

A successful ping and `X-Influxdb-Version` are service/version leads. They do not prove that query authentication is enabled, that a distribution lacks backports or that a particular JWT is accepted. InfluxDB v1 can run with authentication disabled; compare one permitted unauthenticated query against the same query with the selected credentials before attributing access to a token.

For a Bearer token, put the single `Authorization: Bearer ...` header in a private `auth_headers` file, rather than a shared command transcript. Curl's supported `--header @file` reads it. Do not upload captured credentials or signing secrets to an online JWT editor. Basic authentication is another v1 mechanism and has a separate credential/context; choose the mechanism actually configured.

For an authorized test of older JWT handling: upstream **1.7.5** HMAC verification used the configured shared secret even when blank, then required a numeric positive `exp` and nonempty string `username` identifying an existing InfluxDB metastore user. **1.7.6** explicitly rejects Bearer authentication when that secret is blank. Thus a blank-key HS256 candidate tests a specific older-implementation/configuration hypothesis, not a universal v1 behavior. Use a local signing tool with exact key bytes and a short future expiration. Select one permitted username from evidence or label it as a hypothesis; a chat nickname or application `user` measurement does not establish an InfluxDB administrative identity. Test the selected token with the query below; keep authentication acceptance separate from that user's database privileges. An unknown-user, signature or clock failure calls for a different next check; retain each candidate and its result when revising the relevant hypothesis.

## Discover the selected database and measurement

~~~bash
query='SHOW DATABASES'
curl --silent --show-error --connect-timeout 5 --max-time 30 --get --header "@$auth_headers" --data-urlencode "q=$query" --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\n' "$base/query"
~~~

Check curl status, HTTP status **and** `results[].error`/top-level errors. Database visibility can be privilege-scoped. `_internal` is not automatically the application's database; select the database evidenced by application configuration or the returned inventory. Define `database` accordingly and use fresh response paths for each request:

~~~bash
query='SHOW MEASUREMENTS'
curl --silent --show-error --connect-timeout 5 --max-time 30 --get --header "@$auth_headers" --data-urlencode "db=$database" --data-urlencode "q=$query" --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\n' "$base/query"
~~~

`--get` puts the encoded `db` and `q` parameters in the query string; pass unescaped query text so curl encodes it once. Keep `SELECT` without `INTO` and `SHOW` discovery separate from statements that write or change users/configuration. Quote measurement/field identifiers with double quotes in InfluxQL; single quotes denote string values. Queries ordinarily use the database's default retention policy unless another is selected.

For a measurement actually named `user`, inspect its fields and then read the needed records under the same database context. Run the database-scoped capture command above with this schema query first:

~~~bash
query='SHOW FIELD KEYS FROM "user"'
~~~

After inspecting that response, use fresh capture paths and run the same command with:

~~~bash
query='SELECT * FROM "user" LIMIT 10'
~~~

This selection is a bounded sample, not a complete account export. Select only required fields after inspecting the schema; WHERE time and explicit ordering can bound another task. `LIMIT` limits points and grouped series can each contribute results; it is not a universal total-row cap. An empty series can reflect privilege, measurement/retention-policy spelling, time range or selected fields rather than no stored data.

## Interpret the response before using a record

Each series has its own `columns`, positional `values` arrays and sometimes `tags`; map each row against **that** column list, retaining null/boolean types and timestamps. Never hardcode a password or username column index from another response. **Illustrative:** columns `["time","enabled","username"]` with values `[["2022-01-01T00:00:00Z",false,"example-user"]]` describes an application record; `enabled=false` does not establish the OS account's state.

Inspect every result/series, errors and `partial` indicators. A transport cutoff, maximum-row truncation or requested chunked stream can leave incomplete results; chunked responses contain successive JSON objects rather than one ordinary document. A successful first object does not prove the whole stream arrived. For full coverage, establish the query bounds, paging/chunk handling and completion before reporting an absence or record count.

A stored credential belongs to the evidenced application record and may be stale. Keep it private and, if the task explicitly authorizes a selected OS-account test, use the normal credential prompt and confirm the resulting OS identity separately. Neither an HTTP 200 nor a database username is evidence of an OS login.

References: [v1 query API](https://docs.influxdata.com/influxdb/v1/api/query/), [schema queries](https://docs.influxdata.com/influxdb/v1/query_language/explore-schema/), [InfluxQL selection and limits](https://docs.influxdata.com/influxdb/v1/query_language/explore-data/), [v1 authentication](https://docs.influxdata.com/influxdb/v1/administration/authentication_and_authorization/), [1.7.5 authentication implementation](https://github.com/influxdata/influxdb/blob/v1.7.5/services/httpd/handler.go), [1.7.6 blank-secret guard](https://github.com/influxdata/influxdb/blob/v1.7.6/services/httpd/handler.go).
