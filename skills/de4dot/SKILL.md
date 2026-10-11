---
name: de4dot
description: Transform a selected owned .NET assembly into a separate deobfuscated copy with de4dot. Use when obfuscated managed code needs preparation for a decompiler and original-symbol recovery or runtime compatibility is uncertain.
---

# Prepare a separate managed assembly for review

Read this entire SKILL.md before acting. Require the selected owned assembly, a fresh output path and a compatible installed de4dot launcher with its runtime/dependencies. Use an appropriately isolated analysis environment: de4dot can execute code from the input assembly and dependencies during processing. No conditional resources are required. Finish with input/output identity, processing result and independent assembly-reader findings; a saved file alone does not establish valid code.

Select the installed build before invoking it. Upstream has separate .NET Framework and .NET Core targets; a Windows executable is not automatically a Linux launcher, and an available newer `dotnet` runtime does not establish compatibility with an older target. Keep the build's companion files together. Define the Bash array `de4dot_cmd` as the verified launcher and required runtime arguments, `assembly` as the preserved input and `cleaned` as a new, different output file.

~~~bash
"${de4dot_cmd[@]}" --help
"${de4dot_cmd[@]}" "$assembly" -o "$cleaned"
status=$?
~~~

`-o` applies to the preceding input. Select one file rather than recursively processing an arbitrary directory. Retain the processing log and input/output hashes. A loader/framework failure needs the matching installed build/runtime; do not execute the input to diagnose it.

An `Unknown obfuscator` result can mean an unsupported obfuscator or an unobfuscated assembly. Deobfuscation and renaming do not reconstruct authentic source or original symbol names. Load the output in a compatible managed assembly reader/decompiler and compare the selected methods against the original. Reflection, resources or naming-dependent behavior may make automatic renaming unsuitable; upstream documents `--dont-rename` for that case. Preserve the original even after a successful transformation.

References: [upstream capabilities and execution caveat](https://github.com/de4dot/de4dot), [input/output option implementation](https://github.com/de4dot/de4dot/blob/master/de4dot.cui/CommandLineParser.cs), [build targets](https://github.com/de4dot/de4dot/blob/master/De4DotCommon.props).
