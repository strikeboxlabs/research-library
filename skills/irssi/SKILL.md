---
name: irssi
description: Connect to one approved IRC service with Irssi and inspect registration/version replies; distinguish client notices, server claims and successful protocol registration.
---

# Inspect an IRC registration reply

Read this entire SKILL.md before acting; reuse complete current context. Require the installed Irssi, a terminal, an approved server/port and a chosen nickname. Use a trusted profile whose startup scripts and connection settings are understood. Establish one connection below, retain its reply and close the owned session; a version string is a server claim, not patch verification.

Define `nickname` as the chosen IRC nickname. Start without configured automatic connections:

~~~bash
irssi --version
irssi --noconnect --nick "$nickname"
~~~

In Irssi, inspect `/help connect`. Replace SERVER and PORT with the chosen values in this client command; these are placeholders, not shell variables:

~~~text
/connect -! -noautosendcmd SERVER PORT
~~~

Use only options supported by installed help. `-!` avoids configured channel joins and `-noautosendcmd` suppresses that connection's configured automatic command; neither disables arbitrary startup scripts. This initiates IRC registration and exposes the selected nickname/client identity. For a service requiring TLS, use its verified TLS/hostname configuration rather than sending credentials through a plaintext sample.

Inspect the actual welcome/registration replies, server name, reported software and errors. An initial hostname lookup notice or 'not registered' reply can precede a later welcome; preserve their order rather than treating one line as the final state. An unrelated web-page reference to IRC does not prove a listener's protocol. A version claim alone does not establish a vulnerable or modified binary. A timeout, rejection or unresolved hostname is a specific connection gap.

Finish with endpoint/time, selected transport, registration result and exact relevant server claim. Use `/quit` to close this owned client when done. See the [CLI manual](https://manpages.debian.org/testing/irssi/irssi.1.en.html) and [connection help](https://irssi.org/documentation/help/connect/) for installed-version differences.
