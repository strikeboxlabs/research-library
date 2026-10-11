---
name: wat2wasm
description: Compile reviewed WebAssembly text into a fresh binary module with WABT wat2wasm. Use when WAT syntax, export/type contracts or proposal support must be established separately from host execution.
---

# Compile the selected text contract

Read this entire SKILL.md before acting. Require reviewed WAT, the intended module contract and a trusted installed tool. Preserve input, select a fresh output and finish with compiler diagnostics and artifact checks. No conditional resources are required; compilation does not execute the module or its host.

Check `wat2wasm --version` and `--help`. Define `wat_file` as the reviewed absolute input path and `wasm_file` as a fresh output path:

~~~bash
wat2wasm "$wat_file" -o "$wasm_file"
status=$?
~~~

Check status and stderr before using the output; an old file surviving a failed command is not the new artifact. Wat2wasm parses/checks the text under its enabled feature set and writes a binary; do not use `--no-check` as a normal repair. An unsupported proposal needs matching documented compiler and consumer support, not blanket enable-all settings.

An illustrative module exporting a no-argument i32 function whose body is `i32.const 7` supplies that type/value contract. It does not reproduce another module's imports, memory, tables, globals or start function merely because its export name matches. Preserve the complete intended module design and inspect the resulting binary with an available static Wasm reader when exact exports matter.

Decompiler C-like text is not WAT. A successful compile establishes a module artifact, not successful instantiation, permitted host imports or any deployment side effect. A host using the result to launch a process is a separate host program decision. Select any later runtime test explicitly and keep privileged application inputs separate from this local compilation task.

References: [WABT tools and feature support](https://github.com/WebAssembly/wabt), [wat2wasm CLI contract](https://github.com/WebAssembly/wabt/blob/main/test/help/wat2wasm.txt).
