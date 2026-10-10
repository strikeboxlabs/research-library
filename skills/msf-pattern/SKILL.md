---
name: msf-pattern
description: Generate Metasploit patterns and locate observed four-byte fragments with pattern_create and pattern_offset. Use for controlled buffer-layout measurements and ambiguous offset results.
---

# Metasploit pattern offsets

Read this entire SKILL.md before acting; reuse complete current context. Generate and locate using the same pattern family/length, require an exact unambiguous result and confirm its field boundary. For browser/Emscripten display corruption, read [WebAssembly fields](references/wasm-fields.md) fully first; that offset does not imply native control-flow execution.

Locate the installed pair: packages may expose `msf-pattern_create` and `msf-pattern_offset`, or the framework's `tools/exploit/pattern_create.rb` and `pattern_offset.rb`. Define `pattern_create` and `pattern_offset` as their executable paths; inspect each with `-h`.

Define `length` as a bounded size appropriate for the controlled fixture and `pattern_file` as a fresh output:

~~~bash
"$pattern_create" -l "$length" >"$pattern_file"
~~~

The generator prints an additional newline. Preserve the generated pattern separately from the line terminator required by the test protocol; measure what actually reaches the program. Do not assume the saved file contains exactly `length` bytes. Changing encoding, wrapping lines or including terminal decoration changes the input.

After observing four consecutive printable pattern bytes in the affected field or memory, define `observed4` in their original byte order:

~~~bash
"$pattern_offset" -l "$length" -q "$observed4"
~~~

Pass the same length and any custom `-s` character sets to both tools. The lookup defaults to length 8192 when omitted, which need not match the generated input. The reviewed parser treats a four-character query as literal bytes; longer hexadecimal queries have different parsing. For a register printed as an integer, reconstruct the relevant four memory bytes using the target's byte order. Do not feed an arbitrary 64-bit register string and assume an eight-byte search.

Require an **Exact match** and check for multiple matches. **Possible match** is a heuristic after an exact lookup failed; investigate transformation, truncation, query order or the wrong pattern family. Diagnostics and exit status alone are insufficient: these scripts can report errors without a failing exit code. Confirm the measured boundary with a short controlled marker before drawing a layout conclusion.

Offsets count from the start of the generated pattern. They describe the particular observed field: An overwritten executable-path string is not evidence of a saved return-address overwrite. Keep offsets tied to the exact binary, input path and framing. Metasploit and default pwntools cyclic patterns are different sequences; pair generation and lookup implementations.

See the upstream [generator](https://github.com/rapid7/metasploit-framework/blob/master/tools/exploit/pattern_create.rb), [lookup parser and match handling](https://github.com/rapid7/metasploit-framework/blob/master/tools/exploit/pattern_offset.rb), and [pwntools pattern families](https://docs.pwntools.com/en/stable/util/cyclic.html) when resolving generation/lookup differences.
