---
name: quiche-client
description: Make one selected HTTP/3 request with the quiche example client and preserve response evidence. Use when UDP reachability, historical http3-client names or stdout redirection obscure protocol negotiation and binary downloads.
---

# Retrieve the selected HTTP/3 resource

Read this entire SKILL.md before acting. Require an existing trusted Linux client, one exact authorized HTTPS URL, its hostname/CA trust and fresh private output paths. All working instructions are inline. Finish with client identity, request status/headers, complete body and transfer/integrity limits; UDP reachability alone does not establish HTTP/3.

Define client as the verified executable and inspect its --help. Current quiche apps use quiche-client; older builds used http3-client under examples. Do not infer its absolute path or option support from an old walkthrough. Record the build revision and actual help. The example app is intended for testing rather than production reliability. If absent, resolve provisioning separately: source acquisition, Cargo compilation and program execution are distinct steps, with revision-specific Rust/native build prerequisites and executable build scripts. Installing this skill does not build or install quiche.

Define url as the exact resource URL with a nonempty final path component, response_dir as a newly created private empty owned directory, and console/log as fresh private files outside that directory. For a verified build supporting these options:

~~~bash
umask 077
RUST_LOG=debug "$client" --http-version HTTP/3 --method GET \
  --idle-timeout 10000 --dump-responses "$response_dir" "$url" \
  >"$console" 2>"$log"
status=$?
~~~

Use one URL/request. The idle timeout is milliseconds without progress, not a total process deadline; apply the task's overall session budget. Keep TLS verification and the intended hostname. If a private origin CA is needed, use the installed build's trust-origin-ca-pem option with the approved CA. No-verify changes authentication assurances; it is not a DNS repair.

Inspect status, diagnostics and HTTP/3 response headers including :status from this same request. The selected HTTP/3 option restricts the offered application protocol in the reviewed client; a completed HTTP error response still needs application interpretation. A handshake failure differs from an incomplete HTTP response or local parsing error. An HTML login/error page can arrive under a PDF filename. Do not infer current browser support or protocol identity from a port443 label.

Inspect the created file before accepting it. The reviewed dump writer uses the URL's last path segment and creates/truncates that destination; it does not preserve remote directory structure. Use a fresh directory to prevent collisions, and inspect unusual path segments instead of treating remote names as trusted paths. Verify actual bytes/size, intended format and an independently supplied digest when available. The example writer can discard a write error, so zero client status alone is insufficient proof of a complete saved artifact.

Use dump-responses for binary data. Ordinary stdout follows a text sink, and dump-json wraps/caps payload data; neither is a verified binary download merely because its redirect ends .pdf. Preserve console/log separately and report partial files when the bounded process is interrupted. Stop only the tracked client when its budget ends.

Primary execution references: [quiche apps/build instructions](https://github.com/cloudflare/quiche), [client options](https://github.com/cloudflare/quiche/blob/master/apps/src/args.rs), [handshake/request completion](https://github.com/cloudflare/quiche/blob/master/apps/src/client.rs), [response writer and text sink](https://github.com/cloudflare/quiche/blob/master/apps/src/common.rs).
