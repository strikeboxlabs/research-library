---
name: socat
description: Forward a selected owned TCP service through an explicitly bound Linux Socat listener. Use when listener direction, address families, child lifetime or connection evidence determine a local service-routing result.
---

# Forward one owned TCP service

Read this entire SKILL.md before acting. Require one owned destination service, approved local bind/port, compatible application client and bounded session lifetime. Finish with listener/connection/application evidence and closure of the tracked parent and children; a listening socket alone does not establish destination success. No conditional resources are required.

Inspect `socat -V` and `socat -hh` for this build's supported address/options. Define `socat_bin` as that verified invocation, `local_port` as a free unprivileged port, `destination_host` as the known IPv4 service address/name and `destination_port` as its port. For a local consumer, keep the relay in a tracked foreground session:

~~~bash
"$socat_bin" -d -d -T 30 \
  "TCP4-LISTEN:$local_port,bind=127.0.0.1,reuseaddr,fork,max-children=2,accept-timeout=60" \
  "TCP4:$destination_host:$destination_port,connect-timeout=5"
~~~

Both socket endpoints belong to the Socat machine's namespace. The left address listens locally; each accepted connection opens the right destination from that machine. `TCP4` selects IPv4 rather than inheriting version-dependent defaults. A hostname is resolved there. Loopback serves local consumers only; an explicitly approved non-loopback bind changes listener exposure, not the destination application's authorization.

`fork` retains a listening parent and a child per connection. `max-children` bounds concurrent children, not total requests. `reuseaddr` helps rebinding and is not permission to replace an occupied listener. `accept-timeout` limits idle waiting for a new connection; `connect-timeout` bounds destination connection setup; `-T` bounds inactivity in the transfer loop. None is a total session deadline. Use the task's session controller for that budget and track child lifetime separately.

Use the intended application against the local port and preserve its response/error plus Socat diagnostics. The relay copies a bidirectional TCP byte stream; it is not a VPN, a general UDP route or an HTTP/TLS authentication layer. Host/SNI/certificate expectations still belong to the destination application. Do not add newline conversions to a binary protocol. Listener bind failure, destination refusal, timeout and application denial are different stages; retain the failed stage before changing inputs.

`-v` logs transferred contents to stderr with direction markers, unlike `-d -d` diagnostic logging; it can disclose application data and does not provide a byte-exact capture. Omit it for routine routing. Starting this listener does not prove a later client used it, nor that the remote application executed anything.

Stop the tracked session and verify both the parent listener and known child connections close. A parent exit can leave established children alive; stop only identified owned processes under the agreed cleanup scope. Report unresolved handles rather than claiming cleanup from Ctrl-C alone.

See the [upstream Socat manual packaged by Debian](https://manpages.debian.org/trixie/socat/socat.1.en.html) for address/options and installed-version differences.
