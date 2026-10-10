# One selected callback body

Use when an explicitly controlled browser/application callback submits POST evidence rather than downloading a file. Python's standard `SimpleHTTPRequestHandler` does not implement that upload. Required helper: `scripts/receive_callback.py`, which saves **one** bounded raw body at `/evidence`, rejects other paths/oversize/incomplete requests and never serves the stored file. Leave unrelated source mail/secret collection out of the callback.

Define `python_bin` as the installed interpreter, `helper` as this package's absolute `scripts/receive_callback.py`, `listen_ip` as the interface reachable through the intended route, `port` as a selected unprivileged port and `output` as a fresh private file. Start in the foreground:

~~~bash
umask 077
"$python_bin" "$helper" --bind "$listen_ip" --port "$port" --output "$output" --max-bytes 65536
~~~

The handler accepts an explicit Content-Length and a nonempty body within the limit, with a five-second socket timeout. It does not implement chunked uploads or browser authentication. Its listener has no client authentication: bind/route it only to the intended controlled sender, stop when the selected request is captured and keep output private. The file uses exclusive creation; another accepted body or existing file receives 409 rather than overwriting evidence.

Use a unique harmless task marker or one specifically selected test record. Record request time/method/path, expected marker and sender context separately from stored content; raw HTML/JSON is evidence, not code to execute. A valid POST proves body arrival, not its claimed origin. Match the controlled action/time and browser/application evidence. A page can report a connection failure after the request already reached the listener; inspect the stored result before retrying.

A browser's same-origin fetch can read a response under that browser session. A later cross-origin `fetch(...,{mode:'no-cors'})` is limited to permitted request forms and an opaque response; it does not grant cross-origin response reading. CORS, CSP/connect policy and browser mixed-content rules can affect a callback. An HTTP request made by curl does not reproduce a browser's script execution or those policies.

Do not discard exceptions silently or parse unknown HTML using one greedy regex. Preserve raw response bytes, then select fields through the actual document/serialization structure. Identify truncation/transport encoding separately. Stop with Ctrl-C and verify the listener closes. The helper's bounded receiver is a task aid, not a production upload service. See [Python handler APIs](https://docs.python.org/3/library/http.server.html) and [browser opaque responses](https://developer.mozilla.org/en-US/docs/Web/API/Request/mode).
