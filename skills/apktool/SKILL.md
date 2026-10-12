---
name: apktool
description: Decode Android APK resources and rebuild an authorized edited copy with Apktool. Use when resource-only inspection, missing frameworks, SDK metadata or lost signatures make results ambiguous.
---

# Decode the part needed for the task

Read this entire SKILL.md before acting. Require an acquired APK copy and the installed Apktool/Java pair. Select decode-only or an authorized edited-copy rebuild; framework registration is conditional on a matching missing resource package. Finish with status/diagnostics, the selected resource or new artifact and separate signature/installability evidence. No package-local conditional resources are required.

Define `apk` as the selected absolute APK path, `decoded` as a fresh output directory, `frames` as a task-local framework directory and `log` as a separate private log. Preserve the original APK. Check the installed help/version: 2.x uses `apktool --version`; 3.x documents `apktool version`. A verified standalone distribution can be invoked as `java -jar "$apktool_jar"` in place of `apktool`.

For manifest/resource inspection without disassembling DEX:

~~~bash
umask 077
apktool d -s "$apk" -p "$frames" -o "$decoded" >"$log" 2>&1
status=$?
~~~

Check status and diagnostics before consuming the directory. `-s` preserves DEX bytes; it does not mean the APK contains no code. Omit it in a fresh decode when smali inspection is needed. `-r` skips resource decoding, so it defeats a resource-string investigation. Decode `-f` deletes an existing destination; choose a new directory instead of silently replacing earlier evidence. See the [2.x](https://apktool.org/docs/2.x/cli-parameters/) or [3.x options](https://apktool.org/docs/cli-parameters/).

Inspect the manifest's selected application label, corresponding `res/values*/` strings, assets and `apktool.yml`. A display name containing a company word does not establish the publisher. A stored token is evidence of packaged data; its validity, service and permissions need separate evidence. Resource variants and references mean the first matching string may not be the value selected on a device.

Decode output is not the original complete application source. DEX disassembly produces smali; assets can separately contain JavaScript bundles or other runtime data. Inspect an acquired bundle as data without running it. A dense, minified bundle or unfamiliar module wrapper alone does not establish encryption, irrecoverable obfuscation or the absence of readable configuration. Preserve the selected asset's identity and distinguish its contents from code actually observed running on a device.

Keep `compileSdkVersion`, `targetSdkVersion` and `minSdkVersion` separate: build API, targeted behavior and minimum runtime requirement answer different questions. A custom script's compile-SDK threshold is not an Android compatibility test. Read structured metadata rather than treating a single formatting-dependent grep miss as absence. See Android's [SDK attributes](https://developer.android.com/guide/topics/manifest/uses-sdk-element).

If a vendor resource package is missing, obtain the matching framework from the authorized device/firmware and register it only in the task-local cache:

~~~bash
apktool if "$framework_apk" -p "$frames"
~~~

Then retry into a fresh directory with the same `-p`. AOSP defaults do not supply every vendor framework. Unresolved/dummy resources make a decode incomplete; forcing broken resources is not a validated repair. See [framework handling](https://apktool.org/wiki/in-depth/frameworks/).

# Rebuild only the intended edited copy

After reviewing an authorized resource change, define `rebuilt` as a new absolute APK path and `build_log` as a fresh log:

~~~bash
apktool b "$decoded" -p "$frames" -o "$rebuilt" >"$build_log" 2>&1
status=$?
~~~

The input is the decoded directory containing `apktool.yml`, not the APK itself. Resolve the first resource/compiler error before interpreting downstream failures. AAPT selection differs across releases; use the installed version's options instead of copying flags from an old walkthrough.

Successful [building](https://apktool.org/wiki/the-basics/building/) does not restore the original signature or establish installability. `--copy-original` copies manifest/signature metadata; it cannot authenticate changed bytes. Signing is a separate authorized build step. Where Android Build Tools are available, independently inspect the output:

~~~bash
apksigner verify --verbose --print-certs "$rebuilt"
~~~

Retain verification status and signer fingerprints. An unsigned failure is expected before signing; a different signer can prevent an update to an installed app. An organization string in a certificate is insufficient identity evidence. Use [Android signature verification](https://developer.android.com/tools/apksigner), with the intended supported API range, rather than a generic JAR verifier as the sole APK acceptance gate.
