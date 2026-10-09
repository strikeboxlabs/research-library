---
name: gpp-decrypt
description: Decode a captured Group Policy Preferences cpassword locally using the correct gpp-decrypt implementation. Use when reviewing GPP XML and distinguishing recovered historical secrets from validated credentials.
---

# GPP cpassword decoding

Extract the complete `cpassword` attribute from the source XML, with its associated `userName`, policy path and timestamp. Preserve characters such as `/` and `+`; PDF display wrapping is not part of the value. Define `cpassword` as that exact string.

Two different programs use this name. Identify the installed package before selecting syntax:

| Implementation | Invocation |
|---|---|
| Kali's Ruby `gpp-decrypt` package | `gpp-decrypt "$cpassword"` |
| t0thkr1s Python package | `gpp-decrypt -c "$cpassword"`; `-f "$xml"` can read a local XML file |

This is deterministic decryption using the published GPP key, not a wordlist attack. It requires neither a domain connection nor a password guess. An error suggests checking the implementation, copied value and XML field before assuming the password is unrecoverable.

Keep the recovered value tied to its account and original policy. A successful decode establishes what the artifact stored, not whether the account exists, its privileges or whether the password still works. A backup or replication share can contain stale preferences.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Active PDF pp. 4–5. Maintenance sources: [Kali package usage](https://www.kali.org/tools/gpp-decrypt/) and [Python implementation](https://github.com/t0thkr1s/gpp-decrypt).
