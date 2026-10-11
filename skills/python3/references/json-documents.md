# Validate a saved JSON document

Require a trusted Python 3 interpreter, one existing bounded regular input and a fresh output in a private directory. Preserve the acquired bytes; parse data without importing an application or fetching URLs in it. Define `capture` and `formatted` as the selected absolute paths:

~~~bash
umask 077
(set -C; "$python_bin" -I -S -m json.tool < "$capture" > "$formatted")
status=$?
~~~

Retain status and stderr. Input/output redirection avoids confusing a filename with a module option and noclobber protects an existing destination. `json.tool` validates the parser's JSON syntax and formats the document; it does not execute strings. A parse/encoding error or incomplete capture leaves output incomplete, even if a file was created. Select the actual format before changing parsers.

A pretty-printed JSON object is one document spanning lines. It is not newline-delimited JSON: applying `json.loads` to each line fails, and overwriting one variable for each record silently retains only the last record of actual NDJSON. Use `--json-lines` only for a verified line-record format on a Python version supporting it. Preserve record count and per-record failures rather than discarding errors.

Inspect the expected root type, array/object fields and field types after parsing. For a saved FFUF-style object, a `results` array contains selected reported responses, not proof every candidate completed. Empty results differs from a missing field or parse failure. Formatting is not application-schema validation or strict rejection of every standards edge: Python's defaults allow non-finite numbers and repeated object keys, keeping the last value. Use the application's required validator when these matter.

The formatted copy changes whitespace/escaping and can discard duplicate keys; it is not a byte-identical capture. Retain the original and describe which representation was checked. A link string is data: relative references need their actual document base, and resolving a URL does not request it or establish an authorized destination. No automatic crawling follows this task.

See the [standard-library JSON CLI and parser limits](https://docs.python.org/3.12/library/json.html).
