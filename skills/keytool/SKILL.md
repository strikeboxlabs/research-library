---
name: keytool
description: Create an owned test signing identity or inspect a selected Java keystore alias. Use when keystore format, certificate identity and artifact signing are being confused.
---

# Select or create the intended test identity

Read this entire SKILL.md before acting. Require the trusted installed JDK and intended keystore/alias; generation additionally needs an authorized new test identity and fresh keystore destination. No conditional resources are required. Finish with command status, entry type, certificate fingerprint and validity; keep passwords/private-key material out of the result.

Define `keystore` and `alias` as the selected store and exact entry. Inspect:

~~~bash
keytool -list -v -keystore "$keystore" -alias "$alias"
status=$?
~~~

Check entry type, key algorithm, chain and SHA-256 fingerprint. A trusted-certificate entry has no signing private key. Subject fields/self-signing do not establish another publisher's identity.

For a new owned test key, select positive `validity_days` for the actual test lifetime and a fresh private store:

~~~bash
umask 077
keytool -genkeypair -storetype PKCS12 -keystore "$keystore" -alias "$alias" \
  -keyalg RSA -keysize 3072 -validity "$validity_days"
status=$?
~~~

Respond to the identity/password prompts privately. This creates a private-key entry and self-signed certificate; it does not sign an APK/JAR. Inspect the created entry before using it. Do not add a test identity to an existing production store as an implicit retry. A .keystore/.jks suffix does not choose the actual format; retain the explicit type and JDK policy.

Reference: [JDK keytool commands](https://docs.oracle.com/en/java/javase/25/docs/specs/man/keytool.html).
