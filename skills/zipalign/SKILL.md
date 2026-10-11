---
name: zipalign
description: Check or align one owned Android APK with SDK zipalign. Use when native-library page alignment or signing order makes a rebuilt artifact fail acceptance.
---

# Verify alignment before changing the copy

Read this entire SKILL.md before acting. Require the installed SDK Build Tools implementation, owned APK and its intended signing path. No conditional resources are required. Finish with alignment status and separate final signature evidence; alignment alone does not prove installability.

Define `apk` as the selected file. Check installed help for -P support:

~~~bash
zipalign -c -P 16 -v 4 "$apk"
status=$?
~~~

-c checks without rewriting. The 4 value selects ordinary uncompressed-entry alignment; -P 16 selects 16 KiB alignment for uncompressed native libraries. An older binary lacking -P leaves that requirement unresolved; plain 4-byte alignment is a narrower check.

If alignment is needed, define `aligned` as a fresh output:

~~~bash
zipalign -P 16 -v 4 "$apk" "$aligned"
status=$?
~~~

Inspect status and recheck the output. Omit -f to avoid overwriting existing evidence. Align before apksigner signing; subsequent archive changes invalidate that signature. For the selected legacy jarsigner/v1 path, align after signing. Verify the final APK with Android's signature verifier and intended signer/API range. Do not apply the legacy sequence to modern signed APKs.

Reference: [Android zipalign](https://developer.android.com/tools/zipalign?hl=en).
