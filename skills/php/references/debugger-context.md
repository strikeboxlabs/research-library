# Inspect an existing Xdebug configuration and connection failure

Use for static review or diagnosis of an already configured owned PHP debugger. Require the actual PHP/Xdebug generation, CLI versus web SAPI, existing configuration/log evidence and intended IDE endpoint. An HTTP header claiming an extension version does not establish its effective debug settings, connection destination or authorization.

For a trusted existing CLI environment, inspect the extension without running the application:

~~~bash
"$php_bin" --ri xdebug
~~~

Missing extension output applies to this CLI's configuration only. Correlate the web worker's deployed ini/service configuration separately; CLI options do not silently change Apache/FPM. Xdebug 2 and 3 use different setting names/defaults, so do not apply a historical remote_* setting or port assumption to another generation. Current Xdebug 3 step debugging uses client_host/client_port and a default port 9003; verify installed effective values and mode rather than relying on defaults.

PHP's Xdebug engine connects outward to the IDE/debug client. The IDE listener, HTTP application and worker's network namespace are separate endpoints. Existing logs can identify attempted address/port, process ID and connection failure/success; a failed IDE connection does not establish absent HTTP service or safe application input. A configured localhost destination refers to the PHP process's namespace, which may be a container rather than the workstation. Source-path mapping and protocol negotiation remain distinct after transport connects.

Review destination-discovery policy and trusted inputs from the existing deployment configuration; do not introduce request-driven destination discovery to diagnose a missing IDE session. Debug interfaces can evaluate/change program state by design. An extension version alone is insufficient to classify a reachable evaluation interface as a particular vulnerability. Preserve the relevant configuration/connection evidence and resolve unintended debug exposure through a separately authorized configuration change.

Finish with generation/SAPI, actual destination, observed logs and remaining path/protocol gaps. Do not publish full debugger logs containing source paths or data. See [Xdebug step-debugging direction and settings](https://xdebug.org/docs/step_debug) and [Xdebug 2-to-3 changes](https://xdebug.org/docs/upgrade_guide).
