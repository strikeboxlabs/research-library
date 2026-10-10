# Recover a Rust comparison's exact cryptographic inputs

Start with the entrypoint's import/inventory and selected decompilation, following the actual comparison path and necessary callees. Rust namespace names can identify a useful candidate without source debug information; stripped/generated names or ambiguous `main` need address selectors. Renaming a decompiler variable clarifies a hypothesis, not its proven type. Keep the language/endianness, function addresses and analysis limitations with the result.

For a stream-cipher password check, trace the input bytes/length, cipher creation, processed output length, comparison bytes and branch to success/failure. Rust strings/slices carry lengths; UTF-8 bytes and displayed characters differ. A decompiled `ctr` call may include return storage, enum values and slice pointer/length pairs rather than the high-level function's argument count. Match the actual library/compiler convention; do not infer key size by adding the IV length or treating a decompiler's `0x20` as an AES-256 selector.

In rust-crypto's API, `KeySize` selects AES-128/192/256 and key/IV are separate byte slices. A 16-byte key means AES-128; the 16-byte IV/counter does not extend it to 32 bytes. A 32-byte expected ciphertext may instead describe the processed input length. Check the comparison's exact conjunction/disjunction and instruction branch; failed length **or** mismatched bytes can reject, even when prose says both must fail. Follow newline trimming/encoding before assuming every printed password character belongs to the input.

## Export selected mapped bytes

Use Ghidra's mapped program address, not an assumed file offset or a process runtime address. Define `bytes_out` as a fresh private file, `data_addr` as the exact address seen in this imported program and `data_len` as its observed decimal byte count. This task requires the packaged [ReadSelectedBytes.java](../scripts/ReadSelectedBytes.java); retain the entrypoint's `headless`, `project_parent`, `project_name`, `program_name` and `skill_dir` context:

~~~bash
"$headless" "$project_parent" "$project_name" -process "$program_name" -noanalysis -readOnly \
  -scriptPath "$skill_dir/scripts" \
  -postScript ReadSelectedBytes.java "$bytes_out" "$data_addr" "$data_len"
~~~

The helper reads 1..4096 mapped bytes and refuses replacement; short/uninitialized/unmapped reads fail before output creation. Verify its `END bytes` program/address/count against the chosen range and actual output size, plus script errors. File existence alone is insufficient after an interrupted write. `-readOnly` keeps project changes unsaved; the helper still deliberately writes the selected external output. If the task needs more than 4096 bytes, choose reviewed bounded ranges rather than silently increasing the limit. An earlier analysis timeout remains a limitation.

Repeat only for the necessary key, initial counter and expected ciphertext, preserving each address/length/role separately. `getBytes` exports raw byte order; reversing every group because the binary is little-endian can corrupt the cryptographic input. If reconstructing from integer assignments, account for the actual store widths and endianness. Ghidra can contain applied relocations or manual edits: its mapped bytes are not automatically original file bytes. Correlate the relevant sections/mapping when that distinction matters.

In the GUI, selecting exactly the same range in Listing and `Copy Special -> Byte String (No Spaces)` is an alternative acquired byte representation; count the decoded bytes. A copied IV with 30 hex characters is only 15 bytes. Resolve the missing byte against the artifact or another complete verified capture, rather than padding/guessing it. Preserve full contiguous ciphertext, including embedded NULs; `x/s` or a string view can truncate it.

Finish with the supported cipher/counter contract, exact byte ranges and comparison logic. An offline decryption result is a candidate for this binary's predicate, not a verified privileged login. Re-encryption must match the complete extracted ciphertext; actual application acceptance and its resulting effects require the separate authorized operation.

Sources for consequential behavior: [Ghidra mapped-memory API](https://ghidra.re/ghidra_docs/api/ghidra/program/model/mem/Memory.html), [headless processing](https://github.com/NationalSecurityAgency/ghidra/blob/master/Ghidra/RuntimeScripts/support/analyzeHeadlessREADME.md), [rust-crypto AES API](https://github.com/DaGenix/rust-crypto/blob/master/src/aes.rs) and [counter processing](https://github.com/DaGenix/rust-crypto/blob/master/src/blockmodes.rs). Match the compiled library when its behavior differs.
