# Send a selected read-only RPC and interpret metadata

Require the established endpoint/transport, matching descriptors, selected non-mutating method and request data under its actual field contract. Select the intended existing account's authentication mechanism; a method name alone does not establish that it is read-only. Do not invoke registration/login merely to discover a schema or replay a credential acquired from unrelated records.

Define `endpoint` as host:port, `method` as the observed fully qualified Service/Method, and `request_file` as a private local JSON request. For an already established TLS/reflection endpoint:

~~~bash
grpcurl -connect-timeout 5 -max-time 20 -format json -d @ \
  "$endpoint" "$method" <"$request_file"
status=$?
~~~

Put options before the endpoint. For an established cleartext service add `-plaintext`; keep any supplied descriptor/TLS requirements from discovery. `-format text` instead expects protobuf text syntax, not JSON with its punctuation removed. A protobuf string ID stays a string even when it looks numeric. Use the current response's correlated identifier rather than a stale example.

Separate process status, gRPC status, response message and application-level error text. A message saying authorization failed can still be carried in a successfully completed RPC. Inspect existing verbose output or add `-v` to this same authorized read when necessary; `-vv` adds further detail/timing. Headers and response trailers are metadata outside the protobuf body and can contain secrets. Keep those observations private and report only relevant redacted fields.

The documented `-H 'name: value'` metadata option applies to reflection and the RPC. On implementations supporting them, `-rpc-header` and `-reflect-header` limit that scope. Use the service's established metadata key; a value shaped like a JWT does not establish its signature, validity or account rights. For a pre-provisioned secret in an environment variable, supported `-expand-headers` permits a single-quoted literal `${NAME}` placeholder without putting its expanded value in argv; verbose logs can still expose it. Verify local support and the actual service contract before choosing these options.

Finish with the selected read's application result, correlated request identity and remaining transport/schema/authentication gaps. Transport success, returned trailers or a changed response are separate observations. No database-injection or command-execution payload is needed for this task.

References: [RPC input and metadata usage](https://github.com/fullstorydev/grpcurl), [format, timeout, verbosity and metadata options](https://github.com/fullstorydev/grpcurl/blob/master/cmd/grpcurl/grpcurl.go).
