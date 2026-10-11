# Read the selected local API response

Identify the observed socket's service and documented read-only endpoint. Define `socket` as its absolute path, `url` as the complete HTTP URL with the required authority/path, and `headers`/`body` as fresh private files. Check installed Unix-socket support with `curl --version` and help:

~~~bash
umask 077
curl --silent --show-error --max-time 20 --unix-socket "$socket" \
  --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\n' "$url"
~~~

Check transport status, HTTP status and the expected response structure separately. `--unix-socket` selects local socket transport; the URL still supplies HTTP authority/path. A denied or absent socket differs from an application error. A response establishes access to that API in the current filesystem/process context; it does not identify which host owns the daemon or authorize other endpoints. Finish with the selected endpoint, response and unresolved identity/permission facts. See the [curl option manual](https://curl.se/docs/manpage.html#--unix-socket).
