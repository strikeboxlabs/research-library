---
name: telnet
description: Inspect one known legacy text service with a telnet client. Use when a custom application prompt, local telnet commands, line handling or connection-only evidence obscure the result.
---

# Inspect a selected legacy text service

Read this entire SKILL.md before acting. Require the installed client, one authorized known host/port and a selected read-only application command. Inspect local help to identify the implementation; GNU options below are conditional on that client. Complete with the endpoint, banner, actual command/response and remaining coverage, then close this session.

For GNU Inetutils, define `host` and numeric `port` and omit inherited startup commands/automatic login:

~~~bash
telnet --no-rc --no-login "$host" "$port"
~~~

`Connected` establishes a TCP connection, not a login, database query or healthy application. Read the service banner and its documented read-only help/status response before choosing an operation. A custom `HELP` at the remote application's prompt differs from help at the local `telnet>` prompt. Keep the response paired with the command; an invalid-configuration error is a bounded result, not successful query execution. A directory/name returned by the application is not a local filesystem path.

Use the client's displayed escape character (GNU default Ctrl-]) to enter local command mode; `quit` closes the session and exits. Typing quit at the remote prompt can instead send an application command. Record connection refusal, timeout, EOF or missing prompt rather than treating absent output as an empty dataset.

Telnet is not a TLS client or a byte-transparent replacement for every TCP protocol. GNU's ordinary nonstandard-port behavior omits initial TELNET-option negotiation, but line/escape handling remains relevant. Choose the application's proper client for binary/TLS traffic. Keep traces private if explicitly needed; they can contain content and credentials.

See [GNU invocation options](https://www.gnu.org/software/inetutils/manual/html_node/telnet-invocation.html) and the [packaged Inetutils operation manual](https://manpages.debian.org/unstable/inetutils-telnet/inetutils-telnet.1.en.html); resolve differences against the installed implementation.
