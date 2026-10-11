---
name: grpc-tools-protoc
description: Generate Python Protocol Buffer and gRPC bindings from a selected local proto schema using grpc_tools.protoc. Use when import roots, generated filenames or runtime compatibility obscure a local code-generation result.
---

# Generate bindings from the selected local schema

Read this entire SKILL.md before acting. Require a reviewed local schema with its imports, a trusted Python environment already containing grpcio-tools, and a fresh existing output directory. No conditional resources are required. Finish with compiler status, generated paths and schema/runtime gaps; generation alone does not establish compatibility with a deployed service.

Define `python_bin` as that interpreter, `proto_root` as the absolute import root, `schema` as the selected absolute .proto file beneath it and `output_dir` as the fresh directory. Confirm the module's local options/version, then generate both layers:

~~~bash
"$python_bin" -m grpc_tools.protoc --version
"$python_bin" -m grpc_tools.protoc -I "$proto_root" \
  --python_out="$output_dir" --grpc_python_out="$output_dir" "$schema"
status=$?
~~~

Check status and diagnostics before consuming output. Both flags are needed for Python messages plus gRPC service bindings. For a simple schema.proto input, expect schema_pb2.py and schema_pb2_grpc.py; nested inputs/imports can change the relative paths. Generation can overwrite files, so an old output directory can conceal partial or stale results. Preserve the schema/import inputs and list the newly generated files.

The import root controls how schema paths resolve. A missing imported .proto needs its actual local include root; installing the Python runtime package does not automatically provide every application's schema. Keep field numbers/types, package and service/method names faithful to the established contract. A locally guessed schema may compile yet select the wrong wire fields or RPC path.

The _pb2 module defines message/descriptor objects; the _pb2_grpc module imports it and supplies service stubs, servicer scaffolding and registration. Generated scaffolding does not implement the service's application behavior. Inspect generated imports and any version checks before an authorized integration step; grpcio-tools, protobuf and grpcio versions and Python module search paths can differ between environments. An import failure is distinct from a compiler error or remote RPC failure. Missing tools remain a prerequisite gap rather than an instruction to install them.

See the [official generation command](https://grpc.io/docs/languages/python/quickstart/#generate-grpc-code) and [generated-code reference](https://grpc.io/docs/languages/python/generated-code/).
