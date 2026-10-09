---
name: ncat
description: Inspect simple TCP services with Nmap Ncat and diagnose line endings, EOF and timeout behavior. Use when netcat variants or silent connections make protocol testing ambiguous.
---

# Ncat protocol interaction

Check `ncat --version` and `ncat --help`. Nmap Ncat, OpenBSD nc and traditional netcat have different options; a walkthrough's `nc -lvnp` is not a portable Ncat recipe. This skill covers direct service interaction, not attaching a command interpreter to a socket.

Define `host` and `port` as the selected service, often an already-established local forward:

~~~bash
ncat --verbose --wait 5s --idle-timeout 20s "$host" "$port"
~~~

`--wait` limits connection establishment; `--idle-timeout` ends an inactive session, not the total duration of an active one. A connected socket without a banner may be waiting for a request. Use the observed protocol's harmless help/status request; don't send arbitrary HTTP or binary probes to an unknown service.

For a documented CRLF line protocol, `--crlf` translates stdin line endings. Do not add it to binary transfers or preformatted CRLF data. Ncat does not implement full Telnet negotiation; use a protocol-aware client when negotiation matters.

For a finite request, define `request_file` as the exact wire-format input and `response_file` as a fresh destination:

~~~bash
ncat --wait 5s --idle-timeout 20s "$host" "$port" <"$request_file" >"$response_file"
~~~

By default, stdin EOF shuts down the sending side while response reading can continue. `--send-only` ignores responses and quits at input EOF, so it is unsuitable when a reply is the evidence. `--recv-only` never sends input. `--no-shutdown` changes half-close behavior and can make the session wait until the peer or timeout closes it; choose it only for a protocol requiring that behavior.

An open TCP port proves transport availability, not application authentication or command success. Retain stderr separately from protocol bytes when automating. For TLS, use the installed Ncat TLS/verification options and the intended hostname; plain Ncat against a TLS service produces misleading silence or binary output.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Appsanity pp. 15, 27, adapted from nc interaction. Source: [Ncat manual](https://nmap.org/book/ncat-man.html).
