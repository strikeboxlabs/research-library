---
name: oathtool
description: Generate TOTP from an authorised known secret and diagnose encoding, algorithm, digit-count and clock mismatches without confusing local generation with successful authentication.
---

# TOTP generation and mismatch diagnosis

Read this entire SKILL.md before acting. Use only the task's authorized known enrollment, confirm its parameters and keep its secret/code private. No conditional resources are required. Finish with the local calculation or specific parameter/tool gap; server acceptance is a separate result.

Check `oathtool --version` and `--help`. Confirm the provisioning parameters: TOTP or HOTP, secret encoding, MAC algorithm, digits and period. Oathtool defaults to HOTP and hexadecimal keys; those defaults do not match a typical Base32 TOTP enrollment.

For an authorised enrollment using SHA1, six digits and a 30-second period, define `secret_file` as a private file containing only its Base32 secret:

~~~bash
oathtool --totp=SHA1 --base32 --digits=6 --time-step-size=30s - < "$secret_file"
~~~

`-` reads the key from stdin, keeping its value out of process arguments. The file must not contain an entire provisioning URI, account label, recovery-code list or authentication configuration. Preserve leading zeroes in the resulting code. Avoid `--verbose` with a real enrollment: it prints the key in multiple encodings. The code itself is authentication material; keep it out of shared transcripts.

If a service rejects the code, distinguish local calculation from server acceptance. Check the exact account/enrollment, algorithm, digit count, period, Unix clock and any configured start epoch. A code generated near a boundary may expire in transit; a replay may also be rejected. Correct TOTP does not establish the primary password or account policy. Increasing the local `--window` does not widen the server's acceptance policy.

## Separate a tool problem from an enrollment problem

Use this **public RFC 6238 reference vector**, not a real secret, to check deterministic calculation:

~~~bash
oathtool --totp=SHA1 --digits=8 --time-step-size=30s \
  --now='1970-01-01 00:00:59 UTC' \
  3132333435363738393031323334353637383930
~~~

The published expected value is `94287082`. Here the key is hexadecimal, so there is no `--base32`. Matching it establishes this calculation, not the current clock, another algorithm or any remote login. If it differs, resolve the local version/options before using live credentials.

Consult [oathtool's options](https://oath-toolkit.codeberg.page/oathtool.1.html) for input and time parsing, and [RFC 6238](https://www.rfc-editor.org/rfc/rfc6238.html#appendix-B) for algorithm-specific test vectors.
