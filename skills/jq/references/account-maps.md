# Select account records from a decoded JSON object

Use for an acquired application's username-to-value map. Preserve the original response and establish its presentation/serialization layer first. An HTML-rendered `<pre>` may need one decode of that element's text; do not repeatedly unescape the resulting JSON. Plain JSON should go directly to jq.

If `escaped_value` contains **only the extracted HTML-escaped value text**, not tags or a protocol frame, and `decoded_json` is a fresh destination, this Python standard-library glue decodes one presentation layer and rejects invalid JSON before writing:

~~~bash
python3 - "$escaped_value" "$decoded_json" <<'PY'
import html
import json
from pathlib import Path
import sys

text = html.unescape(Path(sys.argv[1]).read_text(encoding="utf-8"))
json.loads(text)
with Path(sys.argv[2]).open("x", encoding="utf-8", newline="") as output:
    output.write(text)
PY
~~~

Do not apply this to text already decoded by a browser/HTML parser. An HTML wrapper and Memcached VALUE/END framing must be separated using their actual formats first. A protocol byte count cannot be validated against the HTML-escaped document length. This conversion does not identify the hash algorithm or guarantee a complete source response.

Define `records` as the decoded JSON file. Require exactly one object with string values before treating it as this account map:

~~~bash
jq -s -e 'length == 1 and (.[0] | type == "object" and all(.[]; type == "string"))' "$records" > /dev/null
~~~

Check that result before extraction. A different schema requires a different selector, not a grep/awk split on quotes. Duplicate JSON keys can be collapsed by parsers; a full JSON parser check does not prove original row uniqueness. Preserve acquisition evidence when that matters.

For `accounts` as a fresh private username-list path, require nonempty keys without line breaks before making one name per line:

~~~bash
umask 077
jq -e 'all(keys[]; length > 0 and (test("[\\r\\n]") | not))' "$records" > /dev/null &&
jq -r 'keys[]' "$records" > "$accounts"
~~~

Other consumers may strip whitespace or restrict names; validate their contract too. For a selected `user` and `digest_file`, preserve the account association and reject absence/type mismatch:

~~~bash
jq -e --arg user "$user" 'has($user) and (.[$user] | type == "string" and length > 0 and (test("[\\r\\n]") | not))' "$records" > /dev/null &&
jq -r --arg user "$user" '.[$user]' "$records" > "$digest_file"
~~~

Before feeding a one-line hash consumer, validate this selected value's encoding, delimiters and newline limits. A 32-character hex value fits several formats; report a format hypothesis separately from a recovered candidate and any actual login. Missing account keys or an expired cache entry are incomplete leads, not proof that the OS account is absent.

See [jq object keys, all, raw output and argument binding](https://jqlang.org/manual/) and [Python's single HTML entity decode](https://docs.python.org/3/library/html.html#html.unescape).
