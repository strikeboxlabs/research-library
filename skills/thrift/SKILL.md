---
name: thrift
description: Generate Apache Thrift bindings from a reviewed IDL and diagnose compiler/runtime, namespace and wire-protocol mismatches. Use when a custom RPC client builds incorrectly or transport success is being confused with a completed method call.
---

# Generate bindings from the actual contract

Check `thrift -version` and `thrift -help`; this is the Apache Thrift compiler, separate from the language runtime library. Obtain the service's actual reviewed `.thrift` file and its includes. Preserve method names, argument field IDs/types, result types and declared exceptions. In `string ReadLogFile(1: string filePath)`, `1` is the argument's field ID, not a method number or TCP port. A namespace selects a language package; it does not select a network endpoint.

Define `idl` as the absolute contract path, `include_dir` as its reviewed include root and `generated` as a fresh nonexistent output directory. For Go bindings:

~~~bash
mkdir -- "$generated" &&
  thrift -I "$include_dir" -r --gen go -out "$generated" "$idl"
~~~

`-r` also generates included contracts. `-out` writes beneath the chosen output location without adding the usual `gen-go` wrapper; namespace/package subdirectories still apply. `-o` instead chooses the parent of that wrapper. Existing output can be overwritten, so keep each generation separate until reviewed. A missing include or generator error leaves incomplete output, even if some files exist.

Generation creates bindings, not a running server or a verified client. Pair generated code with the corresponding compatible language runtime; read compiler/runtime version diagnostics before editing generated methods. Generated Go imports must resolve through the project's module/workspace arrangement. Copying them into the Go installation's `src` directory is not a portable module fix. For multi-file contracts, inspect the generator's installed package-prefix options and the actual imports it emits.

## Match the wire and application layers

Read the deployed service configuration/source to determine endpoint, TLS, transport framing, protocol encoding and any service multiplexing. Binary and compact protocols are different. Buffered I/O is not the same as framed transport; matching a port alone does not resolve either choice. Use the [language tutorial](https://thrift.apache.org/tutorial/) appropriate to the generated bindings and installed runtime.

In the Go client, constructing a TSocket object does not open a connection; `Open` is a separate operation. An open transport proves only that stage. A method exception, disconnect or decoding error needs protocol/contract evidence before changing arguments. An application success string does not prove its internal file or command operation succeeded.

A path argument is interpreted by the server's handler, in its filesystem/working-directory context. A method named `ReadLogFile` can still create, truncate or process output and invoke other programs. Review the handler's effects before making even a diagnostic RPC; do not infer read-only behavior from its name. Keep code generation, client compilation, connection and method execution as separately evidenced outcomes.

Use the [IDL reference](https://thrift.apache.org/docs/idl), [compiler options](https://github.com/apache/thrift/blob/master/compiler/cpp/src/thrift/main.cc) and [Go tutorial](https://thrift.apache.org/tutorial/go) for contract, generation and transport details.
