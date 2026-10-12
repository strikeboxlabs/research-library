# Resolve a selected Go string boundary

Use an already imported acquired Go binary and the entrypoint's function inventory/decompilation procedure. Select a nonsecret endpoint, pathname or diagnostic label needed for the question. Record the actual architecture, compiler evidence and call/field consuming it; a generated DAT name or nearby printable bytes is not a field association.

Go strings have byte lengths, not a required C-style NUL terminator. The runtime represents a string with a data pointer and length; its placement in a reconstructed object or call depends on the compiler/ABI and field layout. Trace both values from the actual assignments and their consumer. A pointer to an address in one field and a length store in another field are not automatically one descriptor. Register/stack calling conventions can differ from an old screenshot, and neighboring strings can be packed together.

Define `data_address` as that supported mapped address, `byte_count` as its positive decimal length (at most4096 for this helper), and `bytes_file` as a fresh absolute output. Reuse `headless`, `project_parent`, `project_name`, `program_name` and `skill_dir` from the imported project:

~~~bash
"$headless" "$project_parent" "$project_name" -process "$program_name" -noanalysis \
  -scriptPath "$skill_dir/scripts" \
  -postScript ReadSelectedBytes.java "$bytes_file" "$data_address" "$byte_count"
~~~

The required helper reads exactly that mapped range without running the specimen and refuses an existing output. Require its `END bytes` marker and matching file count; an exception, short/unmapped read or unresolved descriptor leaves the value incomplete. A zero-length string needs no export. Keep raw bytes before decoding: the length can differ from Unicode character count. Do not trim an arbitrary number of trailing characters or read until the next visible terminator.

**Illustrative:** an endpoint field points to bytes spelling `localhost:6379` followed by another label. A supported length14 selects only the endpoint; adjacent label bytes are not part of it. This does not establish a connection, hostname resolution, authentication or service health. Finish with the pointer/length/consumer association and unresolved reconstruction; no connection or specimen execution is needed.

See [Go string byte semantics](https://go.dev/ref/spec#String_types) and [runtime string representation](https://go.dev/src/runtime/string.go); use the specimen's compiler/ABI when matching that implementation.
