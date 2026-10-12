---
name: winchecksec
description: Inspect a selected Windows PE file's static mitigation metadata from Linux with winchecksec. Use when ASLR, NX, stack-cookie, signature or architecture-specific report states are being confused with runtime protections.
---

# Read a selected PE mitigation report

Read this entire SKILL.md before acting. Require the installed winchecksec build and an acquired local PE copy; no conditional resources are required. Finish with the input identity, tool version, status, reported states and unresolved checks. This static parse does not launch the specimen or establish the running service's protections.

Define `checker` as the actual installed executable, `binary` as the selected absolute PE path, and `report`/`diagnostics` as fresh private outputs:

~~~bash
"$checker" --version
"$checker" --json "$binary" > "$report" 2> "$diagnostics"
status=$?
~~~

Inspect the saved status and diagnostics before parsing the report. The documented JSON output is an array of per-file objects containing `path` and `mitigations`; retain each presence value and any explanation. Plain text is the default when `--json` is omitted. A file-load/parse error is a gap, not an all-absent report. The reviewed CLI stops on an error; earlier plain-text output from a multi-file invocation does not prove later files were checked. A fresh output can still be empty after failure.

An **illustrative** `nx: Present, safeSEH: NotApplicable` reports two different conclusions. Preserve `NotApplicable`, `NotImplemented` and unknown states rather than converting them into false. SafeSEH applies to x86-32; the same expectation does not carry to a 64-bit PE.

Dynamic-base support and ASLR are distinct fields: stripped relocations affect the latter. NX describes static compatibility, not the permissions of every runtime page. A reported stack cookie does not establish coverage of every function. Resolve consequential findings against the installed build's explanations and the actual target architecture/loader policy before making a runtime claim.

Signature checking depends on the build/backend; the upstream guide's Linux limitation and implementation revisions need reconciliation on the installed image. A presence label alone does not establish the intended publisher, current certificate trust or server binary identity. Keep the file digest/provenance and any independent signing/runtime evidence separate; a matching menu or filename is insufficient.

References: [usage and build requirements](https://github.com/trailofbits/winchecksec), [CLI status/output handling](https://github.com/trailofbits/winchecksec/blob/master/main.cpp) and [mitigation implementation](https://github.com/trailofbits/winchecksec/blob/master/checksec.cpp).
