# Serve selected owned files for a bounded transfer

Use a trusted Python 3 interpreter with `http.server` available and `--directory` support (3.7+). Define `python_bin`, `serve_dir` as a dedicated absolute directory containing only intended files, `bind_ip` as the chosen local interface and `port` as an available unprivileged port:

~~~bash
"$python_bin" -m http.server --bind "$bind_ip" --directory "$serve_dir" "$port"
~~~

Keep the server foreground in its own tracked session. Its default is port 8000 and all interfaces; specify the selected bind instead. Loopback serves only local clients; a separate authorized host needs the reachable interface/route. Low ports need existing privileges, not an automatic sudo retry. A bind error leaves no server even if the client later gets a response from something else on that port.

The standard handler serves files and directory listings; it does not execute a served Python/PHP/script file merely because of its extension. It supplies no application authentication and follows symbolic links, so `--directory` is not filesystem confinement. Select a clean tree and inspect links; do not serve a whole home/task directory by convenience. Ordinary static transfer does not need `--cgi`.

Request the exact encoded filename using the consumer's actual route and compare its returned size/digest or public marker. A server log showing `GET /marker.txt ... 200` establishes a response at that server, not that a remote curl job saved it to a protected destination or a scheduler executed it. Preserve client status/body and the separate destination/consumer evidence when those are the task.

Bound the observation window/output using the worker's session control; stop the owned server with Ctrl-C/the tracked process when transfer ends and confirm that listener closes. Missing path, wrong bind, directory listing, stale server and incomplete download call for different next checks. Do not restart by killing an unidentified process.

Reference: [Python http.server CLI and link behavior](https://docs.python.org/3.12/library/http.server.html).
