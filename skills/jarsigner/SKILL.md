---
name: jarsigner
description: Sign an owned JAR copy or inspect signature coverage and certificate warnings with jarsigner. Use when strict checks differ or a JAR result is being mistaken for Android APK acceptance.
---

# Read verification evidence, not just the exit code

Read this entire SKILL.md before acting. Require the selected archive and trusted installed JDK; choose verification or owned-copy signing. For signing with the intended keystore identity, read [owned archive signing](references/owned-signing.md) fully. Finish with actual signed-entry coverage, signer evidence and diagnostics, or the new signed copy plus independent verification. APK acceptance additionally requires the Android-aware check below.

Define `archive` as the selected absolute JAR/ZIP path and `log` as a fresh verification transcript. Select the intended JDK's `jarsigner`; retain its Java version because disabled-algorithm policy changes between releases.

~~~bash
umask 077
jarsigner -verify -strict -verbose -certs "$archive" >"$log" 2>&1
status=$?
~~~

`-verify` matters: signing is otherwise the tool's default operation. This command reads the archive without launching its classes. Review the entire transcript and the entry coverage. In verbose listings, `s` marks a verified signature and `m` marks a manifest entry; `m` alone does not authenticate that entry. A successful signed-entry check still requires a separate decision about which signer is acceptable.

| Evidence | Interpretation and next decision |
|---|---|
| `jar is unsigned` or no manifest | No verified publisher signature. Reject a signed-artifact requirement even if status is zero. |
| Verified entries plus unsigned entries | Coverage is incomplete; identify the unsigned content before accepting the archive. |
| Certificate/algorithm warnings | Separate content integrity from certificate trust, expiry, usage and disabled-algorithm policy. |
| Digest/signature mismatch or unreadable ZIP | Verification failed; retain the original and investigate corruption/modification or format. |

Without `-strict`, severe warnings can still return zero. With it, warning bits are combined (for example certificate issues 4, unsigned entries 16); status 1 identifies a failure. **Strict mode is not a universal signed-content gate:** the OpenJDK 21 verifier can also return zero for an unsigned ZIP with no manifest. Require affirmative signature/coverage evidence. Do not grep for the legend text `s = signature was verified` and mistake it for an actual signed entry. See the [command reference](https://docs.oracle.com/en/java/javase/25/docs/specs/man/jarsigner.html) and [OpenJDK verification implementation](https://github.com/openjdk/jdk21u/blob/master/src/jdk.jartool/share/classes/sun/security/tools/jarsigner/Main.java).

# Use Android verification for APK acceptance

JAR verification covers the JAR/v1 scheme; APK v2 and later schemes require Android-aware validation. With the SDK Build Tools verifier already available:

~~~bash
apksigner verify --verbose --print-certs "$archive"
status=$?
~~~

Inspect the signature schemes, supported API range and signer fingerprint. Compare identity to a trusted expected certificate/lineage; a certificate subject's company name is merely a field. The default API range comes from the manifest minimum and the verifier's maximum; select an explicit range only when it matches the task. See [apksigner verification](https://developer.android.com/tools/apksigner).

Repacking resources does not preserve a valid original signature. Copying `META-INF` is not re-signing, and a display-name substring is not publisher verification. A successful generic JAR exit status cannot resolve those questions. If Android verification is unavailable, report APK signing status as unresolved rather than inferring it from `jarsigner` alone.
