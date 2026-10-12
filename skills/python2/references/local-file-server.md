# Serve selected owned files with the legacy handler

Use an existing trusted Python2.7 environment when that legacy handler is the selected tool. Define `python2_bin`, `serve_dir` as an existing private directory containing only the approved files, `bind_ip` as the approved local address and `port` as an available unprivileged decimal port. Run in a tracked foreground session:

~~~bash
"$python2_bin" -c 'import os, sys, BaseHTTPServer, SimpleHTTPServer; os.chdir(sys.argv[1]); server = BaseHTTPServer.HTTPServer((sys.argv[2], int(sys.argv[3])), SimpleHTTPServer.SimpleHTTPRequestHandler); server.serve_forever()' \
  "$serve_dir" "$bind_ip" "$port"
~~~

This uses the selected working directory and explicit IPv4 listener. SimpleHTTPServer's module CLI otherwise defaults to all interfaces and current directory; it has no Python3-style --bind/--directory switches. Choose a reachable approved interface when the client is elsewhere;127.0.0.1 serves only this machine's namespace. A bind/startup failure leaves no server.

The handler serves files and directory listings, with no authentication or TLS. Symlinks can expose targets beyond the apparent directory, so inspect the owned serving tree first. It does not execute transferred programs. Retain one expected GET path, peer/time/status and independent client save/size/digest evidence when transfer is the question. A logged200 proves the HTTP response status, not application execution or artifact integrity; a404 can reflect path/case/directory context rather than a transport failure.

Use the task's total runtime budget, stop only this owned foreground server, and verify its listener closes. No default service lifetime is imposed by serve_forever. See the matching [SimpleHTTPServer contract](https://github.com/python/cpython/blob/v2.7.18/Doc/library/simplehttpserver.rst) and [BaseHTTPServer lifecycle](https://github.com/python/cpython/blob/v2.7.18/Doc/library/basehttpserver.rst). No Python installation is part of this task.
