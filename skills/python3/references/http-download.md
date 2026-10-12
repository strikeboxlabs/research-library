# Retrieve one approved public artifact

Use when a trusted Python interpreter must save an approved HTTP(S) artifact and no dedicated transfer client fits the task. Require the exact endpoint (including port/path), an expected maximum size and a new destination in a private directory. This is retrieval only; a saved executable is not trusted or installed.

The source's `urllib.request.urlretrieve(url, filename)` returns a filename/header pair and can overwrite that filename. Its Content-Length short-read check cannot establish completeness without the header and does not impose an upper bound. For a bounded disposable retrieval, define `url`, `destination` and positive `max_bytes`:

~~~bash
"$python_bin" -I -S - "$url" "$destination" "$max_bytes" <<'PY'
import hashlib
import sys
from urllib.request import urlopen

url, path, limit = sys.argv[1], sys.argv[2], int(sys.argv[3])
if limit <= 0 or not url.startswith(("https://", "http://")):
    raise SystemExit("require an HTTP(S) URL and positive byte limit")
with urlopen(url, timeout=5) as response:
    data = response.read(limit + 1)
    if len(data) > limit:
        raise SystemExit("size limit exceeded; destination not created")
    expected = response.headers.get("Content-Length")
    if expected is not None and len(data) != int(expected):
        raise SystemExit("body length mismatch; destination not created")
    print("final_url", response.url, "status", response.status)
with open(path, "xb") as output:
    output.write(data)
print("bytes", len(data), "sha256", hashlib.sha256(data).hexdigest())
PY
~~~

Select a small bound: this helper buffers that amount in memory. urllib follows redirects and applies its default proxy policy; approve the resulting origin or use a reviewed opener for a stricter policy. Timeout applies to socket operations, not a complete wall-clock deadline. The fresh exclusive file prevents overwriting an existing destination; failed writes can leave a partial file that must remain labeled incomplete.

Compare the artifact's expected size/hash through an independent trusted source before any later use. A 200 response can still contain HTML/error content, and a filename extension does not identify its format. An HTTP server on an explicit nondefault port cannot be reached by omitting that port. Finish with the actual endpoint, final URL, status, saved size/hash and completeness/provenance limits. See [urllib retrieval behavior](https://docs.python.org/3.12/library/urllib.request.html).
