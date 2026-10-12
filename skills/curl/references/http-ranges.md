# Retrieve and qualify one HTTP byte range

Require the approved ordinary artifact URL, its established authentication/TLS context and the requested decimal start/end offsets. A range request does not grant access to an otherwise inaccessible file. Define `url`, `range` such as `0-499`, and fresh private `headers`/`body` paths. Keep the URL and headers tied to one GET:

~~~bash
umask 077
curl --silent --show-error --connect-timeout 5 --max-time 30 --range "$range" --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\nsize=%{size_download}\n' "$url"
~~~

`--range` (`-r`) requests that HTTP byte interval. Positions start at zero and include both endpoints: `0-499` requests 500 bytes, whereas `0-500` requests 501. `500-` requests the remainder; `-500` requests a suffix of up to 500 bytes. Keep this task to one interval; multipart responses require separate framing interpretation.

Check final curl status and the complete status/headers/body. For 206, inspect Content-Range and the returned body length; a successful requested prefix remains a partial artifact. Its total length can be known without those remaining bytes being acquired. A nonzero status can leave an incomplete part. For 200, the server may have ignored Range and sent the ordinary representation. For 416, retain the error and any reported length, then reconcile the offsets or changed artifact instead of calling the body recovered.

Range is a request preference, not a download-size cap. Apply the task's transfer/time budget and inspect the response. Avoid automatic decoding when exact representation offsets matter; Content-Encoding can describe a byte sequence different from the decoded content. When combining parts, require matching strong representation validators and complete range coverage; do not concatenate bytes from changed versions.

Finish with requested interval, actual response interval/status, artifact identity and received-byte coverage. Accept-Ranges or a HEAD response alone does not establish that this GET delivered the requested part.

References: [curl range option](https://curl.se/docs/manpage.html#-r), [HTTP byte ranges](https://www.rfc-editor.org/rfc/rfc9110.html#section-14.1.2) and [206 interpretation](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.3.7).
