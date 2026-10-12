---
name: ghidra
description: Decompile selected native-binary functions from the CLI with Ghidra headless analysis. Recover exact Rust cipher/compare bytes or trace privilege guards, database fields, filename construction and file operations while separating reconstructed code from runtime evidence.
---

# Ghidra headless function analysis

Read this entire SKILL.md before acting; reuse complete current context. Use an acquired binary copy and the installed Ghidra/JDK pair. The required helper [scripts/DecompileSelected.java](scripts/DecompileSelected.java) inventories functions or exports selected decompilations; use it for the procedure below. For selected file-producing code, including database exports or native logging helpers, read [file data flow](references/file-data-flow.md) fully before that analysis. For a Rust stream-cipher predicate or selected key/IV/ciphertext range, read [Rust cryptographic inputs](references/rust-crypto.md) fully; its byte-export task requires `scripts/ReadSelectedBytes.java`. For a selected Go endpoint/label whose string boundary is unclear, read [Go string fields](references/go-string-fields.md) fully; exact byte export requires [scripts/ReadSelectedBytes.java](scripts/ReadSelectedBytes.java). Finish with the selected function addresses, recovered logic and unresolved calls/analysis failures; decompiled text is not observed execution.

Define `headless` as the verified installed `support/analyzeHeadless` launcher and `skill_dir` as this package's absolute directory. Use the installed release's JDK requirements; do not copy an old walkthrough's install commands. Define `binary` as one local executable/object, `project_parent` as an existing private working directory, and `project_name` as a fresh project name. Ghidra imports a program database without executing the specimen. It writes that project and analysis logs.

For an acquired PAM module and configuration snapshot, read [PAM module review](references/pam-module-review.md) fully before following authentication branches. The required decompiler helper exports the selected functions; this task does not load the module or submit authentication attempts.

First inventory discovered function names and entry addresses. Define `inventory`, `analysis_log` and `script_log` as fresh absolute output paths in a private directory:

~~~bash
"$headless" "$project_parent" "$project_name" -import "$binary" \
  -analysisTimeoutPerFile 120 -scriptPath "$skill_dir/scripts" \
  -log "$analysis_log" -scriptlog "$script_log" \
  -postScript DecompileSelected.java "$inventory"
~~~

Confirm the imported format, language/endianness and analysis diagnostics; do not force an architecture merely to obtain output. A raw blob requires its known load address/language, outside this automatic-import recipe. The helper's `END inventory` marks completed enumeration of **discovered** functions, not proof all code was found. An analysis timeout still permits post-scripts and leaves partial analysis; retain that limitation.

An acquired ELF kernel object can be imported for static function review through this same task. Its filename or a neighboring source listing does not establish that it matches the loaded module. Keep acquisition identity and source-to-object association unresolved unless separately evidenced. Do not load a specimen to make static analysis succeed.

For acquired Windows PE files, match any PDB to the binary's recorded PDB filename, GUID/signature and age before trusting its names or types. An OS version label or matching PDB basename alone is insufficient. Retain the selected binary identity, symbol match and import diagnostics; do not force a mismatched PDB to obtain plausible names. Structure definitions from a different driver/build remain hypotheses. A Ghidra image address, file offset and live address are different coordinates; importing symbols does not establish a loaded module's runtime location. See [PDB matching and loading](https://github.com/NationalSecurityAgency/ghidra/blob/master/Ghidra/Features/PDB/src/main/help/help/topics/Pdb/LoadPDB.html).

Select one or a few actual functions from that inventory. Define `program_name` as the exact project program name reported by import, `selector` as a unique function name or `@` followed by its entry address, and `decompiled` as a fresh absolute file. For example, `main` is only useful if that symbol exists; stripped files may have generated names. Reuse the imported analysis:

~~~bash
"$headless" "$project_parent" "$project_name" -process "$program_name" -noanalysis \
  -scriptPath "$skill_dir/scripts" -postScript DecompileSelected.java "$decompiled" "$selector"
~~~

Append additional selectors as separate arguments to follow necessary callees. The helper refuses an existing output file, rejects ambiguous names and gives each selected function a 60-second decompilation budget. Inspect per-function status, diagnostics and final `END selected` counts, not just the launcher's exit code or output-file existence. Missing functions, partial writes, `FAILED` and absent end markers require narrower claims. A false timeout value in a `-noanalysis` run does not erase a prior import timeout.

Generated variable names/types are hypotheses. Reused register storage can merge distinct values into one displayed variable: trace each definition and use, the call's argument types and the controlling branch before assigning it one meaning. Preserve original addresses, widths, signedness, byte-bounded strings and their termination; check decisive operations against the disassembly when types/casts look inconsistent. A global rename does not resolve conflicting uses. Ghidra's interactive split-variable action applies only to eligible merged locals; this headless helper exports analysis and does not perform that action. Keep a selected-call data-flow note when the reconstruction remains ambiguous. Follow relevant helpers before attributing their effects from names alone. `main` is not necessarily the ELF entrypoint or the first code executed. Reuse this project for deeper work; do not overwrite an unrelated project to retry.

An `in_stack_00...` input can indicate missing stack parameters in the reconstructed signature. Inspect the caller's argument preparation, callee reads and actual calling convention before redefining that signature; the generated name is a diagnostic lead, not a declaration of the original source. A locally defined function named `random` need not be libc's random implementation. When interpreting a scanf call, recover its exact format bytes and destination capacity: an unresolved format address alone cannot establish whether a field width exists. Account for the terminating NUL for string conversions and preserve return/error checks. A nearby stack offset or decompiler array declaration alone does not prove the original buffer's size.

For line-reading code, fgets retains a newline if one is read; it does not manufacture a newline at EOF or after a capacity-limited read. Trace its return, capacity, actual input bytes and later strlen together. NUL-terminated string length differs from acquired byte count. Likewise, zero bytes between small values can reflect little-endian multi-byte integers rather than separate terminated characters; use the consumer's load width/stride to establish the representation.

For bounded formatting, recover snprintf's destination, size argument, exact format and source bytes at the real call. A prose simplification that omits the size changes the prototype and cannot establish the original bound. Trace subsequent comparison length separately from formatted string length and destination capacity.

See the [headless options](https://github.com/NationalSecurityAgency/ghidra/blob/master/Ghidra/RuntimeScripts/support/analyzeHeadlessREADME.md), [decompiler API](https://ghidra.re/ghidra_docs/api/ghidra/app/decompiler/DecompInterface.html), [glibc line input](https://sourceware.org/glibc/manual/latest/html_node/Line-Input.html) and upstream [potential-analysis diagnostics](https://github.com/NationalSecurityAgency/ghidra/blob/master/Ghidra/Features/Decompiler/ghidra_scripts/FindPotentialDecompilerProblems.java) for installed-release differences. The latter diagnostic script is interactive and cannot replace this package's required headless helper.
