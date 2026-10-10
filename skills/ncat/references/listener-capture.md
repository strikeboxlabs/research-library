# Capture one callback and distinguish TCP from HTTP

Select Nmap Ncat, an authorized reachable `bind_ip` and available `port`, plus fresh private `capture_file`/`listener_log`. For one TCP callback, keep the listener in the foreground:

~~~bash
umask 077
ncat --listen --verbose --recv-only --idle-timeout 20s "$bind_ip" "$port" \
  > "$capture_file" 2> "$listener_log"
~~~

An explicit address avoids accidentally exposing every interface; loopback is reachable only from the same host. A low port needs existing bind privileges. A startup error leaves no listener. The idle timeout is not a total duration or guaranteed bound on waiting for the first connection; use the worker's overall runtime budget and stop its owned process explicitly.

This receives bytes without a response. An HTTP client can send a request yet wait indefinitely for an HTTP reply. Capture the request line, headers and exactly the framed body (Content-Length or chunked encoding); a body can contain newlines/binary bytes. An arrival proves receipt at this listener, not successful application processing or browser access to the response.

Use `--keep-open` only when multiple callbacks are intended. It accepts simultaneous connections until stopped; shared stdout does not preserve separate per-client record boundaries. Prefer a protocol-aware collector when exact callback attribution/body parsing or HTTP responses matter. Do not infer that a missing browser callback means no earlier API write occurred.

Retain peer/time evidence from the listener log alongside private captured bytes, but avoid treating a proxy's peer IP as the original browser's identity. Ncat does not enforce browser CORS or provide an HTTP application's status/body semantics. A raw TCP callback and a fully completed HTTP exchange are different results. See [listener and stream options](https://nmap.org/book/ncat-man.html).
