---
name: python-http-server
description: Serve selected local files or receive a bounded controlled POST callback with Python's http.server. Use when bind addresses, directory exposure, transfer verification or callback logs need interpretation.
---

# Temporary Python file server

Read this entire SKILL.md before acting. Select a dedicated directory/listener and establish the requested file transfer with size/hash evidence. For a controlled POST callback, read [bounded callback collection](references/post-callback.md) fully and use its required `scripts/receive_callback.py`; ordinary file-server mode cannot receive that body. Finish with request evidence and closed owned listeners, not a log line alone.

Check `python3 --version` and `python3 -m http.server --help`; `--directory` requires a supporting Python version. Define `share_dir` as a dedicated absolute directory containing only the intended files, `bind_ip` as the local interface reachable by the consumer, and `port` as a free unprivileged port:

~~~bash
python3 -m http.server --bind "$bind_ip" --directory "$share_dir" "$port"
~~~

Keep it in the foreground for a temporary transfer. Omitting `--bind` normally listens on all interfaces; omitting `--directory` serves the working directory. `127.0.0.1` restricts access to the same network namespace, so it cannot serve a remote lab client directly. Confirm the listener and request the exact intended file from the consumer's vantage.

The ordinary handler serves files and may expose a directory listing. It follows symbolic links, so a dedicated directory containing links can still expose files outside that directory. Inspect its contents before serving; do not start from a repository root, home directory or directory containing credentials merely because that is the current shell location.

This is a basic download server. Standard mode does not implement arbitrary upload/POST handling or authentication, and it is not a production service. Do not enable CGI as a file-transfer repair. HTTPS options depend on Python version and require deliberate certificate configuration.

An access-log entry establishes a request, not necessarily a completed download or execution of the file. Compare size/hash after transfer. A browser callback may originate from your own preview, a proxy or another visitor; source IP alone does not prove server-side execution. Preserve method, path, time and relevant request context before attributing behavior.

For query-string evidence, percent decoding and base64 decoding are separate layers; do not decode an entire request line or blindly remove characters from encoded data. Logs can contain secrets. Stop the server after use and verify that its listener has closed.

For handler/version behavior, consult [Python http.server](https://docs.python.org/3/library/http.server.html).
