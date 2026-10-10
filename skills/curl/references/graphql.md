# Inspect a GraphQL endpoint with curl

Use the endpoint observed in application traffic or configuration, with its actual authentication and hostname. `/graphql` and `/api/graphql` are conventions, not discovery guarantees. An SSH forward changes the connection path; it does not supply application credentials or change where a server-side URL is resolved.

## Discover the root names before guessing fields

When schema inspection is in scope, save this small introspection request as UTF-8 JSON in `request_json`:

~~~json
{"query":"query SchemaRoots { __schema { queryType { name } mutationType { name } } }","operationName":"SchemaRoots","variables":{}}
~~~

Define `url` as the selected endpoint and `headers`/`body` as fresh private response paths. This request needs no mutation:

~~~bash
umask 077
curl --silent --show-error --connect-timeout 5 --max-time 30 \
  --header 'Content-Type: application/json' \
  --header 'Accept: application/graphql-response+json, application/json' \
  --data-binary "@$request_json" --dump-header "$headers" --output "$body" \
  --write-out 'status=%{http_code}\n' "$url"
status=$?
~~~

For required bearer authentication, add `--header "@$auth_headers"` with an existing private header file. POST is selected by the body option. Keep TLS verification and use the main skill's hostname-routing procedure where needed. Do not follow redirects blindly.

An **illustrative** response is `{"data":{"__schema":{"queryType":{"name":"Query"},"mutationType":{"name":"Mutation"}}}}`. Those are observed type names, not fixed names every service uses. A null `mutationType` means this schema has no mutation root; a denied/failed introspection request establishes no such absence. Introspection describes a schema and is not inherently a vulnerability or proof that a caller may invoke every listed field. If disabled, use the supplied schema or captured application operations.

## Inspect one observed type

For the illustrative root named `Mutation`, the following body lists field arguments and return types without executing a mutation. Replace the variable value with the root/type actually observed; construct dynamic JSON with a serializer:

~~~json
{
  "query": "query InspectType($typeName: String!) { __type(name: $typeName) { name fields { name args { name defaultValue type { kind name ofType { kind name ofType { kind name } } } } type { kind name ofType { kind name } } } } }",
  "operationName": "InspectType",
  "variables": {"typeName": "Mutation"}
}
~~~

Send that reviewed body with the same curl procedure into fresh response files. `NON_NULL` and `LIST` wrap another type; follow `ofType` to the named leaf and extend the query when wrappers exceed this small selection. A missing leaf name at the selected depth is not an unknown scalar. The default field listing omits deprecated fields; use `fields(includeDeprecated: true)` when that coverage matters. Required arguments without defaults must be supplied. Match schema types: an `Int!` variable needs a JSON integer, not a quoted decimal string. `defaultValue` is GraphQL literal text; do not treat it as an already-decoded JSON value.

The envelope's `query` field contains an operation document, which can itself contain a mutation. Inspect its operation before sending; the field name does not make a request read-only. Choose `operationName` when a document contains multiple operations. Use variables for values instead of concatenating quoted strings into GraphQL source. Object/list-of-object results need a selection set; scalar results such as Boolean do not.

## Interpret transport and execution separately

| Observation | Next decision |
|---|---|
| Nonzero curl status, truncated body or timeout | Preserve diagnostics; parsing a fragment cannot establish a complete response. A timed-out write may already have happened. |
| 200 with `errors` and no `data` | Inspect parsing, validation, authentication and implementation-specific handling. HTTP success is not operation success. |
| `data` plus `errors` | Some execution may have succeeded. Correlate each error's `path` with the affected field; do not discard the valid data or claim complete success. |
| A selected field is `false` | A valid Boolean result, whose application meaning comes from the field contract. Do not replace it with a default via jq's `//`. |
| 400/401/403, HTML or unexpected content type | Check endpoint, request schema, auth and intermediaries before treating the body as GraphQL data. |

Response status conventions vary with server implementation and negotiated media type. Inspect the saved body even after HTTP error status. Introspection alone cannot prove authorization, a URL-fetch effect or the identity of a downstream process. After an ambiguous mutation, inspect the specific state before retrying it; `errors` does not promise rollback.

See the official [HTTP transport guidance](https://graphql.org/learn/serving-over-http/), [introspection](https://graphql.org/learn/introspection/), [query/variable rules](https://graphql.org/learn/queries/) and [response semantics](https://graphql.org/learn/response/) for version and schema differences. Curl's [body/header options](https://curl.se/docs/manpage.html) only transport the document; they do not validate GraphQL.
