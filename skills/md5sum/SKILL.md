---
name: md5sum
description: Reproduce a legacy MD5 checksum over exact file or pipeline bytes and verify an existing checksum manifest with GNU md5sum. Use for newline, text-mode and digest-stage discrepancies.
---

# Identify the bytes actually hashed

Read this entire SKILL.md before acting; reuse complete current context. Select the exact file or completed producer output, preserve byte boundaries and inspect status. Finish with that checksum/comparison and its limits; MD5 consistency does not establish authenticity against deliberate collision attacks.

Define `artifact` as the existing absolute input path:

~~~bash
md5sum --binary -- "$artifact"
~~~

The output includes 32 hex digits, a mode marker and filename; the whole output line is not the digest. Hashing a crypt record, its printed hexadecimal text or a raw password gives different inputs. Preserve producer status before treating an empty/partial stream as intended data.

For an **illustrative public string**, these intentionally differ:

~~~bash
printf '%s' 'demo' | md5sum --binary
printf '%s\n' 'demo' | md5sum --binary
~~~

Command substitution removes trailing newlines; capture producer output directly to a file when exact pipeline bytes matter. GNU/Linux text/binary modes normally coincide, but another platform's text translation can change bytes. Use binary mode for portable byte comparison.

For an existing trusted GNU-format manifest, define `manifest` and run `md5sum --check --strict -- "$manifest"` from the intended base directory. Relative member paths depend on that directory. Check exit status and per-file diagnostics: a missing input, malformed record and mismatch are different failures. Review manifest paths before reading them; an MD5 match is consistency with the supplied manifest, not independent trust in it.

Reference: [GNU md5sum](https://www.gnu.org/software/coreutils/manual/html_node/md5sum-invocation.html).
