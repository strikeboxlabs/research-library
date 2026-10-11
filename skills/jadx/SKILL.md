---
name: jadx
description: Use the jadx CLI to inspect APK resources and DEX call paths without launching the app. Use when a resource hit needs code context or decompiler errors and renamed classes make a conclusion uncertain.
---

# Follow packaged data into code

Read this entire SKILL.md before acting. Use the export and resource-to-call procedure below for static APK inspection; use the incomplete-decompilation section when a relevant class or method is uncertain. Require the selected local APK, an installed jadx with its supported Java runtime and fresh private output locations. Finish with the specific code relationship, export diagnostics and any unresolved path; if the input or runtime is missing, report that prerequisite before claiming an inspection.

Use `jadx`, the CLI entrypoint, on the selected APK; `jadx-gui` is optional. Inspect `jadx --version` and `jadx --help` for installed flags. Define `apk` as its absolute path, `out` as a fresh private output directory and `log` as a separate private log:

~~~bash
umask 077
jadx -j 2 -d "$out" "$apk" >"$log" 2>&1
status=$?
~~~

The normal export includes `sources/` and `resources/`. `-s` omits Java decompilation; use it for resource-only triage. `-r` omits resources and can hide the manifest/string evidence being sought. Check `status` and diagnostics before searching generated files: files may exist after an incomplete export. A duplicate-class warning means the named definitions were not all loaded; retain their input locations and qualify conclusions about that class. Loaded class/method totals do not establish complete or correct reconstruction. See [CLI options](https://github.com/skylot/jadx).

Start at the manifest's actual entry activity and follow its calls. A small WebView wrapper can point to a remote site while service settings reside in resource XML. Search candidate names without dumping all their values:

~~~bash
rg -l -i 'token|api[_-]?key|password|https?://' "$out/resources" "$out/sources"
~~~

Review only the relevant files privately. Record resource identifier, location, consuming code and destination; keep secrets out of shared findings. A resource hit can be an unused placeholder, expired token or public identifier. A loaded URL does not show that the app sends every stored token there. No matches cannot exclude obfuscated, constructed, native or remotely supplied values. If a token needs validation, endpoint/account scope and authorization are separate from static inspection.

# Resolve an incomplete decompilation

For a class of interest, define `class_name` as its fully qualified raw name or recognized alias and `class_out` as a fresh output location:

~~~bash
jadx --single-class "$class_name" --single-class-output "$class_out" "$apk"
~~~

Decompiled Java reconstructs bytecode; it is not the original source. A skipped method or inconsistent block prevents a confident conclusion about that path even if other classes exported successfully. On supporting versions, use `--decompilation-mode simple` or `fallback`, then compare disputed instructions with smali/control-flow evidence. `--show-bad-code` exposes an uncertain reconstruction; it does not correct it. For renamed/inlined classes, check mapping and inlining options before declaring code absent. Reduce `-j` when memory pressure interrupts export and repeat into a fresh directory. The [upstream troubleshooting guide](https://github.com/skylot/jadx/wiki/Troubleshooting-Q%26A) explains these recovery branches.

Finish with the specific resource-to-call relationship found and the unresolved paths. Static export alone establishes neither live credential validity nor runtime behavior.
