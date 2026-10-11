# Sign the intended owned archive copy

Require the owned reviewed archive, authorized signing identity and its actual private-key keystore alias. Define `archive`, `keystore`, `alias` and `signed` as the intended input, key store, selected identity and a fresh private output. Preserve the original; omitting -signedjar would overwrite it. Choose algorithms from the actual key/build contract and installed JDK policy.

~~~bash
jarsigner -keystore "$keystore" -signedjar "$signed" "$archive" "$alias"
status=$?
~~~

The tool prompts for necessary passwords; do not put them in command history. Retain status, warnings and the output identity. A signed-success message can coexist with certificate warnings. Independently verify coverage and signer fingerprint as described in the entrypoint. Generating or using a test key gives the copy that identity, not the original publisher's identity.

For APKs, this is the legacy JAR/v1 path. If it is the selected build requirement, align **after** jarsigner signing, then use Android signature verification on the final artifact. With apksigner, align **before** signing and do not modify the archive afterward. The two orders cannot be interchanged. Installation/update compatibility and runtime behavior require separate evidence.

References: [JDK jarsigner](https://docs.oracle.com/en/java/javase/25/docs/specs/man/jarsigner.html), [Android alignment/signing order](https://developer.android.com/tools/zipalign?hl=en).
