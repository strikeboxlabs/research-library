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

## Receive an authorized two-way process stream

When the selected task requires sending commands to an already authorized remote process stream, keep stdin/stdout connected to the tracked terminal. Use the same reviewed bind address/port; omit `--recv-only` and output-file redirection:

~~~bash
ncat --listen --verbose --idle-timeout 60s "$bind_ip" "$port"
~~~

The idle duration is an adjustable task choice, not a total session budget. Ordinary Ncat relays both directions; `--recv-only` would prevent your input from reaching the peer. This listener does not itself create a shell on either endpoint. Establish the separately authorized process invocation, expected peer/time and a selected command's returned output. Use `id` in an identified remote Unix shell when its identity is part of the task; a socket peer, prompt or source screenshot cannot replace that observation.

Plain TCP has no SSH-like authenticated peer or confidentiality. Keep the selected stream within its authorized network context. A missing prompt/TTY may reflect buffering, stdin, shell mode or missing terminal rather than failed code execution. A PTY on the peer and the operator terminal's settings remain separate layers. Exit the owned remote child deliberately, close the receiver and verify the known processes ended; avoid `--keep-open` unless more than one connection is intended. Check the actual Ncat version's EOF behavior before treating a disconnected stream as completed work.
