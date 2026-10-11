---
name: patchelf
description: Inspect or change the ELF interpreter and runtime library path of a selected owned binary with PatchELF. Use when an acquired loader/library bundle and working-directory assumptions prevent a controlled program from starting.
---

# Select the intended loader and library path

Read this entire SKILL.md before acting. Require the installed PatchELF, an owned ELF copy, its preserved original and trusted ABI-compatible loader/libraries. Select inspection or the requested metadata change below. No conditional resources are required. Finish with status, before/after ELF fields and artifact identity; metadata changes do not establish runtime compatibility or authority.

Define `binary` as the absolute acquired ELF path. Inspect this installation's version/options and the actual fields:

~~~bash
patchelf --version
patchelf --help
patchelf --print-interpreter "$binary"
patchelf --print-rpath "$binary"
patchelf --print-needed "$binary"
~~~

Keep each result/status separately. A static ELF can lack an interpreter or dynamic section; a failed query is not an empty, successfully inspected field. Needed names are direct dependencies, not a fully resolved runtime library inventory. These queries inspect metadata without executing the target.

For a requested change, define `working_binary` as a separately verified owned copy outside system/application deployment paths, `loader` as the existing absolute trusted loader path and `library_dir` as the absolute trusted library directory:

~~~bash
patchelf --set-interpreter "$loader" "$working_binary" &&
patchelf --set-rpath "$library_dir" "$working_binary" &&
patchelf --print-interpreter "$working_binary" &&
patchelf --print-rpath "$working_binary"
~~~

PatchELF edits that file in place. A second-step failure can leave the first edit applied; inspect the copy rather than assuming rollback. Retain the original fingerprint, resulting fingerprint and actual selected architecture/fields. Avoid changing a privileged/deployed executable merely to investigate an acquired artifact.

A relative interpreter such as `./libc/ld.so` is resolved from the launch working directory, not automatically beside the executable. An ordinary `./libc` library path has the same working-directory dependency. For a deliberately relocatable bundle, the loader's literal `$ORIGIN/libc` expands relative to the ELF containing that path; preserve it with single quotes if chosen. The interpreter still needs its own valid path. Do not substitute `$ORIGIN` into the interpreter string as if the kernel expanded a loader search token there.

By default, setting the path normally writes DT_RUNPATH rather than forcing legacy DT_RPATH. RUNPATH applies to direct needed objects; indirect dependencies need their own applicable paths. Environment/cache/default search and secure-execution rules can also affect resolution. Preserve the actual dynamic tags when this distinction matters; do not add --force-rpath reflexively.

Matching filenames or copying libc and its loader does not perfectly reproduce another machine. Check architecture, ABI/symbol versions, dependencies and relevant launch/kernel context. Starting the patched program executes it and its libraries, so a controlled runtime check is a separate requested step. Missing-loader, missing-library and symbol-version failures require different repairs. Keep unresolved compatibility or runtime evidence explicit.

See the upstream [PatchELF manual](https://github.com/NixOS/patchelf/blob/master/patchelf.1) and [dynamic-loader search rules](https://manpages.debian.org/bookworm/manpages/ld.so.8.en.html) for installed-version behavior.
