---
name: jq
description: Validate JSON fields, extract account maps, construct request bodies and inspect configuration transformations with jq. Use when missing fields, false values, escaping or added newlines can turn a plausible response into corrupted evidence.
---

# Preserve JSON types and extracted text

Read this entire SKILL.md before acting. For decoded username-to-value objects, read [account-map extraction](references/account-maps.md) fully first. Keep the original, validate the selected structure and finish with correctly framed extracted data or an explicit parse/schema gap. Other API/configuration tasks are below.

Check `jq --version`. Save the HTTP status, headers and body separately before parsing; `curl ... | jq` can hide curl's failure behind jq's exit status. Valid JSON is not proof of a successful API operation.

Define `response` as an existing JSON response and `extracted` as a fresh output path. For an API whose documented `file` field holds text, require exactly one object with a string field before extraction:

~~~bash
umask 077
jq -s -e 'length == 1 and (.[0] | type == "object" and (.file | type == "string"))' "$response" > /dev/null &&
jq -j '.file' "$response" > "$extracted"
~~~

Plain `.file` prints a JSON string with quotes and escapes. `-r` emits the decoded string but appends a newline; `-j` avoids adding one. This matters when reconstructing source/configuration files or comparing exact text. JSON strings represent Unicode text, not arbitrary original binary bytes; a binary API needs its defined encoding and integrity checks. Keep originals on parse/transfer failure.

Extraction cannot undo server-side transformations. If an application reads lines and rejoins them, original line endings and a final newline may already be lost. Validate the destination format before deliberately restoring any required terminator.

An absent field normally becomes `null`. Use `has("field")` when distinguishing absence from a present null matters. `//` also substitutes for boolean false, so it can conceal a legitimate false value. `-e` reports the final output's truthiness: false/null return 1, no result returns 4. A successful parser exit alone does not establish the expected type, record count or application result. The `-s` check above deliberately validates the complete small response.

To construct a JSON body containing an existing UTF-8 text file, define `source_text` and a fresh `request` path:

~~~bash
jq -n --rawfile content "$source_text" '{file: $content}' > "$request"
~~~

This escapes embedded quotes, backslashes and newlines without search-and-replace chains. Use `--arg` for literal strings and `--argjson` for validated JSON values: `"true"` and `true` are different. Never interpolate external text into the jq program itself. Constructing a request file does not submit it; verify the intended fields and HTTP operation before use.

## Inspect a configuration transformation before replacing input

`.directories_to_archive |= map(gsub(...))` transforms that field while retaining other fields; it does not validate the whole task. Check its array/string types and every field the downstream program consumes, including destinations or optional operations.

`gsub` replaces non-overlapping matches in the input once; it does not keep applying the rule to newly formed text. This harmless example distinguishes one pass from two:

~~~bash
jq -n '"aabb" | {once:gsub("ab"; ""), twice:(gsub("ab"; "") | gsub("ab"; ""))}'
~~~

The **illustrative** result is `{"once":"ab","twice":""}`. Removing substrings is not path canonicalization, and a string prefix cannot establish containment through `..` or symlinks.

Write a transformed candidate to a separate fresh file and check jq's status before reviewing or consuming it. Redirecting output onto the input path truncates it before jq reads; separately saving a failed command's empty output can destroy it too. Do not treat `for path in $values` over `jq -r` output as one iteration per JSON string: shell splitting and globbing can change boundaries. Keep the list as JSON or use an explicit lossless framing contract.

Use the [jq manual](https://jqlang.org/manual/) for update assignment, raw output and regex semantics.
