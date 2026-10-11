---
name: nats-server
description: Run an owned foreground NATS server on loopback for a bounded client connection check and interpret startup or trace evidence. Use to distinguish version queries, listener readiness and completed application exchanges.
---

# Run a local connection fixture

Read this entire SKILL.md before acting. Require the installed server, an unused approved local port and ownership of the foreground process. For a message exchange, also require an installed client, a reviewed local-only client context and an approved synthetic subject. Finish with listener address, actual client result, errors and confirmation that the owned process stopped.

~~~bash
nats-server --version
nats-server --help
~~~

`-V` enables trace logging; lowercase `-v`/`--version` prints version. Define `port` as the selected unused nonprivileged port. In the owned terminal:

~~~bash
nats-server -a 127.0.0.1 -p "$port"
~~~

The explicit bind keeps this unauthenticated fixture on loopback. Default broad binding, existing production configuration, JetStream persistence and cluster routes have different effects and are outside this fixture. Startup readiness establishes a listener, not successful client authentication or message delivery. An address-in-use error is a failed start; do not stop another service to reclaim its port.

For an application check, define `local_context` as the reviewed local-only context and `subject` as a synthetic test subject. Check the installed client's subscribe help. Start a subscriber in a second owned terminal:

~~~bash
nats --context "$local_context" --server "nats://127.0.0.1:$port" sub "$subject"
~~~

After subscription readiness, publish one public marker from a third terminal:

~~~bash
nats --context "$local_context" --server "nats://127.0.0.1:$port" pub "$subject" 'owned-fixture-marker'
~~~

Verify the subscriber received that marker; publisher success alone does not prove delivery. Stop the owned subscriber and foreground server with their terminal interrupts, then confirm process exit/listener closure. Do not use broad process-name kills.

Add `-V` only for synthetic traffic when protocol trace is specifically needed. Trace and packet evidence can expose message data or connection secrets; log redaction does not encrypt transport. A SYN followed by RST is no completed NATS exchange. See [server flags](https://github.com/nats-io/nats-server/blob/v2.11.4/server/opts.go) and [client publish/subscribe](https://github.com/nats-io/natscli#publish-and-subscribe).
