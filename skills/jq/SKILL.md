---
name: jq
description: Validate and extract JSON API fields or construct request bodies with jq. Use when missing fields, false values, escaping or added newlines can turn a plausible response into corrupted evidence.
---

# Preserve JSON types and extracted text

Check `jq --version`. Save the HTTP status, headers and body separately before parsing; `curl ... | jq` can hide curl's failure behind jq's exit status. Valid JSON is not proof of a successful API operation.

Define `response` as an existing JSON response and `extracted` as a fresh output path. For an API whose documented `file` field holds text, require exactly one object with a string field before extraction:

~~~bash
umask 077
jq -s -e 'length == 1 and (.[0] | type == "object" and (.file | type == "string"))' "$response" > /dev/null &&
jq -j '.file' "$response" > "$extracted"
~~~

Plain `.file` prints a JSON string with quotes and escapes. `-r` emits the decoded string but appends a newline; `-j` avoids adding one. This matters when reconstructing source/configuration files or comparing exact text. JSON strings represent Unicode text, not arbitrary original binary bytes; a binary API needs its defined encoding and integrity checks. Keep originals on parse/transfer failure.

An absent field normally becomes `null`. Use `has("field")` when distinguishing absence from a present null matters. `//` also substitutes for boolean false, so it can conceal a legitimate false value. `-e` reports the final output's truthiness: false/null return 1, no result returns 4. A successful parser exit alone does not establish the expected type, record count or application result. The `-s` check above deliberately validates the complete small response.

To construct a JSON body containing an existing UTF-8 text file, define `source_text` and a fresh `request` path:

~~~bash
jq -n --rawfile content "$source_text" '{file: $content}' > "$request"
~~~

This escapes embedded quotes, backslashes and newlines without search-and-replace chains. Use `--arg` for literal strings and `--argjson` for validated JSON values: `"true"` and `true` are different. Never interpolate external text into the jq program itself. Constructing a request file does not submit it; verify the intended fields and HTTP operation before use.

Documentation reviewed 2026-10-09; Linux execution untested. Cases: Backend pp. 2–4, 12–15; BackendTwo pp. 11–16. Source: [jq manual](https://jqlang.org/manual/).
