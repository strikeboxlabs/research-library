# Review an enabled Node inspector

Require the selected launch configuration and existing process/listener evidence from the owned system. Preserve the complete Node argv, effective service settings, PID/account, namespace and observed time. `--inspect` enables a debugger in addition to the application's own listeners; a familiar port alone does not identify it. `--inspect-brk` additionally pauses before user code. Inspect `NODE_OPTIONS` and wrappers without executing them.

An ExecStart line containing an inspector bind establishes configuration text, not that the current process used it or runs as root. Correlate current service/process identity, unit overrides and listener ownership. Root ownership of the script or output log is not the writer's effective identity. Missing PID data in a listener snapshot leaves that attribution unresolved.

A loopback bind limits direct network reachability in that namespace, but does not isolate the debugger from other local users. Existing forwarding, proxies or container mappings can change exposure. Treat an inspector as a privileged debugging interface with the process's authority. Record the exposure for removal or restricted administrative access under the owner's change process; do not attach or evaluate code merely to prove the finding.

An acquired inspector metadata response can name a script, UUID and WebSocket URL. These are separate from the application's HTTP URL and are not account/privilege proof. A WebSocket-expected response alone is not sufficient product identification. Keep such metadata private; a debugger UUID is not an authentication control.

For a monitoring worker, distinguish the configured interval from actual request completions and log rows. An interval scheduler does not by itself prevent overlapping asynchronous requests, and timeout/error handlers can produce more than one row for a failed request. Inspect the entire control flow before treating row count as request count or configured milliseconds as observed uptime.

Finish with the supported bind and identity evidence, any missing effective configuration, and the owner's exposure decision. Application success and debugger exposure are independent findings.

Reference: [Node's debugger security and connection model](https://nodejs.org/en/learn/getting-started/debugging).
