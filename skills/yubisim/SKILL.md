---
name: yubisim
description: Generate a Yubico OTP with dorchain Yubisim from authorized token material. Use when testing an OTP validator or an SSH second factor where token format, counter persistence or Java compatibility matters.
---

# Generate one OTP and preserve its state

Read this entire SKILL.md before acting, then read [token format, generation and validation](references/token-generation.md) fully. Use the existing compiled simulator and matching Java runtime; generation rewrites the token file. Finish with the generation/save outcome and, when requested, the separate validator result. An OTP on stdout is not successful authentication.

This is dorchain's `yubi_simulator` Java class, not a generic OATH TOTP generator or a FIDO2 emulator. Define `java_bin` as the trusted runtime, `class_dir` as the directory containing its reviewed compiled classes, `token_file` as the protected writable token working file and `otp_file` as a fresh private result:

~~~bash
umask 077
"$java_bin" -cp "$class_dir" yubi_simulator "$token_file" > "$otp_file"
~~~

Check exit status and the persisted counter before using the result. Never point a retry at a restored stale state merely because an earlier login failed. Token secrets and generated OTPs belong in private task artifacts, not reusable instructions or general logs.

The original source imports `javax.xml.bind.DatatypeConverter`; a bare modern JDK can fail because JAXB was removed from JDK 11. Select an already supported runtime/build or its existing compatible JAXB classpath. Missing classes are a deployment prerequisite, not a reason to change the authentication algorithm. See the [upstream simulator](https://github.com/dorchain/yubisim) and [JDK removal notes](https://docs.oracle.com/en/java/javase/21/migrate/removed-tools-and-components.html).
