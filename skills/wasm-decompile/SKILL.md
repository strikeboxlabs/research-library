---
name: wasm-decompile
description: Read an acquired WebAssembly module as WABT's decompiled text. Use to inspect exports and return/control flow when C-like output, inferred names or a host's later actions could be mistaken for recovered source or runtime proof.
---

# Inspect the selected Wasm without running it

Read this entire SKILL.md before acting. Require the preserved complete module and a trusted WABT build that actually supplies wasm-decompile. Select fresh output, retain parser diagnostics and finish with the supported static finding and missing host/runtime evidence. No conditional resources are required.

Check `wasm-decompile --version` and `--help` for the installed tool. The command has existed in historical WABT builds; do not assume every current package supplies it or reinstall an obsolete release just to match a walkthrough. Define `module` as the acquired module's absolute working-copy path and `report` as a fresh output path:

~~~bash
wasm-decompile "$module" -o "$report"
status=$?
~~~

Inspect status/stderr and the complete report before accepting it. A failed parse, unsupported proposal or truncated module leaves analysis incomplete; preserve the original and resolve the build/feature mismatch instead of ignoring validation errors. This tool reads/decompiles the module rather than invoking its exported functions.

The output is readable decompiler syntax, not WAT or recovered C source. Names may be taken from module metadata or generated; inferred pointer/structure presentations are interpretation aids. Do not send this text to wat2wasm as though it were a round-trip format.

For an illustrative `export function status():int { return 7 }`, record the observed export/type and constant behavior in that static representation. Also inspect imports, start functions, memory and other relevant paths before claiming the whole module is inert. A host may use a returned value to choose its own script/process action; the constant alone does not perform that host action. Match the preserved module to the host's actual load/export contract before any runtime claim.

References: [WABT decompiler language and limits](https://github.com/WebAssembly/wabt/blob/1.0.23/docs/decompiler.md), [historical CLI reader/validation/output](https://github.com/WebAssembly/wabt/blob/1.0.23/src/tools/wasm-decompile.cc).
