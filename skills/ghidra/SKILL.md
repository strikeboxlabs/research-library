---
name: ghidra
description: Decompile selected native-binary functions from the CLI with Ghidra headless analysis. Recover exact Rust cipher/compare bytes or trace privilege guards, database fields, filename construction and file operations while separating reconstructed code from runtime evidence.
---

# Ghidra headless function analysis

Read this entire SKILL.md before acting; reuse complete current context. Use an acquired binary copy and the installed Ghidra/JDK pair. The required helper [scripts/DecompileSelected.java](scripts/DecompileSelected.java) inventories functions or exports selected decompilations; use it for the procedure below. For interpreting database-to-file code, read [file data flow](references/file-data-flow.md) fully before that analysis. For a Rust stream-cipher predicate or selected key/IV/ciphertext range, read [Rust cryptographic inputs](references/rust-crypto.md) fully; its byte-export task requires `scripts/ReadSelectedBytes.java`. Finish with the selected function addresses, recovered logic and unresolved calls/analysis failures; decompiled text is not observed execution.

Define `headless` as the verified installed `support/analyzeHeadless` launcher and `skill_dir` as this package's absolute directory. Use the installed release's JDK requirements; do not copy an old walkthrough's install commands. Define `binary` as one local executable/object, `project_parent` as an existing private working directory, and `project_name` as a fresh project name. Ghidra imports a program database without executing the specimen. It writes that project and analysis logs.

First inventory discovered function names and entry addresses. Define `inventory`, `analysis_log` and `script_log` as fresh absolute output paths in a private directory:

~~~bash
"$headless" "$project_parent" "$project_name" -import "$binary" \
  -analysisTimeoutPerFile 120 -scriptPath "$skill_dir/scripts" \
  -log "$analysis_log" -scriptlog "$script_log" \
  -postScript DecompileSelected.java "$inventory"
~~~

Confirm the imported format, language/endianness and analysis diagnostics; do not force an architecture merely to obtain output. A raw blob requires its known load address/language, outside this automatic-import recipe. The helper's `END inventory` marks completed enumeration of **discovered** functions, not proof all code was found. An analysis timeout still permits post-scripts and leaves partial analysis; retain that limitation.

Select one or a few actual functions from that inventory. Define `program_name` as the exact project program name reported by import, `selector` as a unique function name or `@` followed by its entry address, and `decompiled` as a fresh absolute file. For example, `main` is only useful if that symbol exists; stripped files may have generated names. Reuse the imported analysis:

~~~bash
"$headless" "$project_parent" "$project_name" -process "$program_name" -noanalysis \
  -scriptPath "$skill_dir/scripts" -postScript DecompileSelected.java "$decompiled" "$selector"
~~~

Append additional selectors as separate arguments to follow necessary callees. The helper refuses an existing output file, rejects ambiguous names and gives each selected function a 60-second decompilation budget. Inspect per-function status, diagnostics and final `END selected` counts, not just the launcher's exit code or output-file existence. Missing functions, partial writes, `FAILED` and absent end markers require narrower claims. A false timeout value in a `-noanalysis` run does not erase a prior import timeout.

Generated variable names/types are hypotheses. Reused register storage can merge distinct values into one displayed variable: trace each definition and use, the call's argument types and the controlling branch before assigning it one meaning. Preserve original addresses, widths, signedness, byte-bounded strings and their termination; check decisive operations against the disassembly when types/casts look inconsistent. A global rename does not resolve conflicting uses. Ghidra's interactive split-variable action applies only to eligible merged locals; this headless helper exports analysis and does not perform that action. Keep a selected-call data-flow note when the reconstruction remains ambiguous. Follow relevant helpers before attributing their effects from names alone. `main` is not necessarily the ELF entrypoint or the first code executed. Reuse this project for deeper work; do not overwrite an unrelated project to retry.

See the [headless options](https://github.com/NationalSecurityAgency/ghidra/blob/master/Ghidra/RuntimeScripts/support/analyzeHeadlessREADME.md) and [decompiler API](https://ghidra.re/ghidra_docs/api/ghidra/app/decompiler/DecompInterface.html) for installed-release differences.
