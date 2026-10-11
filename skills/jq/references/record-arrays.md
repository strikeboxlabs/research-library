# Extract an acquired response's record array

Work on an existing saved JSON response after transport and application status have been assessed. Establish the documented field path and selected string field; a successful JSON parser does not establish a complete response. Define `response` as that file and `extracted` as a fresh output path.

For one top-level array of objects whose selected text field is `name`, validate the whole small response before writing a JSON array:

~~~bash
umask 077
jq -s -e 'length == 1 and (.[0] | type == "array" and all(.[]; type == "object" and (.name | type == "string")))' "$response" > /dev/null &&
jq '[.[].name]' "$response" > "$extracted"
status=$?
~~~

The selected field is a documented literal, not guessed from a display name. Preserve object identifiers and field associations separately when the projection will lose them; an email prefix is not automatically a directory logon identity. This operation does not deduplicate or acquire additional records.

For a response whose records are instead in `hits.hits` and whose selected text field is `_source.quote`, validate one top-level object, that array and every selected value:

~~~bash
umask 077
jq -s -e 'length == 1 and (.[0] | type == "object" and (.hits.hits | type == "array" and all(.[]; type == "object" and (._source.quote | type == "string"))))' "$response" > /dev/null &&
jq '[.hits.hits[]._source.quote]' "$response" > "$extracted"
status=$?
~~~

Adapt the literal paths to the established schema. Check `status` and diagnostics; preserve the original on failure. `.hits.hits` selects the nested array, whereas `.hits.hits[]` generates its elements. Wrapping the generated strings in `[...]` retains string boundaries even when values contain newlines. An empty array is valid but does not prove that the server has no records. Avoid optional iteration or filtering missing fields into silence when completeness matters.

If a downstream format explicitly requires newline-delimited text and every selected value excludes newline/NUL, validate that framing first and use raw output, such as `jq -r '.[].name' "$response"` for the top-level case. Do not pipe ordinary JSON strings through `tr -d '"'`: it deletes quotes belonging to values and leaves JSON escape spelling. Keep a JSON array when arbitrary text boundaries matter.

Record the **returned array length**, response scope and any pagination/partial-result metadata separately. In Elasticsearch, `hits.total` describes matching hits; it is not the returned array's length. Its version-dependent representation can include a lower-bound relation. Check `timed_out` and shard failures before treating the saved records as complete; a separate count request need not describe the same snapshot. This extraction performs no request, pagination or record recovery.

See the [jq iterator and array constructor documentation](https://jqlang.org/manual/) and [Elasticsearch search response contract](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search).
