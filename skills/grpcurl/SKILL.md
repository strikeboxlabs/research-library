---
name: grpcurl
description: Discover a selected gRPC service's methods and message schema, or issue an established read-only RPC with grpcurl. Use when reflection, protobuf text versus JSON, TLS or response metadata obscures the API contract.
---

# Inspect the selected gRPC contract

Read this entire SKILL.md before acting. Establish the endpoint, transport and descriptor source; retain each status and schema result. For a selected read-only method or authentication-metadata discrepancy, read [RPC messages and metadata](references/messages-and-metadata.md) fully first. Reflection discovery alone does not establish method permission or application health.

Check `grpcurl -version` and `grpcurl -help`. Define `endpoint` as the known host:port and `service`/`symbol` from observed fully qualified names. For a TLS endpoint supporting reflection:

~~~bash
grpcurl -connect-timeout 5 -max-time 20 "$endpoint" list
grpcurl -connect-timeout 5 -max-time 20 "$endpoint" list "$service"
grpcurl -connect-timeout 5 -max-time 20 "$endpoint" describe "$symbol"
~~~

Check each status before selecting the next observed symbol. Describe the request and response message types as needed; printed descriptors need not be the original source file. Schema fields do not describe all authentication, authorization or business rules.

For an established non-TLS service, add `-plaintext` before the endpoint. This selects cleartext HTTP/2; it is different from `-insecure`, which disables TLS verification. Use the intended trusted CA/client certificate for TLS rather than disabling checks. Port 50051 is only a service lead.

If reflection is unavailable, require the matching local `.proto` sources and their imports or a compiled descriptor set. `-proto`/`-import-path` and `-protoset` select those sources; local list/describe results then describe supplied files, not proof of the server's current methods. Do not enable reflection or fabricate a schema to repair the client.

Finish with the endpoint/transport, descriptor origin, observed methods/messages and incomplete or denied discovery. See [grpcurl usage](https://github.com/fullstorydev/grpcurl) and [current option definitions](https://github.com/fullstorydev/grpcurl/blob/master/cmd/grpcurl/grpcurl.go).
