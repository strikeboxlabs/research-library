---
name: protoc
description: Decode one acquired Protocol Buffer message offline with its matching schema using the native protoc compiler, separating protobuf text from JSON and HTTP or gRPC framing.
---

# Decode a known-schema message

Read this entire SKILL.md before acting. Require the acquired body, reviewed matching schema and imports, fully qualified message type and installed protoc supporting that syntax. Finish with original identity, decoder status and supported fields or the exact schema/framing gap. This task does not call the service.

Define `proto_root` as the absolute import root, `schema` as the selected absolute .proto file under it, `message_type` as its actual fully qualified type, `body` as the unframed binary message and `decoded` as a fresh private output:

~~~bash
protoc --version
protoc -I "$proto_root" --decode="$message_type" "$schema" < "$body" > "$decoded"
status=$?
~~~

Retain decoder diagnostics and status alongside output. HTTP headers, JSON error bodies and gRPC message framing are not raw protobuf messages. A schema/import/type error and a malformed body require different recovery. Empty text can represent a message with no populated fields; absence of printed values does not alone establish a failed request.

Output is protobuf text format, not JSON or fixed whitespace columns. Preserve nested/repeated fields and quoted string syntax; splitting with awk and deleting quotes can silently change values. Successful decoding supports this schema's interpretation, not publisher identity or completeness of the application's contract.

For an acquired Twirp exchange, identify status and content type independently: its errors are JSON even when the requested successful representation was protobuf. A comment stating a required request field does not prove a shown empty request supplied it or that the deployed service enforces it.

See [protoc decode/import options](https://github.com/protocolbuffers/protobuf/blob/main/src/google/protobuf/compiler/command_line_interface.cc), [protobuf text format](https://protobuf.dev/reference/protobuf/textformat-spec/) and [Twirp wire contract](https://twitchtv.github.io/twirp/docs/spec_v7.html).
