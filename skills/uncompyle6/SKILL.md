---
name: uncompyle6
description: Recover candidate Python source from one acquired supported pyc or pyo file without executing it. Use when bytecode version, reconstructed headers or decompiler control-flow errors limit a static review.
---

# Decompile one selected bytecode artifact

Read this entire SKILL.md before acting. Require a preserved acquired bytecode file, a trusted installed decompiler/runtime and a disposable private analysis environment. Establish the bytecode version separately from the interpreter running the decompiler. Finish with status, diagnostics, recovered scope and unresolved semantics; missing support leaves decompilation incomplete.

Inspect the installed help and package version. Upstream support includes released bytecode through Python3.8; a modern host interpreter does not imply support for its own bytecode. Select the release/environment compatible with the tool's host requirements and the artifact's magic number. For a PyInstaller input, extract the selected member first and retain any skipped-PYZ or repaired-header warning; do not pass the executable itself to this bytecode procedure.

Define `decompiler` as the verified executable, `bytecode` as the absolute selected file, and `recovered`/`errors` as fresh private output paths:

~~~bash
umask 077
"$decompiler" "$bytecode" > "$recovered" 2> "$errors"
decompile_status=$?
~~~

Read both streams and the complete output. Reported Python bytecode version and embedded filename are artifact metadata; the decompiled-from interpreter describes the tool environment. A generated header or partial function does not prove complete source recovery. Parser failures, unsupported magic/opcodes and omitted functions remain gaps.

Treat indentation, loops, exception branches and reconstructed values as candidates. Compare decisive control flow with the original bytecode or an independent compatible decompiler. Comments and original formatting are generally absent. A compatible syntax check can establish parseability, not behavioral equivalence; do not import or execute recovered application code as verification. Preserve the original artifact and unsuccessful result before selecting another supported parser or prepared environment.

Reference: [uncompyle6 usage, supported bytecode and control-flow limitations](https://github.com/rocky/python-uncompyle6).
