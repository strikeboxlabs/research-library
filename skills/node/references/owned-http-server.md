# Run the reviewed owned HTTP server

Require the complete reviewed application entry point/dependencies and an ordinary owning-user runtime. Inspect startup options/environment before launch; preload hooks can execute code. Define `node_bin` as the trusted installed interpreter and `entry` as the selected absolute script. Confirm its module style and version compatibility instead of treating a versioned source pathname as a target-image fact.

Keep configuration lookup separate from module lookup. A bare `require('dotenv').config()` normally reads `.env` relative to the process working directory; `require('./app')` resolves from the requiring file. Record the launch directory, explicit dotenv path and pre-existing environment before attributing the loaded settings. Do not print private environment values to establish that distinction. A supervisor's lifecycle-script string is configuration evidence, not proof that the shown command currently owns a listener.

An inspector option such as `--inspect=127.0.0.1:9229` describes the debugger bind, independently of the application's HTTP bind. Correlate each endpoint with the selected process and namespace; a local forwarding listener establishes only that local socket until the intended service response is observed. Inspector access permits powerful application operations and requires a separate reviewed debugging task.

~~~bash
"$node_bin" --version
"$node_bin" --check "$entry"
~~~

Check syntax status before launch. A syntax check does not resolve all dependencies, validate binds or exercise request behavior. Read its listen configuration: `listen(port)` without a host ordinarily binds an unspecified IPv6/IPv4 address, even when a hardcoded log prints a loopback URL. Choose explicit loopback for a local owned test; keep a separately approved external bind deliberate.

Run in a tracked foreground session:

~~~bash
"$node_bin" "$entry"
~~~

Wait for the actual listening event/address rather than an unconditional startup message. An occupied port or denied bind can fail after such a message. For a reviewed public response handler, request the exact ordinary route through the selected local address/port and compare status, Content-Type and expected public body. Successful listening alone does not establish the handler works; a response from a stale process does not establish this launch succeeded.

For a small owned CommonJS test, this **illustrative fragment** makes the bind and readiness observable after `server` has been created:

~~~javascript
server.listen(port, '127.0.0.1', function () {
  console.log(JSON.stringify(server.address()));
});
~~~

Define `port` as the selected unprivileged test port, or zero if the test consumer will use the reported assigned port. Stop only the tracked child when finished and verify its listener closes. A service manager can independently restart another instance, so keep foreground launch evidence separate from a deployed service's configuration and identity.

References: [listener address and readiness](https://nodejs.org/api/net.html#serverlistenport-host-backlog-callback), [HTTP server API](https://nodejs.org/api/http.html#class-httpserver), [syntax-check option](https://nodejs.org/api/cli.html#-c---check), [dotenv path selection](https://github.com/motdotla/dotenv#path), [Node debugger](https://nodejs.org/api/debugger.html).
