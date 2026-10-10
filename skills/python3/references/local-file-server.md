# Serve selected owned files for a bounded transfer

Use a trusted Python 3 interpreter with `http.server` available and `--directory` support (3.7+). Define `python_bin`, `serve_dir` as a dedicated absolute directory containing only intended files, `bind_ip` as the chosen local interface and `port` as an available unprivileged port:

~~~bash
"$python_bin" -m http.server --bind "$bind_ip" --directory "$serve_dir" "$port"
~~~

Keep the server foreground in its own tracked session. Its default is port 8000 and all interfaces; specify the selected bind instead. Loopback serves only local clients; a separate authorized host needs the reachable interface/route. Low ports need existing privileges, not an automatic sudo retry. A bind error leaves no server even if the client later gets a response from something else on that port.

The standard handler serves files and directory listings; it does not execute a served Python/PHP/script file merely because of its extension. It supplies no application authentication and follows symbolic links, so `--directory` is not filesystem confinement. Select a clean tree and inspect links; do not serve a whole home/task directory by convenience. Ordinary static transfer does not need `--cgi`.

Request the exact encoded filename using the consumer's actual route and compare its returned size/digest or public marker. A server log showing `GET /marker.txt ... 200` establishes a response at that server, not that a remote curl job saved it to a protected destination or a scheduler executed it. Preserve client status/body and the separate destination/consumer evidence when those are the task.

Bound the observation window/output using the worker's session control; stop the owned server with Ctrl-C/the tracked process when transfer ends and confirm that listener closes. Missing path, wrong bind, directory listing, stale server and incomplete download call for different next checks. Do not restart by killing an unidentified process.



## Serve an owned browser test module with CORS

Use this conditional branch when a controlled browser needs an external JavaScript module and the ordinary static server's response lacks the required CORS header. Define the same dedicated serve_dir/bind_ip/port, and `allowed_origin` as the exact scheme/host/port of the test application. Put only reviewed intended assets in that directory. With Python 3.7+:

~~~bash
"$python_bin" -I -S - "$serve_dir" "$bind_ip" "$port" "$allowed_origin" <<'PY'
import functools
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

directory, address, port, origin = sys.argv[1:]
class Handler(SimpleHTTPRequestHandler):
    extensions_map = dict(SimpleHTTPRequestHandler.extensions_map,
                          **{'.js': 'text/javascript', '.mjs': 'text/javascript'})
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', origin)
        self.send_header('Vary', 'Origin')
        super().end_headers()

handler = functools.partial(Handler, directory=directory)
with ThreadingHTTPServer((address, int(port)), handler) as server:
    server.serve_forever()
PY
~~~

Keep it foreground and apply the same owned-root/session/cleanup rules above. The snippet explicitly supplies a JavaScript MIME type and one allowed origin, not application authentication or arbitrary-origin credential access. It handles static GET/HEAD, not a custom OPTIONS/preflight or POST collector. A test requiring those methods needs its observed preflight/request contract rather than broadening headers blindly. It follows the standard handler's symlink behavior.

From the actual browser context, import the selected module or inspect its network response. A server `GET ... 200` can occur even when the browser refuses the module on CORS, MIME, CSP, mixed-content or syntax grounds. A public marker produced by the module distinguishes retrieval from execution. A raw TCP listener that merely receives its GET does not supply a complete module response. Origins include the port; an IP URL and application hostname are different origins.

This server does not need the application's cookies to serve an anonymous test module. HttpOnly cookies still accompany permitted same-origin application requests made by script executing in that origin; hosting the module does not let the static server read those cookies. If sending selected textual results to a controlled collector, choose an explicit byte encoding: JavaScript btoa expects byte-valued characters, not arbitrary Unicode text, and base64 in a URL/form needs outer URL encoding. Capture complete results within the task's data scope; a truncated query or URL-length rejection is incomplete evidence.

References: [Python static server APIs/CLI](https://docs.python.org/3.12/library/http.server.html), [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS) and [JavaScript btoa byte constraints](https://developer.mozilla.org/en-US/docs/Web/API/Window/btoa).
